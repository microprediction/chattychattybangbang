# chattychattybangbang
Utilities for using chatgpt more reliably


### Install

    pip install chattychattybangbang
    
    
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
