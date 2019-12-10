#!/usr/bin/env python
# python manage.py shell < populate_database.py

import os
import sys
import logging

logger = logging.getLogger('Populate database')
log = logger
log.info("START : loading data")

from api import tests
data = tests.InventoryCase()
data.setUp()

log.info("END : loading data")
