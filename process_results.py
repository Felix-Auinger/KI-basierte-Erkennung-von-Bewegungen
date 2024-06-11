import os
import glob
import re



def extract_value_from_line(file_content, keyword):
    for line in file_content.split('\n'):
        if keyword in line:
            try:
                # Extrahiert die Zahl vor "Grad" oder nach dem Doppelpunkt
                match = re.search(r'([-+]?\d*\.\d+|\d+)', line.split(":")[-1])
                if match:
                    return float(match.group())
            except ValueError:
                continue
    return None

def process_files():
    # 1. Verzeichnis einlesen
    files = glob.glob('./outputs/*results*')
    #print(files)
    file_groups = {}
    
    for file_path in files:
        #print(file_path)

        # 2. Dateinamen verarbeiten
        file_name = os.path.basename(file_path)
        if "_rechts" in file_name:
            key = file_name.split("_rechts")[0]
        elif "_links" in file_name:
            key = file_name.split("_links")[0].strip()
        else:
            continue

        if key in file_groups:
            file_groups[key].append(file_path)
        else:
            file_groups[key] = [file_path]

    # 3. Dateien als Pärchen verarbeiten
    for key, pair in file_groups.items():
        if len(pair) == 2:
            file1, file2 = pair
            
            # Score initialisieren
            score = 0
            
            # Inhalte der Dateien lesen
            with open(file1, 'r') as f:
                content1 = f.read()
            with open(file2, 'r') as f:
                content2 = f.read()
            
            # Werte extrahieren und Score anpassen
            knie_value1 = extract_value_from_line(content1, "Knie")
            knie_value2 = extract_value_from_line(content2, "Knie")
            rumpf_value1 = extract_value_from_line(content1, "Rumpfbewegung")
            # rumpf_value2 = extract_value_from_line(content2, "Rumpfbewegung")
            reakt_value1 = extract_value_from_line(content1, "Reaktiv")
            reakt_value2 = extract_value_from_line(content2, "Reaktiv")

            print("##### Score für Videos " , key, " #####")
            
            if (knie_value1 is not None):
                # die beiden Knie getrennt betrachten
                if knie_value1 < 170: 
                    print("Knie 1: instabil, da Wert ", knie_value1 , " < 170°")
                    score -= 1
                else:
                    score += 1
                    print("Knie 1: stabil")
                
                if (knie_value2 < 170):
                    print("Knie 2: instabil, da Wert ", knie_value2 , " < 170°")
                    score -= 1
                else:
                    score += 1
                    print("Knie 2: stabil")
            
            # Rumpfbewegung ist in beiden Files dieselbe, daher nur einmal werten 
            if rumpf_value1 is not None:
                if rumpf_value1 < 5:
                    print("Rumpf stabil")
                    score += 1
                else:
                    print("Rumpf instabil, da Wert ", rumpf_value1, " > 5°")
                    score -= 1
            
            # Differenz der Reaktivitätsindices berechnen
            if reakt_value1 is not None and reakt_value2 is not None:
                reakt_idx = abs(reakt_value1 - reakt_value2) / ((reakt_value1 + reakt_value2) / 2)
                if reakt_idx < 0.1:
                    print("guter Reaktivitätsindex")
                    score += 1
                else:
                    score -= 1 
                    print("schlechter Reaktivitätsindex. Abweichung , ", reakt_idx, " > 0.1")
            else:
                print("Fehlende Reaktivitätsindexwerte")

            # Score ausgeben: Reicht von -4 (schlecht) bis 4 (sehr gut)
            print("Gesamtscore ", key, ": ", score)

# Hauptfunktion ausführen
process_files()