#!/usr/bin/env python
# python manage.py shell < populate_database.py

import os
import sys
import logging

logger = logging.getLogger('Populate database')
self.log = logger
self.log.info("START : loading data")

from api import tests
data = tests.InventoryCase()
data.setUp()

self.log.info("END : loading data")
