#!/usr/bin/env python
# python manage.py shell < populate_database.py

import os
import sys

from api import tests
data = tests.InventoryCase()
data.setUp()
