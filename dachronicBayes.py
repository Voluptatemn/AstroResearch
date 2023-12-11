import numpy 

def bayes(prior, likelihood, specificity):
    return likelihood * prior / (likelihood * prior + specificity * (1 - prior))

pos_likelihood = 0.8
pos_specificity = 0.096
neg_likelihood = 0.904
neg_specificy = 0.2

prior = 0.01
for i in range (4):
    prior = bayes(prior, pos_likelihood, pos_specificity)
    print(prior)


prior = 0.08
one_prior = bayes(1 - prior, neg_likelihood, neg_specificy)
print(one_prior)
two_prior = bayes(one_prior, neg_likelihood, neg_specificy)
print(two_prior)
