from setuptools import setup, find_packages


LIBRARY_NAME = "code_tree"
PACKAGE_DIR = 'code_tree'

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name=LIBRARY_NAME,
    version="0.1.1",
    # package_dir={"": PACKAGE_DIR},
    # packages=find_packages(PACKAGE_DIR),
    packages=find_packages(),
    install_requires=install_requires,
    author="kenyo3023",
    author_email="kenyo3023@gmail.com",
    description="",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kenyo3026/code-tree-parser",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)