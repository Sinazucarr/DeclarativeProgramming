Gerrymandering Project (ASP + Python)
=====================================

This project explores the use of Answer Set Programming (ASP) to simulate and analyze gerrymandering strategies in a grid-based electoral system. 
The goal is to partition a grid of voters into a fixed number of contiguous districts to maximize the representation of a target political party.

------------------------------------------------------------
Project Structure
------------------------------------------------------------

Gerrymandering/
├── benchmarks/               # 100 benchmark instances in ASP format (.lp)
├── imgs/                     # Graphical results used in the report
├── report/                   # PDF reports (English and Italian versions)
├── test/                     # Utility scripts for vote counting and debugging
├── generate_benchmarks.py    # Python script to generate new benchmark instances
├── political_districting.lp  # Main ASP encoding for the districting problem
├── run_experiments_python.py # Python runner to solve all benchmarks with Clingo
├── results_python.csv        # Output file with all results (one row per run)

------------------------------------------------------------
Getting Started
------------------------------------------------------------

Requirements:
- Python 3.8+
- Clingo 5.7.1+ (must be available in PATH)

Install Clingo:
pip install clingo

1. Run All Experiments:
------------------------
To run Clingo on all benchmark files using the default configuration:
python run_experiments_python.py

This script will:
- Run Clingo for both Party 0 and Party 1
- Impose a timeout of 300 seconds per run
- Save all results in results_python.csv

2. Generate New Benchmarks:
---------------------------
To generate a new set of benchmark instances:
python generate_benchmarks.py

The script will:
- Create randomized grid configurations
- Store the resulting .lp files in the benchmarks/ folder

------------------------------------------------------------
Utilities
------------------------------------------------------------

- test/count_voters.py: counts how many voters voted for each party in every .lp instance.
- test/debug_districting.lp: alternative ASP file for debugging district assignment.
- votes_summary.csv: stores the vote summary output by count_voters.py.

------------------------------------------------------------
Reports
------------------------------------------------------------

You can find a bilingual write-up of the project in:
- report/GerrymanderingENG.pdf – English version
- report/GerrymanderingITV.pdf – Italian version

These include theoretical background, model description, benchmark strategy, and experimental results.

------------------------------------------------------------
Visualizations
------------------------------------------------------------

All the images used in the report (such as average resolution time, district wins, and heatmaps) are stored in the imgs/ folder.

------------------------------------------------------------
Contacts
------------------------------------------------------------

If you need to contact us, feel free to reach us at:
aurora.felisari@studenti.unipr.it or claudio.bendini@studenti.unipr.it
