from gpiozero import MCP3008

bat = MCP3008(0)

print(bat.value*3.3)
