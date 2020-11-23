# -*- coding: utf-8 -*-

import logging
import os

from . import controllers
from . import models

_logger = logging.getLogger(__name__)

directory = os.path.dirname(__file__)

def pre_init_hook(cr):
    # _logger.warning("Cannot use '%s' as email alias, fallback to '%s'", alias_name, safe_alias_name)
    query = open(os.path.join(directory, '/querys/before'), '1_before.sql', 'rb')
    cr.execute(query)

def post_init_hook(cr, registry):
    query = open(os.path.join(directory, '/querys/after'), '1_before.sql', 'rb').read()
    cr.execute()
