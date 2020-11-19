# -*- coding: utf-8 -*-

import logging
import os

from . import controllers
from . import models

_logger = logging.getLogger(__name__)

directory = os.path.dirname(__file__)


def pre_init_hook(cr):
    path = os.path.join(directory, 'query/before')
    files = os.listdir(path)
    for file in files:
        path_query = os.path.join(path, file)
        query = open(path_query, 'r').read()
        cr.execute(query)
        message = 'Insert into table: '
        _logger.info(message + file)


def post_init_hook(cr, result):
    path = os.path.join(directory, 'query/after')
    files = os.listdir(path)
    sorted_files = sorted(files)
    for file in sorted_files:
        path_query = os.path.join(path, file)
        query = open(path_query, 'r').read()
        cr.execute(query)
        message = 'Insert into table: '
        _logger.warning(message + file)
