import csv
import pandas as pd

def export_result_to_csv(data: dict, filename="simulation_result.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Poste", "Montant (€)"])
        for key, value in data.items():
            writer.writerow([key.replace("_", " ").capitalize(), round(value, 2)])
    return filename

def export_result_to_excel(data: dict, filename="simulation_result.xlsx"):
    df = pd.DataFrame(list(data.items()), columns=["Poste", "Montant (€)"])
    df["Poste"] = df["Poste"].str.replace("_", " ").str.capitalize()
    df.to_excel(filename, index=False)
    return filename
