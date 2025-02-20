import argparse
import subprocess
import json
import os

BIN_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_RESULTS_FILE = 'results.json'
TEMP_WORKING_DIR = ".temp"

parser = argparse.ArgumentParser(
    description="convert results to result.json"
)

parser.add_argument(
    "filepath",
    metavar = "DIR",
    nargs="+",
    help="The location to grab contracts from (as bytecode files). Accepts both filenames and directories. All contract filenames should be unique."
)

parser.add_argument("-C",
                    "--client",
                    nargs="?",
                    default="",
                    help="additional clients to run after decompilation."
                    )

parser.add_argument("-w",
                    "--working_dir",
                    nargs="?",
                    default=TEMP_WORKING_DIR,
                    const=TEMP_WORKING_DIR,
                    metavar="DIR",
                    help="the location to were temporary files are placed."
                    )

parser.add_argument("-r",
                    "--results_file",
                    nargs="?",
                    default=DEFAULT_RESULTS_FILE,
                    const=DEFAULT_RESULTS_FILE,
                    metavar="FILE",
                    help="the location to write the results."
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

def get_working_dir(contract_name: str) -> str:
    return os.path.join(os.path.abspath(args.working_dir), os.path.split(contract_name)[1].split('.')[0])

def prepare_working_dir(contract_name: str) -> tuple[bool, str, str]:
    newdir = get_working_dir(contract_name)
    out_dir = os.path.join(newdir, 'out')

    if os.path.isdir(newdir):
        return True, newdir, out_dir

    # recreate dir
    os.makedirs(newdir)
    os.makedirs(out_dir)
    return False, newdir, out_dir

"""
    TODO: in-time print stdout and stderr (not required)
    TODO: add result format code
"""
def analyze_contract(contract_filename: str, client_datalog: str):
    try:
        _, work_dir, out_dir = prepare_working_dir(contract_filename)

        decompile_command = [BIN_DIR + "/decompile", "-o", "CALL JUMPI SSTORE SLOAD MLOAD MSTORE", "-d", "-n", "-t", work_dir, contract_filename]
        decompile_process = subprocess.run(decompile_command, universal_newlines=True, capture_output=True)
        assert not(decompile_process.returncode), f"Decompile {contract_filename} failed. Stopping."

        souffle_command = ["souffle", "-F", work_dir, "-D", out_dir, client_datalog]        
        client_analysis_process = subprocess.run(souffle_command, universal_newlines=True, capture_output=True)
        assert not(client_analysis_process.returncode), f"Souffle analysis failed. Stopping."

        contract_name = os.path.split(contract_filename)[1].split('.')[0]
        write_results(out_dir, args.results_file, contract_name)
        
    except Exception as e:
        print(f"Error: {e}")

"""
    analyze startup program needs to do following thing;
        1. clear cache directory
        2. decompile the contract
        3. run the souffle datalog analysis
"""
if __name__ == "__main__":
    args = parser.parse_args()
    for filepath in args.filepath:
        analyze_contract(filepath, args.client)