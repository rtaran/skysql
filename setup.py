from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="flight-data-api",
    version="0.1.0",
    author="Flight Data API Contributors",
    author_email="example@example.com",
    description="A platform for accessing and visualizing flight delay data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/flight-data-api",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "flight-cli=main:main",
            "flight-api=api:app.run",
        ],
    },
)