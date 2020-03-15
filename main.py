from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import requests
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import data_parse as dp
import plotly.graph_objects as go
import predictor as predictor
import os
import gunicorn


server = Flask(__name__)
admin_id = "admin"
admin_pw = "admin"

### Parse Data for Table ###############################################################################################
tabs = dp.table_for_vis()
## Columns ##
columns = tabs["columns"]
columns_for_table = []
for column in columns:
    columns_for_table.append(html.Th(column))

## Rows ##
rows = tabs["rows"]
rows_for_table = []
for column in columns:
    rows_for_table.append(html.Th(column))

## add organized columns into table ##
table_header = [
    html.Thead(html.Tr([
        columns_for_table
    ]))
]
for index, row in rows.iterrows():
    rows_for_table.append(html.Tr([html.Td(row["datetime"]),
                                   html.Td(row["season"]),
                                   html.Td(row["holiday"]),
                                   html.Td(row["workingday"]),
                                   html.Td(row["weather"]),
                                   html.Td(row["temp"]),
                                   html.Td(row["atemp"]),
                                   html.Td(row["humidity"]),
                                   html.Td(row["windspeed"]),
                                   html.Td(row["count"])
                                   ]))

## add organized columns into table ##
table_body = [html.Tbody(
    rows_for_table
)]

### Parse Data for Vis1 ################################################################################################
vis_count_by_date = dp.vis_count_by_date()
gofig = go.Figure()
date_count = gofig.add_trace(go.Scatter(x=vis_count_by_date["date"], y=vis_count_by_date["count"]))

### Parse Data for Vis2 ################################################################################################
visd2 = dp.vis_rel_count_temp()

### Parse Data for Vis3 ################################################################################################
heatfig = dp.vis_heatmap()


@server.route("/", method=['GET'])
@server.route("/login", methods=['GET'])
def index():
    return render_template('login.html')


@server.route("/favicon.ico", methods=['GET'])
def index():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


########################################################################################################################
nav = dbc.NavbarSimple(
    children=[html.Form(dbc.NavItem(html.Button(dbc.NavLink("Back"))), action="/main", method="POST"),
              ],
    brand=" Bike Demand Prediction - Data Visualization & Table",
    brand_href="#",
    sticky="top",
    color="#e3f2fd"
)
########################################################################################################################
tab = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Raw Dataset of Bike Rentals in West Governors City", style={"color": "#de795b"}),
                        html.H4("This shows only 30 rows of all dataset.", style={"color": "#5bc0de"}),
                        html.H6("(If you need the whole dataset, please contact City Hall Public Information Center)",
                                style={"color": "black"}),
                        dbc.Table(table_header + table_body,
                                  bordered=True,
                                  dark=True,
                                  hover=True,
                                  responsive=True,
                                  striped=True,
                                  )
                    ]
                )
            ]
        ), html.Hr()
    ],
    className="mt-4",
)
########################################################################################################################
vis1 = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Trend of Bike Rentals by Date", style={"color": "#de795b"}),
                        dcc.Graph(
                            figure=date_count
                        )
                    ]
                ),
            ]
        ), html.Hr()
    ],
    className="mt-4",
)
########################################################################################################################
vis2 = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Relationship between Bike Rental and Temperature", style={"color": "#de795b"}),
                        dcc.Graph(
                            id='rel_count_temp',
                            figure={
                                'data': [
                                    dict(
                                        x=visd2["temperature"],
                                        y=visd2["count"],
                                        mode='markers',
                                        opacity=0.7,
                                        marker={
                                            'size': 15,
                                            'line': {'width': 0.5, 'color': 'white'}
                                        }
                                    )
                                ],
                                'layout': dict(
                                    xaxis={'type': 'log', 'title': 'Temperature'},
                                    yaxis={'title': 'Number of Bike Rental'},
                                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                                    legend={'x': 0, 'y': 1},
                                    hovermode='closest'
                                )
                            }
                        ),
                    ]
                ),
            ]
        ), html.Hr()
    ],
    className="mt-4",
)
########################################################################################################################
vis3 = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Relationship Between Each Features", style={"color": "#de795b"}),
                        dcc.Graph(
                            id='heatmap',
                            figure={
                                'data': [{
                                    'z': heatfig["values"],
                                    'x': heatfig["columns"],
                                    'y': heatfig["bcolumns"],
                                    'type': 'heatmap'
                                }]
                            }
                        ),
                    ]
                ),
            ]
        ), html.Hr()
    ],
    className="mt-4",
)

########################################################################################################################
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    server=server,
    routes_pathname_prefix='/visual/'
)
app.title = "WGU - Bike Demand Prediction"
app.layout = html.Div([nav, vis1, vis2, vis3, tab],
                      className="container")


@server.route('/forgotpw')
def forgotpw():
    return render_template('forgotpw.html')


@server.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        if admin_id == request.form['login'] and admin_pw == request.form['password']:
            global session
            session = requests.Session()
            session.params["logged"] = False
            session.params["logged"] = True
            return redirect("/main", code=307)
        else:
            return render_template("wronginfo.html")
    else:
        return render_template("wrongaccess.html")


@server.route("/main", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        return render_template("main.html")
    else:
        return render_template("wrongaccess.html")


@server.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        temp = request.values["temperature"]
        humidity = request.values["humidity"]
        weather = request.values["weather"][0:1]
        predict_attr = {"weather": weather, "temp": temp, "humidity": humidity}
        ml_model = predictor.predictor(predict_attr)
        tmrw_demand = int(round(ml_model["tmrw_demand"]))
        score = (round(ml_model["score"], 3)) * 100

        return render_template("predict.html", tmrw_demand=tmrw_demand, score=score)
    else:
        return render_template("wrongaccess.html")


if __name__ == "__main__":
    server.run(host="0.0.0.0", debug=True)
