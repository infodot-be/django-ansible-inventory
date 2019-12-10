#!/usr/bin/env python
# python manage.py shell < populate_database.py

import os
import sys
import logging
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE','inventory.settings')
# Import settings
django.setup()

from django.conf import settings
from django.db import IntegrityError
from api import tests


logger = logging.getLogger('Populate database')
log = logger
log.info("START : loading data")




data = tests.InventoryCase()
data.setUp()

log.info("END : loading data")
