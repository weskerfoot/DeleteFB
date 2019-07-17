import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="delete-facebook-posts",
    version="1.1.8",
    author="Wesley Kerfoot",
    author_email="wes@wesk.tech",
    description="A Selenium Script to Delete Facebook Posts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/weskerfoot/DeleteFB",
    packages=setuptools.find_packages(),
    include_package_data=True,
    requires_python=">=3.6",
    package_data={
        # Include *json files in the package:
        '': ['*.json'],
    },
    install_requires = [
        "selenium",
        "selenium-requests",
        "requests",
        "pybloom-live",
        "attrs"
    ],
    classifiers= [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        "console_scripts" : [
            "deletefb = deletefb.deletefb:run_delete"
        ]
    }
)
