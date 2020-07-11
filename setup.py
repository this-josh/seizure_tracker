from setuptools import setup, find_packages



with open("readme.md", "r") as fh:
    long_description = fh.read()

setup(
    name="seizure_tracker", # Replace with your own username
    version="0.0.1",
    author="Josh Kirk",
    author_email="jarkirk[at]pm.me",
    description="An application to track seizures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/this-josh/seizure_tracker",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)