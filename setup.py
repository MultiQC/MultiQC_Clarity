#!/usr/bin/env python
"""
MultiQC_Clarity is a plugin for MultiQC, providing access to data held in 
the Illumina Genologics Clarity LIMS.

For more information about Clarity, see https://www.genologics.com/clarity-lims/
For more information about MultiQC, see http://multiqc.info
"""

from setuptools import setup, find_packages

version = '0.1'

setup(
    name = 'multiqc_clarity',
    version = version,
    author = 'Denis Moreno',
    author_email = 'denis.moreno@scilifelab.se',
    description = "MultiQC plugin for interacting with Illumina Genologics Clarity LIMS",
    long_description = __doc__,
    keywords = 'bioinformatics',
    url = 'https://github.com/Galithil/MultiQC_Clarity',
    license = 'MIT',
    packages = find_packages(),
    include_package_data = True,
    install_requires = [
        'genologics',
        'pyyaml'
    ],
    entry_points = {
        'multiqc.hooks.v1': [
                        'before_report_generation = multiqc_clarity.multiqc_clarity:MultiQC_clarity_metadata',
                        }
    },
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
)

