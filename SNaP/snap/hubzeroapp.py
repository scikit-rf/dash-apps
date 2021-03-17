# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 14:55:47 2019

@author: ander906
"""

import dash
# need these hubzero functions
from hublib.util import get_proxy_addr, check_access

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# # For hubzero, need to set the base path
app = dash.Dash(url_base_pathname=get_proxy_addr()[0], external_stylesheets=external_stylesheets)
# # Optional. Use hubzero authentication.
# check_access(app)


# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True