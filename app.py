import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from dash import dash_table
from dict_Excel import*

# Lire le fichier Excel
data = pd.read_excel("Excel_Projet.xlsx")

# Mettre les pays en ordre alphabetique
sorted_countries = sorted(data["Pays"])

# Ressortir la tendance mondial
Tendance_Mondial = data[data["Pays"] == "Tendance mondial"]

# Cree l'application
app = dash.Dash(__name__,
                suppress_callback_exceptions=True
                )
app.title = "Statistique Diabète"

favicon = "Earth_1.jpg.jpg"

# Couleurs et style
colors = {
    "background": "#f0f0f0",  
    "text": "#000000",  
    "button-background": "#00FFFF",  
    "button-text": "#000000",  
    "border": "#000000"  
}

data_stats1 = {
    'Variable': ['const', 'PIB du pays (B$US)', 'Âge médian (années)', '% d\'bésité (IMC > 30)', 
                 'Nombre d\'heures de travail/sem', 'Rapport Homme/Femme'],
    'coeff': [-12.7697, 1.628e-05, 0.0246, 0.1876, 0.3288, 3.1115],
    'std err': [14.432, 4.59e-05, 0.069, 0.060, 0.081, 11.790],
    'P > |t|': [0.382, 0.725, 0.724, 0.003, 0.000, 0.793]
}

data_stats2 = {
    'Variable': ['const', '% d\'bésité (IMC > 30)', 'Nombre d\'heures de travail/sem'],
    'coeff': [-8.1019, 0.1809, 0.3158],
    'std err': [2.677, 0.056, 0.071],
    'P > |t|': [0.004, 0.003, 0.000]
}

data_stats3 = {
    'Variable': ['const', 'PIB du pays (B$US)', 'Âge médian (années)', '% d\'bésité (IMC > 30)', 
                 'Nombre d\'heures de travail/sem', 'Rapport Homme/Femme'],
    'coeff': [-8.6689, -2.332e-05, 0.1927, 0.0210, 0.1703, 0.3537],
    'std err': [22.686, 3.87e-05, 0.192, 0.183, 0.134, 13.087],
    'P > |t|': [0.707, 0.554, 0.329, 0.909, 0.219, 0.979]
}

df1 = pd.DataFrame(data_stats1)
df2 = pd.DataFrame(data_stats2)
df3 = pd.DataFrame(data_stats3)

# Mise en page
app.layout = html.Div([
    html.Link(
        rel="shortcut icon",
        href="Earth_1.jpg.jpg"
    ),
    html.Div(style={"backgroundColor": colors["background"], "color": colors["text"]}, children=[
        html.H1("Statistique Diabète", style={"textAlign": "center", "margin": "20px"}),
        html.Div([
            dcc.Dropdown(
                id="pays-dropdown",
                options=[{"label": pays, "value": pays} for pays in sorted_countries],
                value=sorted_countries[0],
                style={"width": "50%", "margin": "auto", "backgroundColor": colors["button-background"],
                       "color": colors["button-text"], "border": f"2px solid {colors['border']}"}
            )
        ]),
        html.Div(id="bar-charts", style={"display": "flex", "flexWrap": "wrap", "justifyContent": "center"}),
        html.Div([
            html.H2("Calculer la Prévalence au Diabète", style={"textAlign": "center"}),
            html.Div([
                html.Div([
                    html.Label("PIB du pays (B$US):", style={"text-align": "center"}),
                    dcc.Input(id="pib-input", type="number", value=15,
                            style={"backgroundColor": colors["button-background"], "color": colors["button-text"],
                                    "border": f"2px solid {colors['border']}", "margin": "5px", "vertical-align" : "center"})
                ]),
                html.Div([
                    html.Label("Âge médian (années):"),
                    dcc.Input(id="age-input", type="number", value=38,
                            style={"backgroundColor": colors["button-background"], "color": colors["button-text"],
                                    "border": f"2px solid {colors['border']}", "margin": "5px"},)
                ]),
                html.Div([
                    html.Label("% d'obésité (IMC > 30):"),
                    dcc.Input(id="obesity-input", type="number", value=20,
                            style={"backgroundColor": colors["button-background"], "color": colors["button-text"],
                                    "border": f"2px solid {colors['border']}", "margin": "5px"})
                ]),
                html.Div([
                    html.Label("Nombre d'heures de travail/sem:"),
                    dcc.Input(id="hours-input", type="number", value=34,
                            style={"backgroundColor": colors["button-background"], "color": colors["button-text"],
                                    "border": f"2px solid {colors['border']}", "margin": "5px"})
                ]),
                html.Div([
                    html.Label("Rapport Homme/Femme:"),
                    dcc.Input(id="gender-ratio-input", type="number", value=0.9,
                            style={"backgroundColor": colors["button-background"], "color": colors["button-text"],
                                    "border": f"2px solid {colors['border']}", "margin": "5px"})
                ]),
            ], style={"display": "flex", "flexWrap": "wrap", "justifyContent": "center"}),
            html.Button("Calculer la Prévalence", id="calculate-button",
            style={"backgroundColor": colors["button-background"],
                   "color": colors["button-text"],
                   "border": f"2px solid {colors['border']}",
                   "margin": "20px auto",
                   "display": "block"}),
            html.Div(id="prevalence-output", style={"textAlign": "center", "margin": "20px", "font-size": "65px"}),
            html.Div(id="statistique-output", style={"textAlign": "center", "margin": "20px"}),
            dcc.Input(id="dummy-input", type="hidden", value=""),
            html.H2("Statistique Diabète Avant Ajustement", style={"textAlign": "center"}),
                dash_table.DataTable(
                    id='table1',
                    columns=[{'name': i, 'id': i} for i in df1.columns],
                    data=df1.to_dict('records'),
                    style_table={'overflowX': 'auto'},
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold'
                    },
                    style_cell={
                        'textAlign': 'left',
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                    },
                ),
                html.H2("Statistique Diabète Premier Ajustement", style={"textAlign": "center"}),
                dash_table.DataTable(
                    id='table2',
                    columns=[{'name': i, 'id': i} for i in df2.columns],
                    data=df2.to_dict('records'),
                    style_table={'overflowX': 'auto'},
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold'
                    },
                    style_cell={
                        'textAlign': 'left',
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                    },
                ),
                html.H2("Statistique Diabète Deuxième Ajustement", style={"textAlign": "center"}),
                dash_table.DataTable(
                    id='table3',
                    columns=[{'name': i, 'id': i} for i in df3.columns],
                    data=df3.to_dict('records'),
                    style_table={'overflowX': 'auto'},
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold'
                    },
                    style_cell={
                        'textAlign': 'left',
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                    },
                ),
            html.Div(html.H3("Franck Fongang"), id="name-output", style={"textAlign": "center", "margin": "20px"}),
        ])
    ])
])

