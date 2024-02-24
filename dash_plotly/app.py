from dash import Dash, html, dash_table, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc

external_stylesheets = [dmc.theme.DEFAULT_COLORS]
app = Dash(__name__, external_stylesheets=external_stylesheets)

def get_year(date):
    return int(date[-4:])

df = pd.read_csv("df_lang.csv")
df["Date"] = df["Date"].astype(str)
df["Year"] = df["Date"].apply(get_year)

app.layout = html.Div([
    html.Div(children='Выберите промежуток времени'),
    dcc.RangeSlider(min=2004, max=2023, marks={i: '{}'.format(i) for i in range(2004,2024,1)}, step=1, value=[2004, 2023], id='range'),
    html.Div(children='Выберите языки программирования'),
    dcc.Dropdown(df.columns[1:],
    ["Python"],
    multi=True,
    id="choice"
    ),
    dcc.Graph(figure={}, id="lang")
])

@callback(
    Output('lang', 'figure'),
    [Input('range', 'value'), 
    Input('choice', 'value')]
    )
def update_graph(range_chosen, col_chosen):
    fig = px.line(df[(df.Year >= range_chosen[0]) & (df.Year <= range_chosen[1])], x='Date', y=col_chosen, height=700)
    fig.update_layout(xaxis_title="Дата", yaxis_title="Доля запросов туториалов по языку от всех запросов туториалов",
                    title="Динамика популярности языков программирования",
                    legend=dict(
                        title="Языки"
))
    fig.layout.yaxis.ticksuffix = '%'
    return fig

if __name__ == '__main__':
    app.run(debug=True) 