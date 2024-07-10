"""This package provides a cups printer driver."""

import cups
from tempfile import NamedTemporaryFile

from django.db import models
from django.utils.translation import gettext_lazy as _

# InvenTree imports
from report.models import LabelTemplate
from plugin import InvenTreePlugin
from plugin.machine import BaseMachineType
from plugin.machine.machine_types import LabelPrinterBaseDriver, LabelPrinterMachine

from inventree_cups.version import CUPS_PLUGIN_VERSION


class CupsLabelPlugin(InvenTreePlugin):
    """Cups label printer driver plugin for InvenTree."""

    AUTHOR = "wolflu05"
    DESCRIPTION = "Label printer plugin for CUPS server"
    VERSION = CUPS_PLUGIN_VERSION

    # Machine registry was added in InvenTree 0.14.0, use inventree-cups-plugin 0.1.0 for older versions
    # Machine driver interface was fixed with 0.16.0 to work inside of inventree workers
    MIN_VERSION = "0.16.0"

    NAME = "CupsLabelPrinterDriver"
    SLUG = "cups-driver"
    TITLE = "Cups Label Printer Driver"


class CupsLabelPrinterDriver(LabelPrinterBaseDriver):
    """Cups label printing driver for InvenTree."""

    SLUG = "cups-driver"
    NAME = "Cups Driver"
    DESCRIPTION = "Cups label printing driver for InvenTree"

    def __init__(self, *args, **kwargs):
        """Initialize the CupsLabelPrinterDriver."""
        self.MACHINE_SETTINGS = {
            'SERVER': {
                'name': _('Server'),
                'description': _('IP/Hostname to connect to the cups server'),
                'default': 'localhost',
                'required': True,
            },
            'PORT': {
                'name': _('Port'),
                'description': _('Port to connect to the cups server'),
                'validator': int,
                'default': 631,
                'required': True,
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
                'protected': True,
            },
            'PRINTER': {
                'name': _('Printer'),
                'description': _('Printer from cups server'),
                'choices': self.get_printer_choices,
                'required': True,
            },
        }

        super().__init__(*args, **kwargs)

    def init_machine(self, machine: BaseMachineType):
        """Machine initialize hook."""
        if self.get_connection(machine) is None:
            machine.handle_error(_("Cannot connect to cups server"))

    def get_printer_choices(self, **kwargs):
        """Get printer choices from cups server."""
        conn = self.get_connection(kwargs['machine_config'].machine)

        if conn:
            return [(dev_id, dev['printer-info'] or dev_id) for dev_id, dev in conn.getPrinters().items()]
        return [("", _("Error scanning for printers"))]

    def get_connection(self, machine: LabelPrinterMachine):
        """Get connection to cups server."""
        cups.setServer(machine.get_setting('SERVER', 'D'))
        cups.setPort(machine.get_setting('PORT', 'D'))
        cups.setUser(machine.get_setting('USER', 'D'))
        cups.setPasswordCB(lambda: machine.get_setting('PASSWORD', 'D'))

        try:
            return cups.Connection()
        except Exception:
            return None

    def print_label(self, machine: LabelPrinterMachine, label: LabelTemplate, item: models.Model, **kwargs) -> None:
        """Print label using cups server."""
        machine.set_status(LabelPrinterMachine.MACHINE_STATUS.UNKNOWN)
        conn = self.get_connection(machine)

        if conn is None:
            machine.handle_error(_('Cannot get connection to printer'))
            machine.set_status(LabelPrinterMachine.MACHINE_STATUS.DISCONNECTED)
            return

        pdf_data = self.render_to_pdf_data(label, item)

        with NamedTemporaryFile(suffix='.pdf') as f:
            f.write(pdf_data)
            f.flush()

            try:
                for copy_idx in range(kwargs.get('printing_options', {}).get('copies', 1)):
                    conn.printFile(
                        machine.get_setting('PRINTER', 'D'),
                        f.name,
                        f'{label.name}-{item.pk}-{copy_idx}.pdf',
                        {},
                    )
            except Exception as e:
                machine.set_status(LabelPrinterMachine.MACHINE_STATUS.DISCONNECTED)
                machine.handle_error(_('Error printing label') + f': {e}')
