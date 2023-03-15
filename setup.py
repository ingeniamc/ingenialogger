import re
import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('ingenialogger/__init__.py') as f:
    __version = re.search(r'__version__\s+=\s+"(.*)"', f.read())[1]


def get_docs_url():
    return f"https://distext.ingeniamc.com/doc/ingenialogger/{__version}"


setuptools.setup(
    name="ingenialogger",
    version=__version,
    packages=setuptools.find_packages(),
    author="Ingenia Motion Control",
    author_email="support@ingeniamc.com",
    description="Logger library for Ingenia projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://www.ingeniamc.com',
    project_urls={
                "Documentation": get_docs_url(),
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    python_requires='>=3.6',
)
