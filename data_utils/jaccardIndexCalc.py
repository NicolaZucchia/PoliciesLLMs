import os
import json
import csv
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

def align_keys(gt_json, pred_json):
    """
    Align keys between ground truth and predictions, adding missing keys with default values (False).
    """
    all_keys = set(gt_json.keys()).union(set(pred_json.keys()))
    gt_aligned = {key: gt_json.get(key, False) for key in all_keys}
    pred_aligned = {key: pred_json.get(key, False) for key in all_keys}
    return gt_aligned, pred_aligned

def calculate_jaccard_index(json1, json2):
    """
    Calculate the Jaccard Index between two JSON objects.
    """
    keys1 = {key for key, value in json1.items() if value is True}
    keys2 = {key for key, value in json2.items() if value is True}

    intersection = keys1 & keys2
    union = keys1 | keys2

    if not union:  # Handle case where both sets are empty
        return 1.0 if not intersection else 0.0

    return len(intersection) / len(union)

def load_json(file_path):
    """
    Load a JSON file from the given path and ensure boolean values are treated correctly.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        # Ensure all values are booleans for comparison
        for key, value in data.items():
            if not isinstance(value, bool):
                raise ValueError(f"Invalid value for key '{key}' in {file_path}. Expected boolean, got {type(value).__name__}.")
        return data

def count_true_false(json_obj):
    """
    Count the number of 'true' and 'false' values in a JSON object.
    """
    true_count = sum(1 for value in json_obj.values() if value is True)
    false_count = sum(1 for value in json_obj.values() if value is False)
    return true_count, false_count

def calculate_metrics(gt_json, pred_json):
    """
    Calculate accuracy, precision, recall, and F1-score between ground truth and predictions.
    """
    gt_values = [value for value in gt_json.values()]
    pred_values = [value for value in pred_json.values()]

    # Use zero_division=0 to handle cases with no predicted positives
    precision = precision_score(gt_values, pred_values, zero_division=0)
    recall = recall_score(gt_values, pred_values, zero_division=0)
    f1 = f1_score(gt_values, pred_values, zero_division=0)
    accuracy = accuracy_score(gt_values, pred_values)

    return accuracy, precision, recall, f1

def process_directories(gt_dir, pred_dir, output_csv):
    """
    Process all JSON files in the ground truth and prediction directories.
    Compare files with matching names (ignoring '_result' in the prediction files).
    Save results to a CSV file.
    """
    gt_files = sorted([f for f in os.listdir(gt_dir) if f.endswith(".json")])
    pred_files = sorted([f for f in os.listdir(pred_dir) if f.endswith(".json")])

    # Ensure correct matching by stripping '_result' suffix
    gt_file_map = {f: f for f in gt_files}
    pred_file_map = {f.replace("_result", ""): f for f in pred_files}

    results = []

    for gt_file, pred_key in gt_file_map.items():
        if pred_key in pred_file_map:
            gt_path = os.path.join(gt_dir, gt_file)
            pred_path = os.path.join(pred_dir, pred_file_map[pred_key])

            try:
                # Load JSON files
                gt_json = load_json(gt_path)
                pred_json = load_json(pred_path)

                # Align keys between JSONs
                gt_aligned, pred_aligned = align_keys(gt_json, pred_json)

                # Calculate Jaccard Index
                jaccard_index = calculate_jaccard_index(gt_aligned, pred_aligned)

                # Count 'true' and 'false'
                gt_true, gt_false = count_true_false(gt_aligned)
                pred_true, pred_false = count_true_false(pred_aligned)

                # Calculate accuracy, precision, recall, and F1-score
                accuracy, precision, recall, f1 = calculate_metrics(gt_aligned, pred_aligned)

                results.append({
                    "File": gt_file,
                    "Jaccard Index": jaccard_index,
                    "GT True": gt_true,
                    "GT False": gt_false,
                    "Pred True": pred_true,
                    "Pred False": pred_false,
                    "Accuracy": accuracy,
                    "Precision": precision,
                    "Recall": recall,
                    "F1 Score": f1
                })

            except ValueError as e:
                print(f"Error processing files {gt_file} and {pred_file_map[pred_key]}: {e}")
        else:
            print(f"Warning: No prediction file found for {gt_file}")

    # Save results to CSV
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["File", "Jaccard Index", "GT True", "GT False", "Pred True", "Pred False", "Accuracy", "Precision", "Recall", "F1 Score"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow(result)

    print(f"Results saved to {output_csv}")

if __name__ == "__main__":
    # Directories containing the ground truth and prediction JSON files
    ground_truth_dir = "../Categories"
    prediction_dir = "../Output/gpt35_turbo/jsonResults/2shot"

    # Output CSV file
    output_csv = "../Metrics/gpt35_turbo/performance/2shot_metrics_results.csv"

    # Process directories and calculate metrics
    process_directories(ground_truth_dir, prediction_dir, output_csv)