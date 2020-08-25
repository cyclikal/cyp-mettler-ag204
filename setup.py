import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
shrt = "Cyckei Plugin Package, Reads Weight from Mettler-Toledo AG204 Scale"

setuptools.setup(
    name="cyp-mettler-ag204",
    version="1.0",
    author="Gabriel Ewig",
    author_email="gabriel@cyclikal.com",
    description=shrt,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cyclikal/cyp-random",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
    ],
    python_requires='>=3.6',
)
