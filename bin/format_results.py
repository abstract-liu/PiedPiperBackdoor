import argparse
import json
import os

parser = argparse.ArgumentParser(
    description="convert results to result.json"
)

parser.add_argument(
    "--results_dir",
    type=str,
)

parser.add_argument(
    "--results_file",
    type=str
)

parser.add_argument(
    "--contract_name",
    type=str
)

def find_non_empty_csv_files(directory: str):
    non_empty_files = []
    for filename in os.listdir(directory):
        if not filename.endswith(".csv"):
            continue
        filepath = os.path.join(directory, filename)

        if os.path.isfile(filepath):
          file_size = os.path.getsize(filepath)

          if file_size > 0:
            non_empty_files.append(filename)

    return non_empty_files

def write_results(results_dir: str, results_file: str, contract_name: str) -> None:
    non_empty_csv_files = find_non_empty_csv_files(results_dir)
    relations = [f.replace(".csv", "") for f in non_empty_csv_files]
    single_result = [contract_name, relations]
    json_result = [single_result]
    
    with open(results_file, "w") as json_file:
        json.dump(json_result, json_file, indent=4)

if __name__ == "__main__":
    args = parser.parse_args()
    write_results(args.results_dir, args.results_file, args.contract_name)