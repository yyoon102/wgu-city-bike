import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def table_for_vis():
    temp = pd.read_csv("data/raw-data.csv")
    tab = temp.head(30)
    tab_rows = tab
    vis_tab = {"columns": temp.columns, "rows": tab_rows}

    return vis_tab


def vis_count_by_date():
    tab = pd.read_csv("data/raw-data.csv")
    tab_date = tab["datetime"]
    tab_count = tab["count"]
    vis_list = {"date": tab_date, "count": tab_count}

    return vis_list


def vis_rel_count_temp():
    temp = pd.read_csv("data/raw-data.csv")
    vis_list = {"temperature": temp["temp"], "count": temp["count"]}
    return vis_list


def vis_heatmap():
    columns = ['season', 'holiday', 'workingday', 'weather', 'temp', 'atemp',
       'humidity', 'windspeed', 'count']
    bcolumns = ['count', 'windspeed', 'humidity', 'atemp', 'temp', 'weather',
       'workingday', 'holiday', 'season']
    values = [
                [0.16, -0.15, 0.19, 0.26, 0.26, 0.0089, -0.0081, 0.029, 1],
                [-0.0054, 0.0084, 0.001, -0.0052, 0.00029, -0.0071, -0.25, 1, 0.029],
                [0.012, 0.013, -0.011, 0.025, 0.03, 0.034, 1, -0.25, -0.0081],
                [-0.13, 0.0073, 0.41, -0.055, -0.055, 1, 0.034, -0.0071, 0.0089],
                [0.39, -0.018, -0.065, 0.98, 1, -0.055, 0.03, 0.00029, 0.26],
                [0.39, -0.057, -0.044, 1, 0.98, -0.055, 0.025, -0.0052, 0.26],
                [-0.32, -0.32, 1, -0.044, -0.065, 0.41, -0.011, 0.0019, 0.19],
                [0.1, 1, -0.32, -0.057, -0.018, 0.0073, 0.013, 0.0084, -0.15],
                [1, 0.1, -0.32, 0.39, 0.39, -0.13, 0.012, -0.0054, 0.16]
            ]
    heatmap = {"columns":columns, "bcolumns":bcolumns, "values":values}
    return heatmap