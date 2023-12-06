import numpy as np

def finding_targ_magnitude(targ_counts, ref_counts, ref_mag):
    return ref_mag - 2.5 * np.log10(targ_counts/ref_counts)

def mag_to_flux(mag, zp_mag = 24.76):
    return 3631 * (10 ** (-0.4*(mag - zp_mag)))

def jy_to_W(flux):
    return flux * (10 ** -26)

targ_count = 22373
ref_counts = [5619, 2364, 27397, 9500, 11008]
ref_mags = [14.17, 15.11, 12.45, 13.60, 13.44] 

targ_flux = []
for i in range (len(ref_counts)):
    targ_flux.append(jy_to_W(mag_to_flux(finding_targ_magnitude(targ_count, ref_counts[i], ref_mags[i]))))
targ_flux = np.array(targ_flux)
print(np.mean(targ_flux), np.std(targ_flux))

Aeff = 0.7
c = 299792458
h = 6.62607015 * (10 ** -34)
photon_per_sec = targ_flux * Aeff * 0.47 * (703-545) * (10 ** -9) / c / h
print(np.mean(photon_per_sec), np.std(photon_per_sec))

