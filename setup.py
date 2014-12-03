from setuptools import setup, find_packages

from dbl import __author__, __version__

if __name__ == '__main__':
    package_name = 'dbl'
    setup(
        name=package_name,
        author=__author__,
        version=__version__,
        packages=find_packages(),
        package_dir={package_name: package_name},
        test_suite='tests'
    )
