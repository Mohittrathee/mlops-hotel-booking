from setuptools import find_packages, setup

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="ml_ops",
    version="0.0.1",
    author="Mohit Rathee",
    author_email="deep.rathee426@gmail.com",
    packages=find_packages(),
    install_requires=requirements,
)