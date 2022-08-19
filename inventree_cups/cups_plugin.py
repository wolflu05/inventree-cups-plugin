"""Cups label printing plugin for InvenTree.

Supports direct printing of labels to networked label printers, using the pycups library.
"""

# Required libs
import cups
from tempfile import NamedTemporaryFile
from time import time

# translation
from django.utils.translation import ugettext_lazy as _

from inventree_cups.version import CUPS_PLUGIN_VERSION

# InvenTree plugin libs
from plugin import InvenTreePlugin
from plugin.mixins import LabelPrintingMixin, SettingsMixin


class CupsLabelPlugin(LabelPrintingMixin, SettingsMixin, InvenTreePlugin):
    AUTHOR = "wolflu05"
    DESCRIPTION = "Label printing plugin for CUPS server"
    VERSION = CUPS_PLUGIN_VERSION

    NAME = "CupsLabels"
    SLUG = "cups"
    TITLE = "Cups Label Printer"

    CONNECTION_INVALIDATION_TIME = 60

    def __init__(self, *args, **kwargs):
        self.SETTINGS = {
            'SERVER': {
                'name': _('Server'),
                'description': _('IP/Hostname to connect to the cups server'),
                'default': 'localhost',
            },
            'PORT': {
                'name': _('Port'),
                'description': _('Port to connect to the cups server'),
                'validator': int,
                'default': 631,
            },
            'USER': {
                'name': _('User'),
                'description': _('User to connect to the cups server'),
                'default': '',
            },
            'PASSWORD': {
                'name': _('Password'),
                'description': _('Password to connect to the cups server'),
                'default': '',
            },
            'PRINTER': {
                'name': _('Printer'),
                'description': _('Printer from cups server'),
                'choices': self.get_printer_choices,
                'default': '',
            },
        }

        self.connection = None

        super().__init__(*args, **kwargs)

    def get_printer_choices(self):
        conn = self.get_connection()

        if conn:
            return [(f"{dev}", f"{dev}") for dev in conn.getPrinters()]
        return [("", _("error scanning for printers"))]

    def serialize_connection(self):
        return "-".join(map(lambda x: str(self.get_setting(x)), ["SERVER", "PORT", "USER", "PASSWORD"]))

    def get_connection(self):
        if self.connection:
            conn = self.connection

            # check if conn is not older than CONNECTION_INVALIDATION_TIME and connection was initiated with same settings
            if time() - conn['initiation_time'] < self.CONNECTION_INVALIDATION_TIME and conn['key'] == self.serialize_connection():
                return conn['connection']

        key = self.serialize_connection()
        cups.setServer(self.get_setting('SERVER'))
        cups.setPort(self.get_setting('PORT'))
        cups.setUser(self.get_setting('USER'))
        cups.setPasswordCB(lambda: self.get_setting('PASSWORD'))

        try:
            conn = cups.Connection()

            self.connection = {
                'key': key,
                'initiation_time': time(),
                'connection': conn,
            }

            return self.connection['connection']

        except Exception:
            self.connection = None
            return None

    def print_label(self, **kwargs):
        """
        Send the label to the printer
        """

        conn = self.get_connection()

        if conn is None:
            raise Exception(_("Cannot get connection to printer"))

        f = NamedTemporaryFile()
        f.write(kwargs['pdf_data'])

        conn.printFile(self.get_setting('PRINTER'),
                       f.name, kwargs['filename'], {})

        f.close()
