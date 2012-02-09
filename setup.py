import os, config
from setuptools import setup, find_packages

'''
    Configuration files should be stored inside user's home directory in
    .pykeep folder
'''
def createConfigFolder():
    if not os.path.isdir(config.__USER_CONFIG_PATH__):
        os.mkdir(config.__USER_CONFIG_PATH__)

createConfigFolder()

setup(
    name = "pykeep",
    version = "0.0.0dev1",
    packages = find_packages(),
)
