# Pomposity Scores for Great Thinkers 
According to ChatGPT


| Thinker            | Pompousness Score |
|--------------------|--------------------|
| jean-paul sartre   | 10                 |
| noam chomsky       | 10                 |
| michel foucault    | 10                 |
| john maynard keynes| 9                  |
| simone de beauvoir | 9                  |
| john stuart mill   | 9                  |
| sigmund freud      | 8                  |
| friedrich nietzsche| 8                  |
| marx               | 8                  |
| freud              | 8                  |
| emile durkheim     | 7                  |
| immanuel kant      | 7                  |
| jung               | 6                  |
| plato              | 6                  |
| rené descartes     | 5                  |  
| aristotle          | 5                  |
| socrates           | 4                  |
| thomas hobbes      | 2                  |
| john locke         | 1                  |


Results are highly stochastic. Just having fun here. For this you can do the following: 

    from chattychattybangbang.castigateuntilvalid import castigate_until_numeric_dict
    from pprint import pprint

    d_all = dict()
    for _ in range(5):
        pomposity_question = """ I would like you to produce a list of ten famous intellectuals of the twentieth century and
                       assign a pomposity score to them between 1 (not pompous) to 10 (extremely pompous). 
                       Please return this as a dictionary keyed by the person's name in lowercase where the 
                       value should be an integer. Only return a dictionary, sorted from most pompous down. 
                       """
        castigator = lambda question_response: pomposity_question + " Make sure you return only a dict, and the complete dict. Do not finish printing"
        d = castigate_until_numeric_dict(question=pomposity_question, castigator=castigator, max_retries=10)
        if d is not None:
            d_all.update(d)
            pprint(sorted(d_all.items(), key=lambda x: x[1]))
