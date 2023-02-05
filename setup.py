from distutils.core import setup

setup(
    name="xindmap",
    version="0.1",
    description="",
    author="Thomas Petiteau",
    author_email="thomas.petiteau@outlook.com",
    url="https://github.com/XanX3601/xindmap",
    entry_points={"console_scripts": ["xindmap=xindmap.main:main"]},
    install_requires=["customtkinter==5.0.5", "rich_click==1.6.0"],
)
