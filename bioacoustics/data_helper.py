import s3fs
import os
import pandas as pd
import intake
import xarray as xr

import tempfile
import shutil

from intake.source.utils import reverse_format



def get_s3_imos_data(bucket="imos-data/IMOS/SOOP/SOOP-BA"):
  """Returns a dataframe of all netcdf files in the S3 imos bucket"""
  data = []
  fs = s3fs.S3FileSystem(anon=True)
  for dirpath, dirname, filename in fs.walk(bucket):
    if len(filename) > 0:
      for _ in filename:
        if _.endswith(".nc"):
          d = reverse_format('IMOS_SOOP-BA_AE_{start}_{platform_code}_FV02_{product_type}_END-{end}_C-{creation}.nc', _)
          d['url'] = "/".join([dirpath, _])
          data.append(d)
  df = pd.DataFrame(data)
  return df

def open_nc_file_from_S3(filepath):
  """file path assumed to contain bucket name"""
  fs = s3fs.S3FileSystem(anon=True)
  file_obj = fs.open(filepath)
  ds = xr.open_dataset(file_obj)
  return ds


def download_imos_file_from_S3(file_list, dir_path):
  fs = s3fs.S3FileSystem(anon=True)
  for filepath in filelist:
    filename = filepath.split('/')[0]
    fs.download(filepath, os.path.join(dir_path, filename))

def mkd_temp_dir():
  temp_dir_path = tempfile.mkdtemp()
  print("tempory directory: ", temp_dir_path)
  return temp_dir_path


def remove_temp_dir(temp_dir_path):
  shutil.rmtree(temp_dir_path)
