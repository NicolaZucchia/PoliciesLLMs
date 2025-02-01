import pandas as pd

# Path to the metrics results CSV file
csv_file_path = "../Metrics/gpt35_turbo/performance/2shot_metrics_results.csv"

# Load the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

# Print column names to verify
print("Columns in CSV:")
print(df.columns)

# Columns to calculate averages for (adapt these based on the actual column names in the file)
metric_columns = ["Jaccard Index", "Accuracy", "Precision", "Recall", "F1 Score"]

# Ensure the columns exist in the DataFrame
existing_columns = [col for col in metric_columns if col in df.columns]
if not existing_columns:
    print("No matching metric columns found in the file. Please check the column names.")
else:
    # Calculate averages for each metric
    average_metrics = df[existing_columns].mean()

    # Print the average metrics
    print("\nAverage Metrics:")
    for metric, avg_value in average_metrics.items():
        print(f"{metric}: {avg_value:.4f}")