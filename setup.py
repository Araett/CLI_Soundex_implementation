from setuptools import setup, find_packages

setup(
    name="CLI-Soundex-Implementation",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    license="GPL-3.0",
    author="Martynas Saulius",
    author_email="martynas575@gmail.com",
    description="A CLI implementation of American Soundex algorithm",
)
