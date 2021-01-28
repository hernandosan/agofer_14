# -*- coding: utf-8 -*-

import logging
import os
from datetime import date, datetime

from . import controllers
from . import models

from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)
directory = os.path.dirname(__file__)

def pre_init_hook(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})
    vals = {
        'external_email_server_default': True, 
        'auth_signup_uninvited': 'b2b',
        'auth_oauth_google_enabled': True,
        'auth_oauth_google_client_id': '1007288078484-861d4rejr8bj3474h6fim0mdlhb0c0ms.apps.googleusercontent.com',
    }
    env['res.config.settings'].create(vals).set_values()
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
        _logger.warning('Table: %s, Progress: %s' % (file, round(i*100/total, 2)))
        with open(os.path.join(path, file), 'r') as query_file:
            cr.execute(query = query_file.read())
            cr.commit()
    end = datetime.now()
    time = start - end
    _logger.warning('Query after, End: %s, Time: %s' % (end, round(time.seconds/60, 2)))
