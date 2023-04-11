from chattychattybangbang.openaicredentials import set_credentials
from chattychattybangbang.validators import default_validator
from chattychattybangbang.jsonutil import json_or_none
from chattychattybangbang.castigators import default_castigator
from chattychattybangbang.openutil import ask_gpt


DEFAULT_MAX_RETRIES = 3


def castigate_until_valid(question:str, validator=None, castigator=None, max_retries=DEFAULT_MAX_RETRIES):
    if validator is None:
        validator = default_validator
    if castigator is None:
        castigator = default_castigator

    retries = 0

    while retries < max_retries:
        response = ask_gpt(question)
        parsed_response = json_or_none(response)

        if parsed_response and validator(parsed_response):
            break

        question = castigator(question, response)
        retries += 1

    if retries == max_retries:
        return None
    else:
        return parsed_response



if __name__=='__main__':
    question = """
      I would like you to create a dictionary by choosing three tickers from companies
      that were in the sp500 index in 2011 and returning a dictionary with keys given by
      the tickers and values equal to a text description of the colors of the companies
      in question. 
    """
    d = castigate_until_valid(question=question)

