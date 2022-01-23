import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xindmap",
    version="1.0.0",
    author="Thomas Petiteau",
    author_email="thomas.petiteau@outlook.com",
    description="Mind mapping app targeted at developpers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/XanX3601/xindmap",
    include_package_data=True,
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": ["xindmap=xindmap.main:main"]},
    install_requires=[],
)
