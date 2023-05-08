import subprocess

from dash import Dash, dcc, html, Input, Output
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H1('Hello World'),
    dcc.Dropdown(['LA', 'NYC', 'MTL'],
                 'LA',
                 id='dropdown'
                 ),
    html.Div(id='display-value')
])


@app.callback(Output('display-value', 'children'),
              [Input('dropdown', 'value')])
def display_value(value):
    args = ("bin/linux/debug/executable")
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    return f'You have selected {value} - {output.decode()}'


if __name__ == '__main__':
    app.run_server(debug=True)
