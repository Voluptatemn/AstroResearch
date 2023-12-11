from astroquery.mast import Observations
observations = Observations.query_criteria(obs_collection='TESS', target_name='25132999')
print(observations)