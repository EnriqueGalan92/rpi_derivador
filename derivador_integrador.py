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
dt = 0.001
T  = 10
L  = 3 # Gain on robust derivator
v0 = 0
z1 = 0
z0 = 0
dato_inicio = 0
dato_mitad = 0
dato_final = 0
pot_values = np.arange(0)
der_values = np.arange(0)
int_values = np.arange(0)
time_values = np.arange(0)

f, (ax1, ax2, ax3) = plt.subplots(3, 1)

print('Reading MCP3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
#print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
print('-' * 57)
print('-' * 20 + 'DERIVADOR ROBUSTO' + '-' * 20)
print('-' * 57)
time.sleep(1)
print('START')
# Main program loop.
for j in range (10000):
    # Read all the ADC channel values in a list.
    values = [0]*8
    volt_values = [0]*8
    for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
        values[i] = mcp.read_adc(i)
        volt_values[i] = adc_volt_value(values[i])
    pot_values=np.append(pot_values,volt_values[5])
        
    y = volt_values[5]

    # Print the ADC values.
    # print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*volt_values))

    # Derivate
    v0 = (-1*pow(L, 0.5)) * pow(abs(z0-y),0.5) * sign_detect(z0-y) + z1
    z1 = z1 + dt * (-1.1 * L * sign_detect(z0-y))
    z0 = z0 + dt * v0
    if (j == 0):
        z1 = 0
        dato_inicio = y
    der_values = np.append(der_values,z1)
    counter += 1
    # Pause for half a second.

    # Integral
    jdt = j * dt
    dato_inicio = y
    if(j%10 == 0):
    	datomitad = y
    if(j%20 == 0):
        datofinal = y
    simpson_int = (jdt/6) * (dato_inicio + 4*dato_mitad + dato_final)
    int_values = np.append(int_values, simpson_int)
    time_values = np.append(time_values, jdt)
                                 
    time.sleep(dt)

print('STOP')
print(pot_values)
print(der_values)

ax1.plot(pot_values, 'r')
ax2.plot(der_values, 'b')
ax3.plot(int_values, 'g')
plt.show()
