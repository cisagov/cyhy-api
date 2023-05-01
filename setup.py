"""Setup environment for Cyber Hygiene API Server."""

from glob import glob
from os.path import splitext, basename

from setuptools import setup, find_packages


def readme():
    """Read in and return the contents of the project's README.md file."""
    with open("README.md") as f:
        return f.read()


def package_vars(version_file):
    """Read in and return the variables defined by the version_file."""
    pkg_vars = {}
    with open(version_file) as f:
        exec(f.read(), pkg_vars)  # nosec
    return pkg_vars


install_requires = [
    "docopt == 0.6.2",
    "Flask == 2.3.2",
    "Flask-Bcrypt",  # compiled in Dockerfile
    "flask-cors == 3.0.7",
    "Flask-GraphQL == 2.0.0",
    "Flask-JWT-Extended == 3.18.1",
    "graphene-mongo == 0.2.4",
    "mongoengine == 0.17.0",
    "python-dateutil == 2.8.0",
    "PyYAML == 5.1",
]

extras_require = {
    "test": ["coveralls", "mimesis", "mongomock", "pre-commit", "pytest-cov", "pytest"]
}


setup(
    name="cyhy-api",
    # Versions should comply with PEP440
    version=package_vars("src/cyhy_api/_version.py")["__version__"],
    description="Cyber Hygiene API Server",
    long_description=readme(),
    long_description_content_type="text/markdown",
    # NCATS "homepage"
    url="https://www.us-cert.gov/resources/ncats",
    # The project's main homepage
    download_url="https://github.com/cisagov/skeleton-python-library",
    # Author details
    author="Cyber and Infrastructure Security Agency",
    author_email="ncats@hq.dhs.gov",
    license="License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        # Pick your license as you wish (should match "license" above)
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    # What does your project relate to?
    keywords="cyhy",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    install_requires=install_requires,
    extras_require=extras_require,
    entry_points={"console_scripts": ["cyhy-api-server=cyhy_api.api:main"]},
)
