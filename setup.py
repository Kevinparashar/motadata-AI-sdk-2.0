# Python setup file for installation
from setuptools import setup, find_packages
from pathlib import Path

# Read version from __version__.py
version_file = Path(__file__).parent / "src" / "__version__.py"
exec(open(version_file).read())

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="metadata-python-sdk",
    version=__version__,
    description="Python SDK for Metadata AI platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Metadata AI Team",
    author_email="team@metadata.ai",
    url="https://github.com/metadata-ai/python-sdk",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # Core dependencies will be added as needed
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords=["ai", "sdk", "agents", "machine-learning", "api"],
)

