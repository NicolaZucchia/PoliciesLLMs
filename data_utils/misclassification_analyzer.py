import os
import json
import pandas as pd

# Input directories
ground_truth_dir = "Categories"
prediction_dir = "Output/jsonResults/2shot"

# Output file
output_csv = "Metrics/gpt-4o-mini/misclassification/2shot_category_discrepancies.csv"

def calculate_discrepancies(ground_truth_dir, prediction_dir):
    discrepancies = {}

    # Iterate through all files in the ground truth directory
    for gt_file in os.listdir(ground_truth_dir):
        gt_path = os.path.join(ground_truth_dir, gt_file)

        # Ensure a corresponding prediction file exists
        pred_file = gt_file.replace(".json", "_result.json")
        pred_path = os.path.join(prediction_dir, pred_file)

        if not os.path.exists(pred_path):
            print(f"Warning: Prediction file not found for {gt_file}")
            continue

        # Load ground truth and prediction JSON
        with open(gt_path, "r") as f:
            ground_truth = json.load(f)
        with open(pred_path, "r") as f:
            prediction = json.load(f)

        # Compare categories
        for category in ground_truth.keys():
            if category not in discrepancies:
                discrepancies[category] = {"total_mismatches": 0, "false_positives": 0, "false_negatives": 0}

            gt_value = ground_truth[category]
            pred_value = prediction.get(category, None)  # Default to None if key is missing

            if pred_value != gt_value:
                discrepancies[category]["total_mismatches"] += 1
                if pred_value is True and gt_value is False:
                    discrepancies[category]["false_positives"] += 1
                elif pred_value is False and gt_value is True:
                    discrepancies[category]["false_negatives"] += 1

    return discrepancies

def save_discrepancies_to_csv(discrepancies, output_csv):
    # Convert discrepancies into a DataFrame
    data = [
        {
            "Category": category,
            "Total Mismatches": values["total_mismatches"],
            "False Positives": values["false_positives"],
            "False Negatives": values["false_negatives"],
        }
        for category, values in discrepancies.items()
    ]

    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)
    print(f"Results saved to {output_csv}")

if __name__ == "__main__":
    # Calculate discrepancies
    discrepancies = calculate_discrepancies(ground_truth_dir, prediction_dir)

    # Save results to CSV
    save_discrepancies_to_csv(discrepancies, output_csv)