# Most Pompous Great Thinkers 
According to ChatGPT

- **jean-paul sartre** (Pompousness Score: 10)
- **noam chomsky** (Pompousness Score: 10)
- **michel foucault** (Pompousness Score: 10)
- **john maynard keynes** (Pompousness Score: 9)
- **simone de beauvoir** (Pompousness Score: 9)
- **john stuart mill** (Pompousness Score: 9)
- **sigmund freud** (Pompousness Score: 8)
- **friedrich nietzsche** (Pompousness Score: 8)
- **marx** (Pompousness Score: 8)
- **freud** (Pompousness Score: 8)
- **emile durkheim** (Pompousness Score: 7)
- **immanuel kant** (Pompousness Score: 7)
- **jung** (Pompousness Score: 6)
- **plato** (Pompousness Score: 6)
- **aristotle** (Pompousness Score: 5)
- **socrates** (Pompousness Score: 4)
- **rené descartes** (Pompousness Score: 3)
- **thomas hobbes** (Pompousness Score: 2)
- **john locke** (Pompousness Score: 1)

To reproduce you can use this package's functionality: 

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
