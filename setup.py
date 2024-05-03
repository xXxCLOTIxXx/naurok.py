from setuptools import setup, find_packages
from platform import system

with open("README.md", "r") as file:
	long_description = file.read()

link = 'https://github.com/xXxCLOTIxXx/naurok.py/archive/refs/heads/main.zip'
ver = '1.0'
setup(
	name = "naurok.py",
	version = ver,
	url = "https://github.com/xXxCLOTIxXx/naurok.py",
	download_url = link,
	license = "MIT",
	author = "Xsarz",
	author_email = "xsarzy@gmail.com",
	description = "Library for working with tests naurok.ua.",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	keywords = [
		"naurok.py",
		"naurok",
		"naurok-py",
		"naurok-bot",
		"api",
		"python",
		"python3",
		"python3.x",
		"xsarz",
		"official",
		"async",
		"sync",
		"naurok"
	],
	install_requires = [
		"requests",
		"selenium",
		"faker",
		"bs4"
	],
	packages = find_packages()
)
