from setuptools import setup, find_packages

# Read requirements.txt
with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="gcp-oauth-utils",
    version="0.1",
    packages=find_packages(),
    install_requires=required,  
    url="https://github.com/Ruairi-osul/gcp-oauth-utils",
    license="MIT",
    author="Your Name",
    author_email="ruairi.osullivan.work@gmail.com",
    description="A small Python library for working with the OAuth2 protocol on Google Cloud Platform",
)
