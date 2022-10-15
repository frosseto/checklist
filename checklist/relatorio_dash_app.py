from dash import dcc
from dash import html
from dash import dash_table as dt
from dash.dependencies import Input, Output
import plotly.express as px
from django_plotly_dash import DjangoDash

from django.db import connection
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('Relatorio', external_stylesheets=external_stylesheets)

#df = pd.read_csv('https://git.io/Juf1t')
query='SELECT * FROM public."ListaVerificacaoResultadoAnalise"'
df = pd.DataFrame() # pd.read_sql_query(query, connection)

resultado_query='''
SELECT resultado_analise."Resposta", resultado_analise."Modelo", COUNT(*) AS "Qde" 
FROM public."ListaVerificacaoResultadoAnalise" AS resultado_analise
GROUP BY resultado_analise."Resposta",resultado_analise."Modelo"
'''
resultado_df =   pd.DataFrame() #pd.read_sql_query(resultado_query, connection)

status_query= '''
 SELECT lista_analise."Status"
 ,lista_analise."Modelo" 
 ,COUNT(*) AS "Qde"
 FROM public."ListaVerificacaoResultadoAnalise" lista_analise
 GROUP BY lista_analise."Modelo", lista_analise."Status"
'''
status_df = pd.DataFrame() # pd.read_sql_query(status_query, connection)

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
                id="modelo-select",
                options=[
                    {'label': 'Encerramento de OMs', 'value': 'Encerramento de OMs'},
                    {'label': 'Rotas', 'value': 'Rotas'},
                ],
                value='Encerramento de OMs'
                ),       
        html.Div([
            html.Div([
                html.H6('Qde por Resultado'),                
                dcc.Graph(id='resultado-graph'),

            ], className="six columns"),

            html.Div([
                html.H6('Qde por Status'),
                dcc.Graph(id='status-graph'),
            ], className="six columns"),
        ], className="row"),
        html.H6('Resultados por Lista de Verificação'),
        dt.DataTable(
        id='tbl', data=df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.columns],
        style_cell={'textAlign': 'left'},
    ),


    ]),
    
])


@app.callback(
    Output('resultado-graph', 'figure'),
    Input('modelo-select', 'value'))
def update_figure(modelo):
    fig = px.bar(resultado_df.loc[resultado_df['Modelo'] == modelo], x="Resposta", y="Qde")
    fig.update_layout(transition_duration=500)
    return fig


@app.callback(
    Output('status-graph', 'figure'),
    Input('modelo-select', 'value'))
def update_figure(modelo):
    fig = px.bar(status_df.loc[status_df['Modelo'] == modelo], x="Status", y="Qde")
    fig.update_layout(transition_duration=500)
    return fig
