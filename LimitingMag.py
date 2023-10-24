'''
Limiting magnitude of r band for 300 second exposure in 3 arcsecond seeing (1.5 arcseond aperture radius)
SNR = 10, zeropoit from observatory paper, gain of new camera, Background level given in slides
'''

import numpy as np

def lim_mag(background, mzp = 21.91, SNR = 10, aperture_radius = 1.5, gain = 0.97, time_exposure = 300):
    number_pix = np.pi * np.power(aperture_radius, 2)
    mag_lim = mzp - 2.5 * np.log10(SNR * np.sqrt(number_pix * background / (gain * time_exposure)))
    return mag_lim

skyglow = 22 
moon = 17 
light_pollution = 18 

lim_mag_sky = lim_mag(skyglow) 
lim_mag_moon = lim_mag(moon)
lim_mag_light_pollution = lim_mag(light_pollution)
print(lim_mag_sky, lim_mag_moon, lim_mag_light_pollution)

import matplotlib.pyplot as plt

x = np.linspace(10, 30, 50)
y = lim_mag(x)
plt.scatter(x, y)
plt.show()