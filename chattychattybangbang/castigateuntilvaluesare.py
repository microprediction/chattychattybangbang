from chattychattybangbang.castigateuntilvalid import castigate_until_valid
from chattychattybangbang.validators import validate_yes_or_no

DEFAULT_MAX_RETRIES = 3


def values_isa_validator(parsed_response: dict, value_description:str, max_retries=DEFAULT_MAX_RETRIES):
    """ For each value in a dictionary, ask ChatGPT if it meets value_description
        Short-circuit
    :param value_description:  'is a president'
    :return:
    """
    for k, v in parsed_response.items():
        validation_question = 'Please answer the following as a yes or no question only, returning a single word please. Is ' + str(
            v) + ' ' + value_description + ' ?'
        yes_or_no_dict = castigate_until_valid(question=validation_question,
                                          validator=validate_yes_or_no,
                                          max_retries=max_retries)
        if yes_or_no_dict is None:
            return False
        else:
            yes_or_no_values = list(yes_or_no_dict.values())[0]
            if not isinstance(yes_or_no_values, str) or (('no' in yes_or_no_values.lower()) and ('yes' not in yes_or_no_values.lower())):
                return False
    return True


def castigate_until_values_are(question:str, value_description:str, castigator=None, max_retries=DEFAULT_MAX_RETRIES):
    """ Retry until we get a dict whose values are 'value_description'
    :param question:   'Please provide a dictionary length 3 where
    :param value_description:  'is a color'
    :param castigator:
    :param max_retries:
    :return:
    """
    def _validator(parsed_response):
         return values_isa_validator(parsed_response=parsed_response, value_description=value_description)

    return castigate_until_valid(question=question,
                                validator=_validator,
                                  castigator=castigator,
                                max_retries=max_retries)


if __name__=='__main__':
    question = """
      I would like you to pick three companies from the sp500 index. 
      Return a dictionary containing the main color in their logo (pick one only)
      The keys of the dictionary should be the company tickers. 
      Just provide the dict and nothing else in your response, please. 
    """
    d = castigate_until_values_are(question=question, value_description='a color')
    print(d)

