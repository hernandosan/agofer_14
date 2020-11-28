# -*- coding: utf-8 -*-

import logging
import os

from . import controllers
from . import models

_logger = logging.getLogger(__name__)

directory = os.path.dirname(__file__)


def pre_init_hook(cr):
    _logger.warning('Query before')
    path = os.path.join(directory, 'querys/before')
    for file in sorted(os.listdir(path)):
        with open(os.path.join(path, file), 'r') as query_file:
            cr.execute(query_file.read())

def post_init_hook(cr, result):
    _logger.warning('Query after')
    path = os.path.join(directory, 'querys/after')
    total = len(os.listdir(path))
    for i, file in enumerate(sorted(os.listdir(path))):
        _logger.warning('Query Table: ' + file + ', progress: ' + str(i/total))
        with open(os.path.join(path, file), 'r') as query_file:
            cr.execute(query = query_file.read())
