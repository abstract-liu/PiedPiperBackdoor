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

def write_results(results_dir: str, results_file: str, contract_name: str) -> None:
    csv_files = [f for f in os.listdir(results_dir) if f.endswith(".csv")]
    relations = [f.replace(".csv", "") for f in csv_files]
    single_result = [contract_name, relations]
    json_result = [single_result]
    
    with open(results_file, "w") as json_file:
        json.dump(json_result, json_file, indent=4)

if __name__ == "__main__":
    args = parser.parse_args()
    write_results(args.results_dir, args.results_file, args.contract_name)