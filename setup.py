import sys
import os
import os.path
__REPOSITORY_ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
if __REPOSITORY_ROOT_DIR not in sys.path:
    sys.path.insert(0, __REPOSITORY_ROOT_DIR)
os.chdir(__REPOSITORY_ROOT_DIR)

import setuptools
from datalidator.DatalidatorConstants import DatalidatorConstants


with open("./README.md", "r") as readme_io:
    readme_text = readme_io.read()


setuptools.setup(
    name="datalidator",
    version=DatalidatorConstants.LIBRARY_VERSION,
    description="A flexible, object-oriented Python input data parsing & validation library",
    long_description=readme_text,
    long_description_content_type="text/markdown",
    author="Vít Labuda",
    author_email="dev@vitlabuda.cz",
    license="BSD License",
    url="https://github.com/vitlabuda/datalidator",
    project_urls={
        "Bug Tracker": "https://github.com/vitlabuda/datalidator/issues",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries",
        "Typing :: Typed",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.9",
    tests_require=["pytest", "requests"],
)
