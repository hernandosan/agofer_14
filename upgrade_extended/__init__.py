# -*- coding: utf-8 -*-

import logging
import os

from . import controllers
from . import models

_logger = logging.getLogger(__name__)

directory = os.path.dirname(__file__)

def pre_init_hook(cr):
    # _logger.warning("Cannot use '%s' as email alias, fallback to '%s'", alias_name, safe_alias_name)
    cr.execute()

def post_init_hook(cr, registry):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../views'))
    # open(os.path.join(directory, 'files', 'test_content.pdf'), 'rb') as file:
    cr.execute()
