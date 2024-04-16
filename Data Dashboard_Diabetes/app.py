import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Lire le fichier Excel
data = pd.read_excel("Excel_Projet.xlsx")

# Mettre les pays en ordre alphabetique
sorted_countries = sorted(data["Pays"])

# Ressortir la tendance mondial
Tendance_Mondial = data[data["Pays"] == "Tendance mondial"]

# Cree l'application
app = dash.Dash(__name__)
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

# Mise en page
app.layout = html.Div([
    html.Link(
        rel="shortcut icon",
        href="/assets/Earth_1.jpg"
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
            html.H2("Calculer la Prevalence au Diabète", style={"textAlign": "center"}),
            html.Div([
                html.Label("PIB du pays (B$US):"),
                dcc.Input(id="pib-input", type="number", value=0,
                          style={"backgroundColor": colors["button-background"], "color": colors["button-text"],
                                 "border": f"2px solid {colors['border']}", "margin": "5px"})
            ]),
            html.Div([
                html.Label("Âge médian (années):"),
                dcc.Input(id="age-input", type="number", value=0,
                          style={"backgroundColor": colors["button-background"], "color": colors["button-text"],
                                 "border": f"2px solid {colors['border']}", "margin": "5px"})
            ]),
            html.Div([
                html.Label("% d'obésité (IMC > 30):"),
                dcc.Input(id="obesity-input", type="number", value=0,
                          style={"backgroundColor": colors["button-background"], "color": colors["button-text"],
                                 "border": f"2px solid {colors['border']}", "margin": "5px"})
            ]),
            html.Div([
                html.Label("Nombre d'heures de travail/sem:"),
                dcc.Input(id="hours-input", type="number", value=0,
                          style={"backgroundColor": colors["button-background"], "color": colors["button-text"],
                                 "border": f"2px solid {colors['border']}", "margin": "5px"})
            ]),
            html.Div([
                html.Label("Rapport Homme/Femme:"),
                dcc.Input(id="gender-ratio-input", type="number", value=0,
                          style={"backgroundColor": colors["button-background"], "color": colors["button-text"],
                                 "border": f"2px solid {colors['border']}", "margin": "5px"})
            ]),
            html.Button("Calculate Prevalence", id="calculate-button",
                        style={"backgroundColor": colors["button-background"],
                               "color": colors["button-text"],
                               "border": f"2px solid {colors['border']}",
                               "margin": "20px"}),
            html.Div(id="prevalence-output", style={"textAlign": "center", "margin": "20px"})
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

    return html.H4(f"Prevalence au Diabète: {prevalence:.2f}%", style={"color": colors["text"]})


if __name__ == "__main__":
    app.run_server(debug=True)

           
