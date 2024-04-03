from setuptools import setup, find_packages


def readme():
    with open("README.md", "r") as f:
        return f.read()


setup(
    name="botmom",
    version="0.0.1",
    author="Arsenii Misiurenko",
    author_email="2028misyurenko.ad@student.letovo.ru",
    description="Easiest and most variable module for creating telegram bots",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Arsenii22/botmom",
    packages=find_packages(),
    install_requires=["aiogram>=3.0", "aiohttp"],
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    keywords="telegram botmom bots chatbots",
    project_urls={
        "GitHub": "https://github.com/Arsenii22/botmom"
    },
    python_requires=">=3.6"
)