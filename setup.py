#!/usr/bin/env python
import os

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding="utf-8").read()


setup(
    name="tilingsgui",
    version="0.1.1",
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
    install_requires=["pyperclip==1.8.0", "pyglet==1.5.5", "tilings==2.0.0"],
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
