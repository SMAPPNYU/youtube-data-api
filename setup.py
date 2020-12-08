import os
import sys
from setuptools import setup

if sys.version_info[0] != 3:
    raise RuntimeError('Unsupported python version "{0}"'.format(
        sys.version_info[0]))

def _get_file_content(file_name):
    with open(file_name, 'r') as file_handler:
        return str(file_handler.read())
def get_long_description():
    return _get_file_content('README.md')

on_rtd = os.environ.get('READTHEDOCS') == 'True'

if not on_rtd:
    INSTALL_REQUIRES = [
        'pandas',
        'requests',
    ]
else:
    INSTALL_REQUIRES = [
        'requests',
    ]

setup(
    name="youtube-data-api",
    version='0.0.21',
    author="Leon Yin, Megan Brown",
    description="youtube-data-api is a Python wrapper for the YouTube Data API.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    keywords='youtube-data-api youtube-data youtube-api wrapper youtube tweepy social-media',
    url="https://github.com/mabrownnyu/youtube-data-api",
    packages=['youtube_api'],
    py_modules=['youtube_api'],
    license="MIT",
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=INSTALL_REQUIRES
)
