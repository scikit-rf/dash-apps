# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 14:57:14 2019

@author: ander906
"""
import sys
from os.path import join, dirname, abspath, basename, realpath
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

def isnotebook():
    '''
    Check if in jupyterlab environment.

    From https://stackoverflow.com/questions/15411967/how-can-i-check-if-code-is-executed-in-the-ipython-notebook
    '''
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter


in_jupyterlab = isnotebook()
hubzero = False
auth_on = True
flask_debug = False
for arg in sys.argv:  # Check if any hubzero runtime arguments were specified.
    if arg == 'hubzero':
        hubzero = True
    elif arg == 'noauth':
        auth_on = False
    elif arg == "debug":
        flask_debug = True
    else:
        continue
# Handle conditional imports for hubzero hosting
if hubzero:
    from hublib.util import check_access
    from hubzeroapp import app

    if auth_on: check_access(app)
elif in_jupyterlab:
    import jupyterlab_dash
    viewer = jupyterlab_dash.AppViewer()
    from app import app
else:
    from app import app

server = app.server

from apps import app_viewer

if flask_debug:
    from werkzeug.middleware.profiler import ProfilerMiddleware

changes = ''
with open(join(dirname(dirname(abspath(__file__))), 'CHANGELOG.md')) as f:
    changes = changes+f.read()

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    try:  # Need to take basename to handle nanohub proxy
        if basename(pathname):
            pathname=basename(pathname)
    except TypeError:  # On start of app, pathname will be NoneType, throwing error unless caught
        pass
    if pathname == 'app_viewer':
        return app_viewer.layout
    else:
        return html.Div([
            html.A(
                children=html.Img(src=app.get_asset_url('github2.svg')),
                href=r'https://github.com/JAnderson419/SNaP',
                style={'fill': r'#151513', 'color': r'#fff', 'position': 'absolute', 'top': 0, 'border': 0, 'right': 0}
            ),
            html.H1('SNaP SnP Utilities'),
            html.H3(children='by Jackson Anderson, ander906@purdue.edu'),
            html.Hr(),
            html.H5('Release Notes'),
            html.Div(
                dcc.Markdown(children=changes),
                style={'border': '2px solid #a3a3c2', 'background-color': r'#f0f0f5',
                       'height': r'10em', 'overflow': 'scroll', 'resize': 'both'}
            ),
            html.Hr(),
            dcc.Link('Go to SnP Viewer.', href='app_viewer'),
            html.A(
                children=html.Img(src=app.get_asset_url('powered_by_scikit-rf.svg')),
                href=r'http://scikit-rf.org',
                style={'position': 'absolute', 'bottom': 0, 'right': 0}
            ),
        ])


def main():
    if hubzero:
        app.run_server(port=8000, host='0.0.0.0')
    elif in_jupyterlab:
        viewer.show(app)
    else:
        if flask_debug:
            print(join(dirname(dirname(realpath(__file__))), 'debug'))
            app.server.config['PROFILE'] = True
            app.server.wsgi_app = ProfilerMiddleware(app.server.wsgi_app,
                                                     restrictions=[30],
                                                     profile_dir=join(dirname(dirname(realpath(__file__))), 'debug'))
            app.run_server(debug=False)
        else:
            app.run_server(debug=True)


if __name__ == '__main__':
    main()
