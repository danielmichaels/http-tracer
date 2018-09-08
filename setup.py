"""
Publish a new version:
$ git tag X.Y.Z -m "Release X.Y.Z"
$ git push --tags
$ pip install --upgrade twine wheel
$ python setup.py sdist bdist_wheel
$ twine upload --repository-url https://test.pypi.org/legacy/ dist/*
    // ABOVE ONLY FOR TESTING
$ twine upload -r pypi dist/*
"""

from setuptools import setup, find_packages

NAME = 'http-tracer'
VERSION = '18.8.1'
DESCRIPTION = "A simple script that follows redirects and returns their " \
              "headers, cookies and url's along its path."
URL = 'https://github.com/danielmichaels/http-tracer'
DOWNLOAD_URL = (URL + '/tarball/' + VERSION)
AUTHOR = 'Daniel Michaels'
AUTHOR_EMAIL = 'dans.address@outlook.com'
REQUIRES_PYTHON = '>= Python 3.6'

# Include what dependencies it requires:
REQUIRED = [
    'requests',
    'click',
    'colorama'
]

entry_points = {
    'console_scripts': [
        ['http-tracer = main:main']
    ]
}

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    download_url=DOWNLOAD_URL,
    install_requires=REQUIRED,
    entry_points=entry_points,
    include_package_data=True,
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6'
    ]
)
