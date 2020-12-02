# -*- coding: utf-8 -*-

import logging
import os

from . import controllers
from . import models

_logger = logging.getLogger(__name__)
directory = os.path.dirname(__file__)


def pre_init_hook(cr):
    path = os.path.join(directory, 'querys/before')
    for file in sorted(os.listdir(path)):
        with open(os.path.join(path, file), 'r') as query_file:
            query = query_file.read()
            message = 'Insert into table: '
            _logger.info(message + file)
            cr.execute(query)


def post_init_hook(cr, result):
    path = os.path.join(directory, 'querys/after')
    for file in sorted(os.listdir(path)):
        with open(os.path.join(path, file), 'r') as query_file:
            query = query_file.read()
            message = 'Insert into table: '
            _logger.warning(message + file)
            cr.execute(query)
