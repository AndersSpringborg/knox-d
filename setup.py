import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


def requirements():
    return [i.strip() for i in open("requirements.txt").readlines()]


setuptools.setup(
    name="knox-mi-graph",  # Replace with your own username
    version="1.0.2",
    author="Foersteholdet",
    author_email="sw514e20@cs.aau.dk",
    description="Knowledge graph builder",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.its.aau.dk/Knox/mi-graph",
    packages=setuptools.find_packages(),
    install_requires=requirements(),
    entry_points={"console_scripts": ['mi_graph=mi_graph:cli']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
# AAU schema
# https://repos.libdom.net/
