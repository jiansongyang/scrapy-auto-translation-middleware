import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scrapy-auto-translation-middleware",
    version="0.0.7",
    author="Jiansong Yang",
    author_email="yangjiansong@gmail.com",
    description="A Scrapy spider-middleware that performs automatic translation when the spider is working",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jiansongyang/scrapy-auto-translation-middleware",
    license='MIT',
    packages=setuptools.find_packages(exclude=('examples',)),
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

