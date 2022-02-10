# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
from multiprocessing import Queue

values_python = [0, 0, 0]
top_words_python = ["", "", ""]

values_java = [0, 0, 0]
top_words_java = ["", "", ""]


def run_plotly_dash_app(msg_queue_python: Queue, msg_queue_java: Queue, debug=False):
    app = Dash()

    app.layout = html.Div(children=[
        html.H1(children='REACTANT'),
        # html.Div(children='Dash: A web application framework for your data.'),
        dcc.Graph(id='live-graph'),
        dcc.Interval(id='interval-component', interval=1000)
    ])

    @app.callback(Output('live-graph', 'figure'),
                  Input('interval-component', 'n_intervals'))
    def update_graph_live(n):
        global values_python
        global values_java
        global top_words_python
        global top_words_java
        print('got updated')

        if not msg_queue_python.empty():
            data_python: dict = msg_queue_python.get()
            print(data_python)
            data_sorted_python = dict(sorted(data_python.items(), key=lambda item: item[1], reverse=True))
            keys = list(data_sorted_python.keys())
            top_words_python = [keys[0], keys[1], keys[2]]
            values_python = [data_sorted_python[keys[0]], data_sorted_python[keys[1]], data_sorted_python[keys[2]]]

        if not msg_queue_java.empty():
            data_java: dict = msg_queue_java.get()
            print(data_java)
            data_sorted_java = dict(sorted(data_java.items(), key=lambda item: item[1], reverse=True))
            keys_java = list(data_sorted_java.keys())
            top_words_java = [keys_java[0], keys_java[1], keys_java[2]]
            values_java = [data_sorted_java[keys_java[0]], data_sorted_java[keys_java[1]], data_sorted_java[keys_java[2]]]


        # df = pd.DataFrame({
        #     "Top Names in Functions and Methods on GitHub": top_words_python,
        #     "Amount": values_python,
        # })

        # fig = px.bar(df, x="Top Names in Functions and Methods on GitHub", y="Amount")

        fig = make_subplots(rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.1)

        fig.add_trace(go.Bar(x=top_words_python, y=values_python), row=1, col=1)
        fig.add_trace(go.Bar(x=top_words_java, y=values_java), row=2, col=1)
        fig.update_layout(height=1000, width=1000, title_text="Stacked Subplots with Shared X-Axes")

        print('* return figure')
        return fig

    app.run_server(debug=debug)


if __name__ == '__main__':
    run_plotly_dash_app(None, None, debug=True)
