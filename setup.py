# Python setup file for installation
from setuptools import setup, find_packages

setup(
    name="metadata-python-sdk",
    version="0.1.0",
    description="Python SDK for Metadata AI platform",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # Add dependencies here
    ],
    python_requires=">=3.7",
)

