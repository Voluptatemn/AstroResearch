'''
Limiting magnitude of r band for 300 second exposure in 3 arcsecond seeing (1.5 arcseond aperture radius)
SNR = 10, zeropoit from observatory paper, gain of new camera, Background level given in slides
'''

import numpy as np

def lim_mag(background, mzp = 21.91, SNR = 10, aperture_radius = 1.5, gain = 0.97, time_exposure = 300):
    '''
    brute force
    '''
    background_counts = np.power(10, -0.4*(background - mzp))
    number_pix = np.pi * np.power(aperture_radius, 2)
    mag_lim = mzp - 2.5 * np.log10(SNR * np.sqrt(number_pix * background_counts / (gain * time_exposure)))
    return mag_lim

def lim_mag_simplified(background, mzp = 21.91, SNR = 10, aperture_radius = 1.5, gain = 0.97, time_exposure = 300):
    '''
    simplied the equation from plugging in the background magnitude to background counts
    proved it to be linear relationship between background magnitude and limit magnitude
    '''
    mag_lim = 0.5 * mzp - 2.5 * np.log10(SNR * aperture_radius * np.sqrt(np.pi / (gain * time_exposure))) + 0.5 * background
    return mag_lim

skyglow = 22 
moon = 17 
light_pollution = 18 

lim_mag_sky = lim_mag(skyglow) 
lim_mag_moon = lim_mag(moon)
lim_mag_light_pollution = lim_mag(light_pollution)
print(lim_mag_sky, lim_mag_moon, lim_mag_light_pollution)

lim_mag_sky = lim_mag_simplified(skyglow) 
lim_mag_moon = lim_mag_simplified(moon)
lim_mag_light_pollution = lim_mag_simplified(light_pollution)
print(lim_mag_sky, lim_mag_moon, lim_mag_light_pollution)