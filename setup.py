from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in llm_bot/__init__.py
from llm_bot import __version__ as version

setup(
	name="llm_bot",
	version=version,
	description="Chat with LLM",
	author="yiouyou",
	author_email="zhuosong@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
