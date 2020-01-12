import re
from setuptools import setup
import setuptools
 
 
with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")
 
setup(
    name = "py-mconv",
    packages = ['mconv'],
    entry_points = {
        "console_scripts": ['mconv = mconv.cli:main']
        },
    install_requires=[
        'pandas>=0.25.3',
    ],
    version = '0.0.0',
    description = "a command line tool for converting many formats of key-value data from files to files.",
    long_description = long_descr,
    long_description_content_type="text/markdown",
    author = "Myriad-Dreamin",
    author_email = "camiyoru@gmail.com",
    url = "https://github.com/Myriad-Dreamin/py-mconv",
    )