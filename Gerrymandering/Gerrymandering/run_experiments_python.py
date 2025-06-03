import os
import subprocess
import csv
import time
import re # For regular expressions

# --- Configuration ---
ASP_PROGRAM = "political_districting.lp"
BENCHMARK_DIR = "benchmarks"
RESULTS_FILE = "results_python.csv"  # Using a different name for the Python version's output
TIMEOUT_SECONDS_CLINGO = 300  # 5 minutes for Clingo's internal timeout
PYTHON_TIMEOUT_SAFETY_MARGIN = 30 # Extra seconds for Python's subprocess timeout as a fallback
CLINGO_CONFIGS = {
    "default": [],  
}

CLINGO_MODEL_COUNT = "0"
CLINGO_QUIET_OPTION = ["--quiet=1"] 

def parse_clingo_summary(output_text, clingo_return_code, python_timed_out):
    """
    Parses Clingo's summary output to extract status, max representatives, and model count.
    """
    status = "UNKNOWN"
    max_reps_val = "NA"
    num_models_val = "NA"
    raw_opt_val = "NA"

    if python_timed_out: # Python's subprocess timeout triggered
        status = "PYTHON_SAFETY_TIMEOUT"
    elif "INTERRUPTED" in output_text: # Clingo's internal timeout or user interrupt
        status = "CLINGO_TIMEOUT_INTERRUPT"
    elif "OPTIMUM FOUND" in output_text:
        status = "OPTIMUM_FOUND"
    elif "SATISFIABLE" in output_text: # Check after OPTIMUM FOUND
        status = "SATISFIABLE"
    elif "UNSATISFIABLE" in output_text:
        status = "UNSATISFIABLE"
    elif clingo_return_code != 0 and clingo_return_code not in [10, 20, 30]: # 10,20,30 are normal exits
        status = f"CLINGO_ERROR_CODE_{clingo_return_code}"
    elif clingo_return_code == 0 and status == "UNKNOWN": # If no clear keyword but exit 0, might be unknown
        status = "UNKNOWN_EXIT_0"


    # Parse "Optimization: VALUE"
    opt_match = re.search(r"Optimization\s*:\s*(-?\d+)", output_text)
    if opt_match:
        raw_opt_val = int(opt_match.group(1))
        max_reps_val = -raw_opt_val # Actual N is -(-N)

    # Parse "Models: X" or "Models : X+"
    models_match = re.search(r"Models\s*:\s*(\S+)", output_text)
    if models_match:
        num_models_val = models_match.group(1)
        
    if status in ["OPTIMUM_FOUND", "SATISFIABLE"] and max_reps_val == "NA" and opt_match is None:
        pass

    return status, max_reps_val, num_models_val, raw_opt_val


def main():
    # Check if results file exists to decide on writing header
    write_header = not os.path.isfile(RESULTS_FILE)

    with open(RESULTS_FILE, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        if write_header:
            csv_writer.writerow([
                "Instance", "PartyOptimized", "Strategy", "MaxReps", "TimeSec",
                "Status", "Models", "ClingoReturnCode", "RawOptValue"
            ])

        benchmark_files = sorted([f for f in os.listdir(BENCHMARK_DIR) if f.endswith(".lp")])

        for instance_filename in benchmark_files:
            instance_path = os.path.join(BENCHMARK_DIR, instance_filename)
            print(f"Processing {instance_path}...")

            for party in [0, 1]:
                for strategy_name, strategy_options_list in CLINGO_CONFIGS.items():
                    
                    # Construct the command for Clingo
                    command = [
                        "clingo",
                        ASP_PROGRAM,
                        instance_path,
                        f"-c party_to_optimize={party}",
                        f"--time-limit={TIMEOUT_SECONDS_CLINGO}", # Clingo's internal time limit
                    ]
                    command.extend(CLINGO_QUIET_OPTION) 
                    command.append(CLINGO_MODEL_COUNT)  
                    command.extend(strategy_options_list) 

                    print(f"  Party: {party}, Strategy: {strategy_name} ({' '.join(command[1:])})") # Log command details

                    start_time = time.perf_counter()
                    
                    run_timed_out_by_python = False
                    clingo_output_text = ""
                    clingo_exit_code = "NA"
                    
                    try:
                        # Python's timeout is a safety net, slightly longer than Clingo's
                        process = subprocess.run(
                            command,
                            capture_output=True,
                            text=True,  # Decodes stdout/stderr as strings
                            timeout=TIMEOUT_SECONDS_CLINGO + PYTHON_TIMEOUT_SAFETY_MARGIN,
                            check=False # Don't raise exception for non-zero Clingo exit codes
                        )
                        clingo_output_text = process.stdout + "\n---\n" + process.stderr # Combine stdout and stderr
                        clingo_exit_code = process.returncode
                    except subprocess.TimeoutExpired:
                        run_timed_out_by_python = True
                        clingo_output_text = "Execution timed out by Python script (safety margin)."
                    except FileNotFoundError:
                        clingo_output_text = "Clingo executable not found. Ensure it's in PATH."
                        clingo_exit_code = "FNF_ERROR" # File Not Found
                    except Exception as e:
                        clingo_output_text = f"Python error during subprocess: {str(e)}"
                        clingo_exit_code = "PYTHON_SUBPROC_ERROR"
                    
                    end_time = time.perf_counter()
                    elapsed_time_sec = end_time - start_time

                    # Parse the output
                    status, max_reps, num_models, raw_opt = parse_clingo_summary(
                        clingo_output_text, clingo_exit_code, run_timed_out_by_python
                    )

                    # Write results to CSV
                    csv_writer.writerow([
                        instance_filename,
                        party,
                        strategy_name,
                        max_reps,
                        f"{elapsed_time_sec:.3f}",
                        status,
                        num_models,
                        clingo_exit_code,
                        raw_opt
                    ])
                    csvfile.flush() # Ensure data is written to disk periodically

    print(f"\nBatch processing complete. Results in {RESULTS_FILE}")

if __name__ == "__main__":
    main()