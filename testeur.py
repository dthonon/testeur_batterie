import csv
import sys
from time import sleep
from gpiozero import LED, MCP3008

AREF = 3.3
RESIST = 10
TEMPO = 1

ctrl = LED("GPIO24")
bat0 = MCP3008(0)
bat1 = MCP3008(1)

try:
  énergie = 0
  durée = 0
  with open("batterie.csv", "w", newline="") as csvfile:
    csv_out = csv.writer(csvfile)
    csv_out.writerow(["Pas", "Contrôle", "V0(V)", "V1(V)", "I(mA)", "E(mAh)"])
    while True:
      if durée % 10:
        ctrl.on()
      else:
        ctrl.off()
      sleep(TEMPO)
      v0 = bat0.value*AREF
      v1 = bat1.value*AREF
      dv = v1-v0
      intens = dv/RESIST*1000
      énergie += intens*TEMPO/3600
      csv_out.writerow([durée, ctrl.value, v0, v1, intens, énergie])
      print(f"Pas : {durée}, Contrôle : {ctrl.value}, v0 = {v0:.3f}V, v1 = {v1:.3f}V, i = {intens:.3f}mA, e = {énergie:.3f}mAh")
      durée += 1
except KeyboardInterrupt:
  print("Fin")
  sys.exit()
