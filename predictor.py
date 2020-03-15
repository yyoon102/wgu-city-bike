import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor


def predictor(attr):
    ### split data
    train = pd.read_csv("data/train-data.csv")
    X = train.drop("count", axis=1)
    y = train["count"]
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    ### train data
    model = RandomForestRegressor(n_jobs=-1,
                                  random_state=42)
    model.fit(x_train, y_train)

    ### evaluate data
    score = model.score(x_test, y_test)

    ### add user's input
    our_data = pd.read_csv("data/test-data.csv")
    our_data["humidity"] = int(attr["humidity"])
    our_data["temp"] = int(attr["temp"])
    our_data["weather"] = int(attr["weather"])

    ### predict tomorrow's demand
    tmrw_bike = model.predict(our_data)
    ml_model = {"tmrw_demand" : tmrw_bike.sum(), "score":score}

    return ml_model