# Dropdown pour selectionnner un pays
@app.callback(
    Output("bar-charts", "children"),
    [Input("pays-dropdown", "value")]
)
def update_bar_charts(selected_pays):
    selected_data = data[data['Pays'] == selected_pays]
    bar_charts = []

    # Graphique pour chaque variable
    for idx, col in enumerate(data.columns[1:]):
        fig = px.bar(x=[selected_pays, "Tendance Mondial"],
                     y=[selected_data[col].iloc[0], Tendance_Mondial[col].iloc[0]],
                     color=[selected_pays, "Tendance Mondial"],
                     labels={"x": "", "y": col},
                     title=f"{col} ({selected_pays})",
                     color_discrete_map={selected_pays: '#FFD700', "Tendance Mondial": '#7FFF00'})
        fig.update_layout(plot_bgcolor=colors["background"], paper_bgcolor=colors["background"],
                          height=300, width=400)
        
        if idx % 2 == 0:
            fig.update_traces(marker_line_color="black", marker_line_width=2, opacity=0.8)
        else:         fig.update_traces(marker_line_color="black", marker_line_width=2, opacity=0.8)
        bar_charts.append(html.Div(dcc.Graph(figure=fig, config={"displayModeBar": False}),
                                    style={"margin": "10px", "border": f"2px solid {colors['border']}",
                                           "borderRadius": "10px", "boxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2)",
                                           "transition": "0.3s"}))

    return bar_charts

# @app.callback(
#     Output("statistique-output", "children"),
#     [dash.dependencies.Input("dummy-input", "value")] 
# )
# def update_statistique_output(value):
#     try:
#         con = data.copy() 
#         con.rename(columns={"Unnamed: 0": "Pays"}, inplace=True)
#         Y = con["Prévalence au diabète (%)"]
#         x = con[
#             ["PIB du pays (B$US)",
#              "Âge médian (années)",
#              "% d'bésité (IMC > 30)",
#              "Nombre d'heures de travail/sem",
#              "Rapport Homme/Femme", ]
#         ]
#         X = sm.add_constant(x)
#         ks = sm.OLS(Y, X)
#         ks_res = ks.fit()
#         p_value = ks_res.summary()

#         p_value_html = p_value.tables[1].as_html()

#         return html.Div([html.Table([html.Tr([html.Th(col) for col in p_value.tables[1].columns])] +
#                                      [html.Tr([html.Td(val) for val in row]) for row in p_value.tables[1].data])])
#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return html.Pre(f"Error: {str(e)}")


# Calculer la prevalence avec la formule
@app.callback(
    Output("prevalence-output", "children"),
    [Input("calculate-button", "n_clicks")],
    [dash.dependencies.State("pib-input", "value"),
     dash.dependencies.State("age-input", "value"),
     dash.dependencies.State("obesity-input", "value"),
     dash.dependencies.State("hours-input", "value"),
     dash.dependencies.State("gender-ratio-input", "value")]
)
def calculate_prevalence(n_clicks, pib, age, obesity, hours, ratio):
    if n_clicks is None:
        return ""

    # Appliquer la formule au valeur entree
    intercept = -9.880215805
    x_pib = 1.83718E-05
    x_age = 0.00562842
    x_obesity = 0.184466083
    x_hours = 0.32044396
    x_gender_ratio = 1.297924562

    prevalence = intercept + x_pib * pib + x_age * age + x_obesity * obesity + x_hours * hours + x_gender_ratio * ratio
    if prevalence >= 100:
        return html.H3("Prévalence au Diabète:100%")
    elif prevalence <= 0:
        return html.H3("Prévalence au Diabète: 0%")
    else:
        return html.H3(f"Prévalence au Diabète: {prevalence:.2f}%", style={"color": colors["text"]})



if __name__ == "__main__":
    app.run_server(debug=False)

           
