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

'''
Outcomes: 
    0 or 1
Probabilities:
    P(0) = 0.6    # 0 is slightly more likely than 1...
'''

probabilities = {0:0.7, 1:0.3}  # {outcome: probability}
# 1 is redundant here, but I want to preserve the possiblity of extending this to more than just 2 outcomes.

class Outcome( object ):
    def __init__( self, probabilities ):
        self.probabilities = probabilities
    def generate( self ):
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
        self.outcome_generator = Outcome( probabilities )
        self.algos = [cla( probabilities ) for cla in Algo.__subclasses__()]
        self.outcomes = []
        self.predictions = dict( ( algo.__class__.__name__, [] ) for algo in self.algos )
    
    def run( self ):
        self.outcomes.append( self.outcome_generator.generate() )
        for algo in self.algos:
            self.predictions[algo.__class__.__name__].append( algo.predict() )
    
    def report_results( self ):
        outcomes = self.outcomes
        scores = dict( ( algo.__class__.__name__, 0 ) for algo in self.algos )
        # process data...
        # tally up correct answers!
        for algo in self.algos:
            print algo.__class__.__name__
            predictions = self.predictions[algo.__class__.__name__]
            for ( pred, outc ) in zip( predictions, outcomes ):
                if pred == outc:
                    scores[algo.__class__.__name__] += 1
        print scores

if __name__ == '__main__':
    t = Test( probabilities )
    for _ in range( 1000 ):
        t.run()
    t.report_results()
    print "done" 
    
