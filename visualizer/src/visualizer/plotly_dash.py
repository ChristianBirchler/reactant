from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from multiprocessing import Queue

N = 3

values_python = [0, 0, 0]
top_words_python = ["", "", ""]

values_java = [0, 0, 0]
top_words_java = ["", "", ""]


def get_top_words(data, n):
    data_sorted = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))
    keys = list(data_sorted.keys())
    words = keys[:n]
    values = [data_sorted[key] for key in words]
    return words, values


def get_figure(x1, y1, x2, y2):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.1)
    fig.add_trace(go.Bar(x=x1, y=y1, name='Python'), row=1, col=1)
    fig.add_trace(go.Bar(x=x2, y=y2, name='Java'), row=2, col=1)
    fig.update_layout(height=1000, width=1000,
                      title_text="Popular words in function/method names of Java and Python repositories on GitHub")
    return fig


def run_plotly_dash_app(msg_queue_python: Queue, msg_queue_java: Queue, debug=False):
    app = Dash()

    app.layout = html.Div(children=[
        html.H1(children='REACTANT'),
        # html.Div(children='Dash: A web application framework for your data.'),
        dcc.Input(id='input', value=3, type='number'),
        dcc.Graph(id='live-graph'),
        dcc.Interval(id='interval-component', interval=1000)
    ])

    @app.callback(Output('live-graph', 'figure'),
                  Input('interval-component', 'n_intervals'),
                  Input('input', 'value'))
    def update_graph_live(_, n_words):
        global values_python
        global values_java
        global top_words_python
        global top_words_java
        print('got updated')
        print(n_words)

        if not msg_queue_python.empty():
            data_python: dict = msg_queue_python.get()
            top_words_python, values_python = get_top_words(data_python, n_words)
            print(data_python)

        if not msg_queue_java.empty():
            data_java: dict = msg_queue_java.get()
            top_words_java, values_java = get_top_words(data_java, n_words)
            print(data_java)

        fig = get_figure(top_words_python, values_python, top_words_java, values_java)

        print('* return figure')
        return fig

    app.run_server(debug=debug)


if __name__ == '__main__':
    run_plotly_dash_app(None, None, debug=True)
