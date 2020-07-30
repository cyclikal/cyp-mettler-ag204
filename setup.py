import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cyp-random", # Replace with your own username
    version="0.1.dev1",
    author="Gabriel Ewig",
    author_email="gabriel@cyclikal.com",
    description="Example Cyckei Plugin Package, Generates Random Numbers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cyclikal/cyp-random",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
    ],
    python_requires='>=3.6',
)
