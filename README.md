Declarative Programming Project – Gerrymandering (ASP + Python)
================================================================

This project demonstrates the use of Answer Set Programming (ASP) to model and analyze gerrymandering strategies in grid-based electoral systems. The objective is to partition a voting region (represented as a 2D grid) into a fixed number of contiguous districts to maximize the number of seats won by a given political party.

------------------------------------------------------------
Project Structure
------------------------------------------------------------

Gerrymandering/
├── benchmarks/               # 100 benchmark instances in ASP format (.lp)
├── imgs/                     # Graphical results and heatmaps from experiments
├── report/                   # Final PDF reports (English and Italian versions)
├── test/                     # Utility scripts for vote counting and debugging
├── generate_benchmarks.py    # Python script for generating benchmark instances
├── political_districting.lp  # ASP encoding for the districting problem
├── run_experiments_python.py # Python script for running Clingo on all benchmarks
├── results_python.csv        # CSV file with solver results

------------------------------------------------------------
Getting Started
------------------------------------------------------------

Requirements:
- Python 3.8 or higher
- Clingo 5.7.1 or later (must be available in the system PATH)

Install Clingo:
pip install clingo

1. Run All Experiments:
------------------------
To execute the main solver on all benchmark files:
python run_experiments_python.py

This script will:
- Run Clingo for both Party 0 and Party 1
- Enforce a timeout of 300 seconds per run
- Save all output results in results_python.csv

2. Generate New Benchmark Instances:
------------------------------------
To generate a new set of randomized benchmark instances:
python generate_benchmarks.py

This will:
- Generate randomized grid configurations with party votes
- Save the new .lp files in the benchmarks/ folder

------------------------------------------------------------
Utilities
------------------------------------------------------------

- test/count_voters.py: Count votes per party in each .lp instance
- test/debug_districting.lp: Simplified ASP encoding for debugging connectivity
- votes_summary.csv: Summary output from the vote counter script

------------------------------------------------------------
Reports
------------------------------------------------------------

Theoretical background, model structure, and experimental analysis are provided in:

- report/GerrymanderingENG.pdf – English version
- report/GerrymanderingITV.pdf – Italian version

------------------------------------------------------------
Visualizations
------------------------------------------------------------

All report images (plots, heatmaps, examples) are stored in the imgs/ folder.

------------------------------------------------------------
Extra Files
------------------------------------------------------------

This repository includes two PDF files with study notes used to support project development.

------------------------------------------------------------
Contacts
------------------------------------------------------------

For inquiries or feedback:
- aurora.felisari@studenti.unipr.it
- claudio.bendini@studenti.unipr.it

------------------------------------------------------------
Project Context
------------------------------------------------------------

This work was developed as part of the Declarative Programming course to explore logic-based modeling and optimization using ASP and Python.
