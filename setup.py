from setuptools import setup, find_packages

setup(
    name="xindmap",
    version="0.1",
    description="",
    author="Thomas Petiteau",
    author_email="thomas.petiteau@outlook.com",
    url="https://github.com/XanX3601/xindmap",
    packages=find_packages(),
    entry_points={"console_scripts": ["xindmap=xindmap.main:main"]},
    install_requires=[
        "customtkinter==5.1.2",
        "pytest==7.2.1",
        "rich_click==1.6.0",
        "singleton-decorator==1.0.0",
        "sortedcontainers==2.4.0",
    ],
    extras_require={
        "dev": [
            "mkdocs==1.4.2",
            "mkdocs-material==9.1.3",
            "mkdocstrings==0.20.0",
        ]
    }
)
