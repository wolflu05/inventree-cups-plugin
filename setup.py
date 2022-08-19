# -*- coding: utf-8 -*-

import setuptools

from inventree_cups.version import CUPS_PLUGIN_VERSION

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setuptools.setup(
    name="inventree-cups-plugin",

    version=CUPS_PLUGIN_VERSION,

    author="wolflu05",

    author_email="76838159+wolflu05@users.noreply.github.com",

    description="Cups label printer plugin for InvenTree",

    long_description=long_description,

    long_description_content_type='text/markdown',

    keywords="inventree cups",

    url="https://github.com/wolflu05/inventree-cups-plugin",

    license="MIT",

    packages=setuptools.find_packages(),

    install_requires=[
        "pycups"
    ],

    setup_requires=[
        "wheel",
        "twine",
    ],

    python_requires=">=3.6",

    entry_points={
        "inventree_plugins": [
            "CupsLabelPlugin = inventree_cups.cups_plugin:CupsLabelPlugin"
        ]
    },
)
