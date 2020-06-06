import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scrapy-auto-translattion-middleware",
    version="1.0.1",
    author="Jiansong Yang",
    author_email="yangjiansong@gmail.com",
    description="A Scrapy spider-middleware that performs automatic translation when the spider is working",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/autotranslatemiddleware",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

