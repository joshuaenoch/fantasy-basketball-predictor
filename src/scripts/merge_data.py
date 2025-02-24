import pandas as pd

data_2024_2025 = pd.read_csv("/computed_data/new-2024-2025.csv")
model1_predictions = pd.read_csv("/outputs/model1_predictions.csv")
model2_predictions = pd.read_csv("/outputs/model2_predictions.csv")

merged_data = data_2024_2025.merge(
    model1_predictions, on="Player", suffixes=("", "_model1")
)
merged_data = merged_data.merge(
    model2_predictions, on="Player", suffixes=("", "_model2")
)

numeric_columns = merged_data.select_dtypes(include=[float, int]).columns
merged_data[numeric_columns] = merged_data[numeric_columns].round(2)

merged_data.to_csv("/outputs/full_data.csv", index=False)
