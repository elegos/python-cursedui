import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cursedui",
    license="LGPLv3",
    version="0.0.1",
    author="Giacomo Furlan",
    author_email="opensource@giacomofurlan.name",
    description="Graphic library based on curses ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/elegos/python-cursedui",
    packages=setuptools.find_packages(''),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    python_requires='>=3.6',
)
