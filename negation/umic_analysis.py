import json
import numpy as np
import scipy.stats
from collections import defaultdict

def main():
    with open('./correct_yes_no_umic.json') as f:
        correct_caps = json.load(f)
    with open('./negated_correct_yes_no_umic.json') as f:
        negated_correct_caps = json.load(f)
    

    all_scores = []
    correct_scores = []
    incorrect_scores = []
    almost_equal_correct = 0
    incorrect_ranking = 0
    for correct, negated_correct in zip(correct_caps, negated_correct_caps):
        correct_scores.append(correct['UMIC_score'])
        incorrect_scores.append(negated_correct['UMIC_score'])
        score = (correct['UMIC_score'], negated_correct['UMIC_score'])
        if np.abs(correct['UMIC_score'] - negated_correct['UMIC_score']) == 0:
            almost_equal_correct += 1
            #print('sample correct:', correct, negated_correct)
        all_scores.append(score)
        if correct['UMIC_score'] < negated_correct['UMIC_score']:
            incorrect_ranking += 1
    min = np.min(all_scores)
    max = np.max(all_scores)
    range = max - min
    print('min, max: ', min, max)
    print('correct', np.mean((correct_scores-min)/ range), np.std((correct_scores-min)/ range))
    print('negated', np.mean((incorrect_scores-min)/ range), np.std((incorrect_scores-min)/ range))
    print('len all_scores', len(all_scores))
    print('almost_equal_correct', almost_equal_correct/len(correct_caps)*100, '%')
    print('incorrect_ranking', incorrect_ranking/len(correct_caps)*100)

    print('t-test correct_scores/incorrect_scores: ', scipy.stats.ttest_ind((correct_scores-min)/range,(incorrect_scores-min)/range))
    
    
main()