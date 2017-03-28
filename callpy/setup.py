from setuptools import setup

NAME = "callpy"

with open("README.rst") as fo:
    README = fo.read()

setup(
    name=NAME,
    description=README.split("\n")[0],
    long_description=README,
    author="Petri Heinilä",
    author_email="hevi00@gmail.com",
    url="http://github.com/hevi9/" + NAME,
    packages=[NAME],
    setup_requires=[
        "setuptools_scm"
    ],
    use_scm_version=True,
    entry_points={
        "console_scripts": [
            "callpy=callpy:main",
        ]
    },
    install_requires=[
    ]
)
