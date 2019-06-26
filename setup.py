from setuptools import setup

import normalizer


setup(
    name='dolphin-normalizer',
    author='Jean-Philippe Hautin',
    description="a small utility to normalize gamecube iso files to be runnable by nintendont or dolphin",
    long_description=open('README.md').read(),
    install_requires=['requests'],
    license='GLPv3',
    packages=['normalizer'],
    platforms='ALL',
    url='https://github.com/jphautin/dolphin-normalizer',
    version=normalizer.__version__,
    entry_points = {
        'console_scripts': [
            'dolphin-normalizer = normalizer:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "License :: GLPv3",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Games",
    ],
)
