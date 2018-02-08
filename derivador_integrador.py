import time
import numpy as np
from matplotlib import pyplot as plt

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

def adc_volt_value(adc_value):
    volt_value = 0
    volt_value = (adc_value * 3.3)/1024
    return volt_value

def sign_detect(val_eval):
    if (0 > val_eval):
        return -1
    else:
        return 1
    return 0

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

counter = 0

# Derivator Variable declarations
dt = 0.1
T  = 10
L  = 3 # Gain on robust derivator
v0 = 0
z1 = 0
z0 = 0

print('Reading MCP3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
#print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
print('-' * 57)
print('-' * 20 + 'DERIVADOR ROBUSTO' + '-' * 20)
print('-' * 57)
# Main program loop.
for j in range (100):
    # Read all the ADC channel values in a list.
    values = [0]*8
    volt_values = [0]*8
    pot_values = []
    der_values = []
    for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
        values[i] = mcp.read_adc(i)
        volt_values[i] = adc_volt_value(values[i])
    pot_values.append(volt_values[5])
    y = volt_values[5]

    # Print the ADC values.
    # print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*volt_values))

    # Derivate
    v0 = (-1*pow(L, 0.5)) * pow(abs(z0-y),0.5) * sign_detect(z0-y) + z1
    z1 = z1 + dt * (-1.1 * L * sign_detect(z0-y))
    z0 = z0 + dt * v0
    der_values.append(z1)

    print ('Valor = {5:>4} '.format(*volt_values))
    counter += 1
    # Pause for half a second.
    time.sleep(dt)

ax = plt.subplot(111)
t = np.arange(0.0, T, dt)
line, = plt.plot(t, pot_values, lw = 2)
plt.show()
