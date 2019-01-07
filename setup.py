from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Topic :: Software Development :: Libraries",
]

setup(
    name="falcon_pagination",
    author="Raphael Cohen",
    author_email="raphael.cohen.utt@gmail.com",
    url="https://github.com/darkheir/falcon-pagination-hook",
    version="0.0.1",
    classifiers=classifiers,
    description="Falcon pagination helper",
    long_description=open("README.rst").read(),
    keywords="falcon pagination api",
    packages=find_packages(include=("falcon_pagination*",)),
    install_requires=["falcon>=0.3"],
    include_package_data=True,
    license="MIT",
)
