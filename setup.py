import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("src/win32_setctime/__init__.py", "r") as file:
    regex_version = r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]'
    version = re.search(regex_version, file.read(), re.MULTILINE).group(1)

with open("README.md", "rb") as file:
    readme = file.read().decode("utf-8")

setup(
    name="win32_setctime",
    version=version,
    packages=["win32_setctime"],
    package_dir={"": "src"},
    package_data={"win32_setctime": ["py.typed"]},
    description="A small Python utility to set file creation time on Windows",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Delgan",
    author_email="delgan.py@gmail.com",
    url="https://github.com/Delgan/win32-setctime",
    download_url="https://github.com/Delgan/win32-setctime/archive/{}.tar.gz".format(version),
    keywords=["win32", "windows", "filesystem", "filetime"],
    license="MIT license",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: System :: Filesystems",
        "Intended Audience :: Developers",
        "Environment :: Win32 (MS Windows)",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    extras_require={
        "dev": [
            "black>=19.3b0 ; python_version>='3.6'",
            "pytest>=4.6.2",
        ]
    },
    python_requires=">=3.5",
)
