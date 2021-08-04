from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='ohw-proj-bioaccoustics',
    url='https://github.com/oceanhackweek/owh-proj-bioacoustics',
    author='Nick Mortimer, Chris Bladwell', # others
    author_email='',
    # Packages included
    packages=['bioacoustics'],
    # dependencies
    install_requires=['numpy', 'xarray', 'intake', 'astral'],
    version='0.1',
    license='MIT',
    description='A package of tools to import and analyse bioacoustics data',
)
