import codecs
import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()


VERSION = "0.4.2"

PACKAGE_NAME = "Evaluation machine translation"
DESCRIPTION = ""
LONG_DESCRIPTION = "common methods used to evaluate machine translation,"
AUTHOR_NAME = "Alireza Parvaresh"
AUTHOR_EMAIL = "parvvaresh@gmail.com"
PROJECT_URL = "https://github.com/parvvaresh/Evaluation-of-machine-translation-by-NLP"
REQUIRED_PACKAGES = []
PROJECT_KEYWORDS = ["nlp", "machine translation" , "bleu", "nist", "glue" ,"chrf", "wer" , "ter" , "meteor"]

CLASSIFIERS = [
    "Development Status :: 1 - Planning",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3",
    "Operating System :: Unix",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
]
setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    url=PROJECT_URL,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=REQUIRED_PACKAGES,
    keywords=PROJECT_KEYWORDS,
    classifiers=CLASSIFIERS,
)
