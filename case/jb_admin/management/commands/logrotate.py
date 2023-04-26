
from django.core.management.base import BaseCommand
from django.conf import settings
import os
from django.utils import timezone
import logging
from django.utils import timezone

general_log = logging.getLogger('general_log')
import invoke
import os

class Command(BaseCommand):
    """
    """
    def handle(self, *args, **options):
        base_url = os.path.dirname( settings.BASE_DIR )
        log_conf = os.path.join(base_url,'deploy','logrotate.conf')
        invoke.run(f'logrotate -fd {log_conf}')
        general_log.info('logstate')