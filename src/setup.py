"""Setup environment for Cyber Hygiene REST API Server."""

from setuptools import setup, find_packages

setup(
    name='cyhy_api',
    version='0.0.1',
    author='Mark Feldhousen',
    author_email='mark.feldhousen@trio.dhs.gov',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
          'cyhy-rest-server=cyhy_rest.api:main',
        ],
    },
    license='LICENSE.txt',
    description='Cyber Hygiene API Server',
    # long_description=open('README.md').read(),
    install_requires=[
        "Flask == 1.0.2",
        "Flask-RESTful == 0.3.7",
        "Flask-REST-JSONAPI == 0.22.0",
        "docopt == 0.6.2",
        "PyYAML == 3.12",
        "python-dateutil == 2.7.5",
        "pytest == 4.1.1",  # TODO get pip install -e to pickup tests_require
        "mock == 2.0.0",
    ],
    # tests_require=[
    # 'pytest',
    # 'mock'
    # ]
)
