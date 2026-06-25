from time import sleep
from gpiozero import MCP3008

AREF = 3.3
RESIST = 47
TEMPO = 1

bat0 = MCP3008(0)
bat1 = MCP3008(1)

energ = 0
while True:
  v0 = bat0.value*AREF
  v1 = bat1.value*AREF
  dv = v0-v1
  intens = dv/RESIST
  puiss = dv*intens
  energ += puiss*TEMPO/3.6
  print(f"v0 = {v0:.3f}, v1 = {v1:.3f}, i = {intens:.3f}, e = {energ:.3f}")
  sleep(TEMPO)
