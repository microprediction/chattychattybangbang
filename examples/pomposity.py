from chattychattybangbang.castigateuntilvalid import castigate_until_numeric_dict
from pprint import pprint

if __name__=='__main__':
    d_all = dict()
    for _ in range(5):
        pomposity_question = """ I would like you to pick any ten pretty famous intellectuals from any era and
                       assign a pomposity score to them between 1 (1 mean not pompous) to 10 (10 means extremely pompous). 
                       Please return this as a dictionary keyed by the person's name  where the 
                       value should be an integer. Only return a dictionary, sorted from most pompous down. 
                       """
        castigator = lambda question_response: pomposity_question + " Make sure you return only a dict, and the complete dict. Do not finish printing"
        d = castigate_until_numeric_dict(question=pomposity_question, castigator=castigator, max_retries=10)
        if d is not None:
            d_all.update(d)
            pprint(sorted(d_all.items(), key=lambda x: x[1], reverse=True))
