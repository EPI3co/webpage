from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="webpage",
    version="0.1.2",
    author="Sebastian Tabares Amaya",
    author_email="me@syta.co",
    description="A package for processing HTML files and web content",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EPI3co/webpage.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        # Add your dependencies here
    ],
    entry_points={
        "console_scripts": [
            "webpage=webpage.main:main",
        ],
    },
)
