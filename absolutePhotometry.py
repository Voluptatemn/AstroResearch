import numpy as np

def finding_targ_magnitude(targ_counts, ref_counts, ref_mag):
    return ref_mag - 2.5 * np.log(targ_counts/ref_counts)

targ_count = 22373
ref_counts = [5619, 2364, 27397, 9500, 11008]
ref_mags = [14.17, 15.11, 12.45, 13.60, 13.44] 

tag_mags = []
for i in range (len(ref_counts)):
    tag_mags.append(finding_targ_magnitude(targ_count, ref_counts[i], ref_mags[i]))

print(np.mean(tag_mags), np.std(tag_mags))
  