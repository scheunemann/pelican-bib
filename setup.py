import pelican_bib
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

CLASSIFIERS = """\
Development Status :: 3 - Alpha
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: Public Domain
Programming Language :: Python
Programming Language :: Python :: 3
Topic :: Scientific/Engineering
Operating System :: POSIX
Operating System :: Unix
"""

setuptools.setup(
    name="pelican_bib",
    version=pelican_bib.__version__,
    author="Marcus M. Scheunemann",
    author_email="find@mms.ai",
    description="Organize your scientific publications using Pelican and BibTeX",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://mms.ai",
    packages=setuptools.find_packages(),
    classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f],
)
