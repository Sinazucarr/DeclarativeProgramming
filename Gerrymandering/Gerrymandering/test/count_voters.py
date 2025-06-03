import os
import re
import csv

def analyze_votes_in_file(file_path):
    """
    Scansiona un file .lp, estrae tutte le triple vote(riga, col, valore).
    Restituisce:
      - max_riga, max_col (dimensione griglia)
      - count0, count1 (conteggio voti 0 e 1)
    """
    # Espressione regolare per catturare vote(R,C,V).
    vote_pattern = re.compile(r'vote\(\s*(\d+)\s*,\s*(\d+)\s*,\s*([01])\s*\)\.')
    
    max_r = 0
    max_c = 0
    count0 = 0
    count1 = 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            m = vote_pattern.search(line)
            if m:
                r = int(m.group(1))
                c = int(m.group(2))
                v = int(m.group(3))
                # aggiorna dimensione griglia
                if r > max_r: max_r = r
                if c > max_c: max_c = c
                # aggiorna conteggio voti
                if v == 0:
                    count0 += 1
                else:
                    count1 += 1
    
    return max_r, max_c, count0, count1

def main():
    folder = 'benchmarks'  # cartella che contiene i file .lp
    results = []

    # Scorri tutti i file nella cartella
    for filename in os.listdir(folder):
        if filename.endswith('.lp'):
            file_path = os.path.join(folder, filename)
            # Analizza votes per estrarre grid_size e voti
            grid_r, grid_c, c0, c1 = analyze_votes_in_file(file_path)
            results.append({
                'instance': filename,
                'grid_rows': grid_r,
                'grid_cols': grid_c,
                'votes0': c0,
                'votes1': c1
            })

    # Scrivi i risultati in un CSV
    output_file = 'votes_summary.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['instance', 'grid_rows', 'grid_cols', 'votes0', 'votes1']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print(f"Risultati scritti in {output_file}")

if __name__ == '__main__':
    main()
