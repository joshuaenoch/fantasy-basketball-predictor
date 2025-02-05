import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer

points_data = pd.read_csv("fppg_py.csv")

data_year1 = pd.read_csv("season_data/2014-2015.csv")
data_year2 = pd.read_csv("season_data/2015-2016.csv")
data_year3 = pd.read_csv("season_data/2016-2017.csv")
data_year4 = pd.read_csv("season_data/2017-2018.csv")
data_year5 = pd.read_csv("season_data/2018-2019.csv")
data_year6 = pd.read_csv("season_data/2019-2020.csv")
data_year7 = pd.read_csv("season_data/2020-2021.csv")
data_year8 = pd.read_csv("season_data/2021-2022.csv")
data_year9 = pd.read_csv("season_data/2022-2023.csv")
data_year10 = pd.read_csv("season_data/2023-2024.csv")
test_data = pd.read_csv("season_data/2024-2025.csv")

data = [
    data_year1,
    data_year2,
    data_year3,
    data_year4,
    data_year5,
    data_year6,
    data_year7,
    data_year8,
    data_year9,
    data_year10,
]

num_atts = [
    "MIN",
    "FGM",
    "FGA",
    "FG3M",
    "FG3A",
    "FTM",
    "FTA",
    "OREB",
    "DREB",
    "REB",
    "AST",
    "STL",
    "BLK",
    "TOV",
    "PTS",
]
cat_atts = ["TEAM_ABBREVIATION"]
numeric_transformer = SimpleImputer(strategy="constant", fill_value=0)
preprocessor = ColumnTransformer(transformers=[("num", numeric_transformer, num_atts)])
models = []

for year in range(len(data)):
    X = data[year][num_atts + cat_atts]
