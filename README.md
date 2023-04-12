# chattychattybangbang [docs](https://microprediction.github.io/chattychattybangbang)
Utilities for using chatgpt more reliably


### Install

    pip install chattychattybangbang
    
### Set key

    import os
    os.environ['OPEN_AI_KEY'] = 'getakeyfromopenaisite' 
    
### Example
Asks ChatGPT a question, then calls it again to QA the answer. 


    from chattychattybangbang.castigateuntilvaluesare import castigate_until_values_are
    question = """
      I would like you to pick three companies from the sp500 index. 
      Return a dictionary containing the main color in their logo (pick one only)
      The keys of the dictionary should be the company tickers. 
      Just provide the dict and nothing else in your response, please. 
    """
    d = castigate_until_values_are(question=question, value_description='a color', max_retries=5)
    print(d)
    
    {'AAPL': 'white', 'MSFT': 'red', 'GOOGL': 'green'}

See [examples](https://github.com/microprediction/chattychattybangbang/tree/main/examples) for presidential poetry appreciation, etc. 

### Article
See [Reliably getting answers out of chatgpt](https://medium.com/@mike.roweprediger/reliably-getting-answers-out-of-chatgpt-by-forcing-it-to-qa-itself-feb1f56782b9) on medium. Thanks to Michael Rowe. 
