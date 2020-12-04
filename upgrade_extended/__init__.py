# -*- coding: utf-8 -*-

import logging
import os
from datetime import date, datetime

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
    # PSQL
    path = os.path.join(directory, 'querys/after')
    total = len(os.listdir(path))
    start = datetime.now()
    _logger.warning('Query after, Total: %s, Start: %s' % (total, start))
    for i, file in enumerate(sorted(os.listdir(path))):
        _logger.warning('Table: %s, Progress: %s' % (file, round(i*100/total,2)))
        with open(os.path.join(path, file), 'r') as query_file:
            cr.execute(query = query_file.read())
    end = datetime.now()
    time = start - end
    _logger.warning('Query after, End: %s, Time: %s' % (end, round(time.seconds/60, 2)))
