# inventree-cups-plugin

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![CI](https://github.com/wolflu05/inventree-cups-plugin/actions/workflows/ci.yml/badge.svg)

A label printing plugin for [InvenTree](https://inventree.org), which provides support for [Cups label printing servers](https://www.cups.org). If your printer is not cups compatible, you can setup a cups printing server. This [article](https://nerdig.es/labelwriter-im-netz-teil1/) describes how to setup a cups printing server for the DYMO LabelWriter 450 Duo.

## Installation

> :warning: This plugin needs `cups-devel` installed to install its dependencies. You can read more about the requirements at [`pycups`](https://github.com/OpenPrinting/pycups). If you're using `apt` as a package manager run `apt install libcups2-dev` before.

Install this plugin as follows:

```bash
pip install git+https://github.com/wolflu05/inventree-cups-plugin
```

Or, add to your `plugins.txt` file:

```txt
git+https://github.com/wolflu05/inventree-cups-plugin
```
 
## Configuration Options

| Name| Description| Example |
| --- | --- | --- |
| Server | IP/Hostname to connect to the cups server | `192.168.1.5` |
| Port | Port to connect to the cups server | `631` | 
| Benutzer | User to connect to the cups server	| *can also be empty* |
| Passwort | Password to connect to the cups server	| *can also be empty* |
| Printer | Printer from cups server, can be selected if valid connection options are saved in | `myprinter` |
