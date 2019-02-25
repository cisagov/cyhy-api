"""Setup environment for Cyber Hygiene API Server."""

from setuptools import setup, find_packages

install_requires = [
    "Flask == 1.0.2",
    "Flask-JWT-Extended == 3.17.0",
    "Flask-GraphQL == 2.0.0",
    "graphene-mongo == 0.2.0",
    "mongoengine == 0.16.3",
    "Flask-Bcrypt",  # compiled in Dockerfile
    "docopt == 0.6.2",
    "PyYAML == 3.12",
    "python-dateutil == 2.7.5",
]

tests_require = [
    'pytest == 4.1.1',
    'mock == 2.0.0',
    'mongomock == 3.15.0'
]

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
            'cyhy-api-server=cyhy_api.api:main',
        ],
    },
    license='LICENSE.txt',
    description='Cyber Hygiene API Server',
    # long_description=open('README.md').read(),
    install_requires=install_requires + tests_require,
    # tests_require=tests_require
)
