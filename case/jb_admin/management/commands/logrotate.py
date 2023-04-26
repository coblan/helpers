
from django.core.management.base import BaseCommand
from django.conf import settings
import os
from django.utils import timezone
import logging
from django.utils import timezone

general_log = logging.getLogger('general_log')
import invoke
import os
from helpers.func.stdout_process import Capturing

class Command(BaseCommand):
    """
    """
    def handle(self, *args, **options):
        capturing = Capturing()
        def on_read(line):
            general_log.debug(f'外部logrotate: {line}')
        capturing.on_readline(on_read)
        base_url = os.path.dirname( settings.BASE_DIR )
        log_conf = os.path.join(base_url,'deploy','logrotate.conf')
        capturing.start()
        invoke.run(f'chmod 600 {log_conf}')
        invoke.run(f'chown root {log_conf}')
        invoke.run(f'logrotate -fd {log_conf}')
        capturing.stop()
        general_log.info('logstate结束')