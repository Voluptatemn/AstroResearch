import numpy 

def bayes(prior, sensitivity, specificity):
    return sensitivity * prior / (sensitivity * prior + specificity * (1 - prior))

prior = 0.08 
sensitivity = 0.8
specificity = 0.096
print(bayes(prior, sensitivity, specificity))

