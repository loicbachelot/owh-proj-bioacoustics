import s3fs
import os
import pandas as pd
import intake
import xarray as xr

import tempfile
import shutil

from datetime import datetime
from intake.source.utils import reverse_format

dtstr = lambda t: datetime.strptime(t, "%Y%m%dT%H%M%SZ")

def get_s3_imos_data(bucket="imos-data/IMOS/SOOP/SOOP-BA"):
  """Returns a dataframe of all netcdf files in the S3 imos bucket, with start and end
  datetime stamps for searching between periods. Defaults to the S3 imos bucket."""
  data = []
  fs = s3fs.S3FileSystem(anon=True)
  for dirpath, dirname, filename in fs.walk(bucket):
    if len(filename) > 0:
      for _ in filename:
        if _.endswith(".nc"):
          d = reverse_format('IMOS_SOOP-BA_AE_{start_date}_{platform_code}_FV02_{product_type}_END-{end_date}_C-{creation}.nc', _)
          d['url'] = "/".join([dirpath, _])
          d['start_date'] = dtstr(d['start_date'])
          d['end_date'] = dtstr(d['end_date'])
          d['creation'] = dtstr(d['creation'])
          data.append(d)
  df = pd.DataFrame(data)
  return df

def open_nc_file_from_S3(filepath):
  """Open netCDF acoustic data file directly from S3 and return xarray dataset.
  filepath assumed to contain bucket name"""
  fs = s3fs.S3FileSystem(anon=True)
  file_obj = fs.open(filepath)
  ds = xr.open_dataset(file_obj)
  return ds

def search_imos_data_url(url=None):
  try:
    val = df[df['url'].str.contains(url)]
  except:
    print("url not found")
    val = None
  return val


def mkd_temp_dir():
  """Creates a local temporary directory in the current working directory to
  download imos S3 data to.
  Returns directory name"""
  temp_dir_path = tempfile.mkdtemp()
  print("tempory directory: ", temp_dir_path)
  return temp_dir_path

def download_imos_file_from_S3(file_list, dir_path):
  """Download imos file into the dir_path directory"""
  fs = s3fs.S3FileSystem(anon=True)
  for filepath in filelist:
    filename = filepath.split('/')[0]
    fs.download(filepath, os.path.join(dir_path, filename))


def remove_temp_dir(temp_dir_path):
  """Delete tempory directory"""
  shutil.rmtree(temp_dir_path)
