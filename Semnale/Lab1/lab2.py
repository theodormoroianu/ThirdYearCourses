# Theodor Moroianu
# Grupa 334

#%%
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wf
import scipy.signal as sg
import math

# %%
# Exercitiu 1

# A
frc = 2000
durata = 1 / frc
print("Durata:", durata)
# Durata dintre doua esantioane este de
# 0.0005 secunde.

# B
dim_esantion = 4
sec_per_hour = 60 * 60
dim_total = frc * sec_per_hour * dim_esantion
print("Dimensiune:", dim_total / 8, "Bytes")
# Dimensiunea este de 3.6Mb.
# 3600000 Bytes.

# %%
# Exercitiul 2

# x(t) = cos(200*pi*t) = cos(100 * 2 * pi * t)
# Asadar, frecventa este de 100
frc_x = 100

# y(t) = cos(80*pi*t) = cos(40 * 2 * pi * t)
# Asadar, frecventa este de 40
frc_y = 40

# Frecventa maxima din semnalul compus este 100
frc_max = 100

# Fie frecventa minima de esantionare T.
# Frecventa Nyquist va fi T / 2, care trebuie sa fie mai mare sau egal
# ca frc_max.
# Asadar, T / 2 >= frc_max
# T / 2 >= 100
# T >= 200

# Frecventa minima de esantionare este de 200Hz.



# %%
# Exercitiul 3

def cosine(amp, frq, ph, t):
    return amp * np.cos(2 * np.pi * frq * t + ph)

time_of_view = 0.03
ctime = np.linspace(0, time_of_view, 10**5)
x_signal = cosine(1, 520 / 2, np.pi / 3, ctime)
y_signal = cosine(1, 280 / 2, -np.pi / 3, ctime)
z_signal = cosine(1, 120 / 2, np.pi / 3, ctime)

dtime = np.linspace(0, time_of_view, int(200 * time_of_view) + 1)
x_disc = cosine(1, 520 / 2, np.pi / 3, dtime)
y_disc = cosine(1, 280 / 2, -np.pi / 3, dtime)
z_disc = cosine(1, 120 / 2, np.pi / 3, dtime)


fig, axes = plt.subplots(nrows=4, ncols=1, sharex=True, sharey=True)
fig.suptitle('Aliere A Semnalelor')

axes[0].plot(ctime, x_signal)
axes[0].stem(dtime, x_disc)
axes[1].plot(ctime, y_signal)
axes[1].stem(dtime, y_disc)
axes[2].plot(ctime, z_signal)
axes[2].stem(dtime, z_disc)


axes[3].plot(ctime, x_signal)
axes[3].stem(dtime, x_disc)
axes[3].plot(ctime, y_signal)
axes[3].plot(ctime, z_signal)

plt.show()

# %%
# Exercitiul 4

# Stim:

p_semnal_db = 80 # 80 db
# p_semnal_db = 10 * log10(p_semnal)
# p_semnal = 10^(p_semnal_db / 10)
p_semnal = math.pow(10, p_semnal_db / 10)

snr_db = 90 # 90 db
# snr_db = 10 * log10(snr)
# snr = 10^(snr_db / 10)
snr = math.pow(10, snr_db / 10)

# snr = p_semnal / p_zgomot
# p_zgomot = p_semnal / snr

p_zgomot = p_semnal / snr

print("Puterea zgomotului:", p_zgomot)
# 0.1

# %%
# Exercitiul 5
rate, x = wf.read('sound.wav')
f,t,s = sg.spectrogram(x, fs=rate)

fig = plt.figure()
plt.pcolormesh(t, f, 10*np.log10(s), shading='gouraud')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')

plt.show()

"""
Pentru a identifica si izola cele doua sunete separate,
putem:
 1. Aplicam un filtru de blur gaussian usor, pentru a netezi imaginea
 2. Aplicam un filtru de contrast peste imagine, pentru a izola cele doua sunete
 3. Aplicam un threashold boolean, pentru a scapa de zgomotul din imagine
 4. Putem vedea cele doua sunete.
 
"""