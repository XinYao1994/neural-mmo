from itertools import chain

from setuptools import find_packages, setup

REPO_URL = "https://github.com/neuralmmo/environment"

extra = {
    'docs': [
        'sphinx-rtd-theme==0.5.1',
        'sphinxcontrib-youtube==1.0.1',
        'myst-parser==1.0.0',
        'sphinx-rtd-theme==0.5.1',
        'sphinx_design==0.4.1',
    ],
}

extra['all'] = list(set(chain.from_iterable(extra.values())))
 
setup(
    name="nmmo",
    description="Neural MMO is a platform for multiagent intelligence research inspired by "
    "Massively Multiplayer Online (MMO) role-playing games. Documentation hosted at neuralmmo.github.io.",
    long_description_content_type="text/markdown",
    version=open('nmmo/version.py').read().split()[-1].strip("'"),
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy==1.23.3',
        'scipy==1.10.0',
        'pytest==7.3.0',
        'pytest-benchmark==3.4.1',
        'fire==0.4.0',
        'autobahn==19.3.3',
        'Twisted==19.2.0',
        'vec-noise==1.1.4',
        'imageio==2.23.0',
        'tqdm==4.61.1',
        'h5py==3.7.0',
        'pettingzoo==1.19.0',
        'gym==0.23.0',
        'pylint==2.16.0',
        'py==1.11.0'
    ],
    extras_require=extra,
    python_requires=">=3.7",
    license="MIT",
    author="Joseph Suarez",
    author_email="jsuarez@mit.edu",
    url=REPO_URL,
    keywords=["Neural MMO", "MMO"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)

