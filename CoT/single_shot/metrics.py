import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def calculate_metrics(intersection_file, model_file):
    """
    Calculate metrics: accuracy, precision, recall, and F1-score.
    """
    intersection = pd.read_csv(intersection_file).set_index("File")
    model = pd.read_csv(model_file).set_index("File")
    
    metrics = {}
    for category in intersection.columns:
        true_values = intersection[category]
        pred_values = model[category]
        
        # Calculate metrics for each category
        metrics[category] = {
            "Accuracy": accuracy_score(true_values, pred_values),
            "Precision": precision_score(true_values, pred_values, zero_division=0),
            "Recall": recall_score(true_values, pred_values, zero_division=0),
            "F1": f1_score(true_values, pred_values, zero_division=0),
        }
    
    return metrics

def summarize_results(gpt4o_csv, gpt35_csv, output_intersection_csv):
    # Load CSV files
    gpt4o = pd.read_csv(gpt4o_csv)
    gpt35 = pd.read_csv(gpt35_csv)
    
    # Ensure columns are integers or booleans
    gpt4o.iloc[:, 1:] = gpt4o.iloc[:, 1:].astype(int)
    gpt35.iloc[:, 1:] = gpt35.iloc[:, 1:].astype(int)
    
    # Create intersection file (1 if both predict threat, else 0)
    intersection = gpt4o.copy()
    intersection.iloc[:, 1:] = (gpt4o.iloc[:, 1:] & gpt35.iloc[:, 1:])
    intersection.to_csv(output_intersection_csv, index=False)
    print(f"Intersection file saved as {output_intersection_csv}")
    
    # Count threats in each category
    threat_counts_gpt4o = gpt4o.iloc[:, 1:].sum().to_dict()
    threat_counts_gpt35 = gpt35.iloc[:, 1:].sum().to_dict()
    threat_counts_intersection = intersection.iloc[:, 1:].sum().to_dict()
    
    print("\n--- Threat Counts ---")
    print("Category | GPT-4o | GPT-3.5 | Intersection")
    for category in threat_counts_gpt4o.keys():
        print(f"{category: <30} | {threat_counts_gpt4o[category]: <7} | {threat_counts_gpt35[category]: <7} | {threat_counts_intersection[category]: <12}")
    
    # Calculate Jaccard Index
    jaccard_values = []
    for category in intersection.columns[1:]:
        gpt4o_vals = gpt4o[category]
        gpt35_vals = gpt35[category]
        intersection_vals = intersection[category]
        union_vals = (gpt4o_vals | gpt35_vals).sum()
        intersection_sum = intersection_vals.sum()
        jaccard = intersection_sum / union_vals if union_vals > 0 else 0
        jaccard_values.append(jaccard)
    
    print("\n--- Jaccard Index ---")
    print("Category | Jaccard Index")
    for category, jaccard in zip(intersection.columns[1:], jaccard_values):
        print(f"{category: <30} | {jaccard:.3f}")
    
    # Calculate evaluation metrics
    print("\n--- Evaluation Metrics ---")
    print("Model     | Category | Accuracy | Precision | Recall | F1")
    for model_name, csv_file in [("GPT-4o", gpt4o_csv), ("GPT-3.5", gpt35_csv)]:
        metrics = calculate_metrics(output_intersection_csv, csv_file)
        for category, values in metrics.items():
            print(f"{model_name: <10} | {category: <30} | {values['Accuracy']:.3f} | {values['Precision']:.3f} | {values['Recall']:.3f} | {values['F1']:.3f}")           

if __name__ == "__main__":
    # Define input and output files
    gpt4o_csv = "gpt4o_labels.csv"       # Path to GPT-4o CSV
    gpt35_csv = "gpt35_labels.csv"       # Path to GPT-3.5 CSV
    intersection_csv = "intersection_labels.csv"  # Output file for intersection
    
    # Run summary
    summarize_results(gpt4o_csv, gpt35_csv, intersection_csv)