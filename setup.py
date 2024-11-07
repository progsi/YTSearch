from setuptools import setup

setup(
    name='ytsearch',
    version='0.1.0',
    description='A small tool to search YouTube using the official YouTube Data API.',
    url='https://github.com/progsi/YTSearch/tree/main',
    author='Simon Hachmeier',
    author_email='simon.hachmeier@hu-berlin.de',
    license='BSD 2-clause',
    packages=['ytsearch'],
    install_requires=['python>=3.7.16',
                      'pandas>=1.3.5',
                      'google-api-python-client>=2.151.0'
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux :: Ubuntu',
        'Programming Language :: Python :: 3.7',
        ],
)
