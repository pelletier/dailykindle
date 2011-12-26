from distutils.core import setup

setup(
    name = "dailykindle",
    version = "1.0.0",
    description = "Build MOBI documents out of news feeds.",
    url = "http://bitbucket.org/pelletier/dailykindle/",
    author = "Thomas Pelletier",
    author_email = "thomas@pelletier.im",
    packages = [
        "dailykindle",
    ],
    classifiers = [
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
    ],
)
