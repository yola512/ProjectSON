import os

from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

version = os.getenv(
    "VERSION", "0.0.0"
)  # Fallback to '0.0.0' version = os.getenv('PACKAGE_VERSION', '0.0.0')  # Fallback to '0.0.0'



setup(
    name="projectSON",
    version=version,
    author="Jolanta Majcher",
    author_email="jolamajcher12@gmail.com",
    description="Student attendance management",
    long_description = open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        "console_scripts": ["projectSON=src.modules.main:main"], #main() in main.py is an entry point :)
    },
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires=">=3.11",
)
