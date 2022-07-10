import matplotlib.pyplot as plt
import numpy as np

def calc_acceleration(velocity, time):
    '''
    Funktion zur Berechnung der Beschleunigung aus dem Geschwndikgeitsverlauf
    '''
    acceleration = []
    for i in range(0, len(t)-1):
        acceleration.append((velocity[i+1] - velocity[i]) / (time[i+1] - time[i]))
    acceleration.append(0)
    return acceleration

def calc_power(v, a):
    '''
    Funktion zur Berechnung der momentanen Antriebsleistung
    '''
    F_Roll = m_Fzg * f_roll * g
    F_Luft = []
    F_Beschleunigung = []
    F_Fzg = []
    power_act = []
    power_sum = []
    #Fahrzeugwiderstände berechnen und summieren
    for i in range(0, len(v)-1):
        F_Luft.append(rho_Luft * c_w * A * v[i])
        F_Beschleunigung.append(e_i * m_Fzg * a[i])
        F_Fzg.append(F_Luft[i] + F_Beschleunigung[i] + F_Roll)
        power_act.append(F_Fzg[i] * v[i])
        if power_act[i] < 0:
            power_act[i] = 0
    power_act.append(0)
    return power_act

def plot_data(x_value, y_value1, y_value2,  y_value3, text):
    '''
    Funktion zum Plotten der Kurven
    '''
    fig, ax = plt.subplots(3, 1)
    ax[0].plot(x_value, y_value1)
    ax[0].set_ylabel('v_Fzg [km/h]')
    ax[1].plot(x_value, y_value2, color = 'red', linewidth = 0.75)
    ax[1].set_ylabel('Beschleuningung [m/s]')
    ax[2].plot(x_value, y_value3, linewidth = 0.75)
    ax[2].set_xlabel('Zeit [s]')
    ax[2].set_ylabel('Leistung [Watt]')
    ax[0].grid(True)
    ax[1].grid(True)
    ax[2].grid(True)
    textstr = 'Mittlere Leistung = {:.2f} Watt'.format(P_mean)
    ax[2].text(0.0, 22000, textstr)
    plt.show()

def mean(param):
    '''Berechnet den Mittelwert der übergebenen Liste'''
    return sum(param) / len(param)


# Fahrzeugparameter
m_Fzg = 1200    # Fahrzeugmasse in kg
rho_Luft = 1.2  # Luftdichte in kg/m^3
A = 1.2         # projezierte Stirnfläche des Fahrzeugs in m^2
c_w = 0.3       # Cw-Wert des Fahrzeugs
f_roll = 0.01   # Rollwiderstandsfaktor
e_i = 1         # Massenfaktor der rotierenden Anteile des Antriebsstrangs
g = 9.81        # Erdbeschleunigung in m/s^2

cycle_array = np.genfromtxt('cycle_data.txt', delimiter='\t')
t = []
v_kmh = []
v_ms = []
for i in range(0, len(cycle_array)-1):
    t.append(cycle_array[i][0])     # Zeitstempel auslesen
    v_kmh.append(cycle_array[i][1]) # Geschwindigkeiten auslesen
    v_ms.append(v_kmh[i] / 3.6)     # Geschwindikeit in m/s umrechnen

a = calc_acceleration(v_ms, t)
P_ist = calc_power(v_ms, a)
P_mean = mean(P_ist)
plot_data(t, v_kmh, a, P_ist, P_mean) # WLTP-Zyklus plotten
