import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="ceevee",
	version="1.0.0",
	author="Louis Kraak",
	author_email="xxkraaklxx@gmail.com",
	description="For when you're feeling vulnerable, GPL-3.0-or-later",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/Krocodial/ceevee",
	packages=setuptools.find_packages(),
	classifiers=(
		"Programming Language :: Python :: 3.5",
		"License :: OSI approved :: BCgov License",
		"Operating System :: OS Independent",
	),
)
