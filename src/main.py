'''
Recently I was reading about logistic regression and support vector machines and came across this presentation on slideshare:
www.slideshare.net/NYCPredictiveAnalytics/intro-to-classification-logistic-regression-svm

And on slide 8, at the bottom, the author says that, for a two-outcome system with a known probability of either outcome, the most successful prediction algorithm is always to predict the more likely outcome. This was referred to as an "inference rule".

I was curious about this... What about randomizing the prediction, where the prediction has the same outcomes and probabilities as the actual event being predicted?

This runs a trial to test this computationally.

Spoiler alert: I did the napkin algebra... and making the same guess every time really is the best algorithm. Interesting.

Basically, it comes down to this:
    - Givens:
        * Two outcomes are possible: "A" or "not A"
        * P(outcome = "A") = p
    - Two algorithms for predicting A are as follows:
        * Algo 1: If p > 0.5, then always predict "A". Else, predict "not A".
        * Algo 2: Make a new prediction each time. Predict "A" with probability p, or "not A" with probability 1-p.
    - hypothesis: Algo 2 is better than Algo 1
    - testable prediction: Algo 2 will predict the outcome correctly more often than Algo 1.

Created on Aug 1, 2012

@author: willg
'''

import random
import time

'''
Outcomes: 
    0 or 1
Probabilities:
    P(0) = 0.6    # 0 is slightly more likely than 1...
'''

probabilities = {0:0.7, 1:0.3}  # {outcome: probability}
# 1 is redundant here, but I want to preserve the possiblity of extending this to more than just 2 outcomes.

class RandomProcess( object ):
    def __init__( self, probabilities ):
        self.probabilities = probabilities
    def generate_outcome( self ):
        pick = random.uniform( 0, 1 )
        tmp = 0
        for outcome, p in probabilities.iteritems():
            tmp += p
            if pick < tmp:
                return outcome

class Algo( object ):
    def __init__( self, probabilities ):
        self.probabilities = probabilities

class Algo1( Algo ):
    def predict( self ):
        probabilities = self.probabilities
        # find key with greatest value
        most_likely_outcome = max( probabilities, key = probabilities.get )
        # return that key
        return most_likely_outcome

class Algo2( Algo ):
    def predict( self ):
        probabilities = self.probabilities
        pick = random.uniform( 0, 1 )
        tmp = 0
        for outcome, p in probabilities.iteritems():
            tmp += p
            if pick < tmp:
                return outcome

class Test( object ):
    def __init__( self, probabilities ):
        self.random_process = RandomProcess( probabilities )
        self.algos = dict( ( algo.__name__, algo( probabilities ) ) for algo in Algo.__subclasses__() )
        self.predictions = dict( ( algo, [] ) for algo in self.algos )
    
    def run( self ):
        for algo in self.algos:
            self.predictions[algo].append( self.algos[algo].predict() )
    
    def report_results( self ):
        generate_outcome = self.random_process.generate_outcome
        scores = dict( ( algo, 0 ) for algo in self.algos )
        for algo in self.algos:
            predictions = self.predictions[algo]
            for pred in predictions:
                if generate_outcome() == pred:
                    # tally up correct answers!
                    scores[algo] += 1
        print scores

if __name__ == '__main__':
    t_start = time.time()
    t = Test( probabilities )
    for _ in range( 100000 ):
        t.run()
    t.report_results()
    t_end = time.time()
    print "%.10f seconds" % ( t_end - t_start )
    
