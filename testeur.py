import csv
import sys
from pathlib import Path
from time import sleep
from gpiozero import LED, MCP3008

AREF = 3.3  # Tension de référence ADC
RESIST = 15  # Valeur de la résistance de décharge
TEMPO = 1  # Cycle de mesure
TEMPO_C = 60 * 10  # Temporisation de mesure de tension à vide

ctrl = LED("GPIO24")  # GPIO de mise en décharge de la batterie
bat0 = MCP3008(0)  # Point de mesure aval
bat1 = MCP3008(1)  # Point de mesure amont
fic_enreg = Path("batterie.csv")

try:
    énergie = 0.0
    durée = 0

    # Extension du fichier existant, s'il existe
    if fic_enreg.exists():
        print("Ajout au fichier d'enregistrement existant")
        mode = "a"
        # Recherche de la dernière énérgie relevée
        with open(fic_enreg, "r", newline="") as csvfile:
            csv_in = csv.reader(csvfile)
            lig = 0
            for row in csv_in:
                if lig > 0:
                    durée = int(row[0]) + 1
                    énergie = float(row[5])
                lig += 1
    else:
        print("Création d'un nouveau fichier d'enregistrement")
        mode = "w"
    # Boucle infinie de lecture des tensions et écriture dans le fichier csv
    with open(fic_enreg, mode, newline="") as csvfile:
        csv_out = csv.writer(csvfile)
        if mode == "w":
            # Nouveau fichier CSV : ajout de l'entête
            csv_out.writerow(["Pas", "Contrôle", "V0(V)", "V1(V)", "I(mA)", "E(mAh)"])
        while True:
            if durée % TEMPO_C:
                ctrl.on()
            else:
                ctrl.off()
            sleep(TEMPO)
            v0 = bat0.value * AREF
            v1 = bat1.value * AREF
            dv = v1 - v0
            intens = dv / RESIST * 1000
            énergie += intens * TEMPO / 3600
            csv_out.writerow([durée, ctrl.value, v0, v1, intens, énergie])
            print(
                f"Pas : {durée}, Contrôle : {ctrl.value}, v0 = {v0:.3f}V, v1 = {v1:.3f}V, i = {intens:.3f}mA, e = {énergie:.3f}mAh"
            )
            durée += 1
except KeyboardInterrupt:
    print("Fin")
    sys.exit()
