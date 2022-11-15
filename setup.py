from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jet",
    version="0.0.1",
    author="Antonio Leitao",
    author_email="aleitao@novaims.unl.pt",
    description="Simple clean testing toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Antonio-Leitao/jet",
)
