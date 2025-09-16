# -*- coding: utf-8 -*-

import setuptools
import importlib
import os

module_path = os.path.join(os.path.dirname(__file__), "inventree_cups", "__init__.py")
spec = importlib.util.spec_from_file_location("inventree_cups", module_path)
inventree_cups = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inventree_cups)


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setuptools.setup(
    name="inventree-cups-plugin",

    version=inventree_cups.PLUGIN_VERSION,

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

    python_requires=">=3.9",

    entry_points={
        "inventree_plugins": [
            "CupsLabelPlugin = inventree_cups.cups_plugin:CupsLabelPlugin"
        ]
    },
)
