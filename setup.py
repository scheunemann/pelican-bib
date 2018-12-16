from setuptools import setup, find_packages

version = "0.2.7"
download_url = 'https://github.com/scheunemann/pelican-bib/archive/{}.zip'.format(version)

with open("README.md", "r") as fh:
    long_description = fh.read()

CLASSIFIERS = """\
Development Status :: 3 - Alpha
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Programming Language :: Python
Programming Language :: Python :: 3
Topic :: Scientific/Engineering
Operating System :: POSIX
Operating System :: Unix
Topic :: Software Development :: Libraries :: Python Modules
Topic :: Text Processing
"""

setup(
    name="pelican-bib",
    #version=pelican_bib.__version__,
    version=version,
    download_url=download_url,
    author="Marcus M. Scheunemann",
    author_email="find@mms.ai",
    description="Organize your scientific publications using Pelican and BibTeX",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scheunemann/pelican-bib",
    packages=find_packages(),
    classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f],
)
