#!/usr/bin/env python
import os

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding="utf-8").read()


def get_version():
    with open("tilingsgui/__init__.py", encoding="utf8") as init_file:
        for line in init_file.readlines():
            if line.startswith("__version__"):
                return line.split(" = ")[1].rstrip()[1:-1]
    raise ValueError("Version not found in tilingsgui/__init__.py")


setup(
    name="tilingsgui",
    version=get_version(),
    author="Permuta Triangle",
    author_email="permutatriangle@gmail.com",
    description="A graphical user interface for tilings.",
    license="BSD-3",
    keywords=("gui permutation tiling pyglet"),
    url="https://github.com/PermutaTriangle/tilingsgui",
    project_urls={
        "Source": "https://github.com/PermutaTriangle/tilingsgui",
        "Tracker": "https://github.com/PermutaTriangle/tilingsgui/issues",
    },
    packages=find_packages(),
    long_description=read("README.rst"),
    install_requires=["pyperclip==1.8.0", "pyglet==1.5.7", "tilings==2.2.0"],
    python_requires=">=3.6",
    include_package_data=True,
    classifiers=[
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    entry_points={"console_scripts": ["tilingsgui=tilingsgui.main:main"]},
)
