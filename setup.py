import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="delimiter_check",
    version="0.1.0",
    author="Jonas Kaerts",
    description="Checking for delimiter matching in text files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
)