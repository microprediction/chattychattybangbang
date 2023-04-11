from chattychattybangbang.openaicredentials import set_credentials
from chattychattybangbang.validators import default_validator, validate_numeric_dict
from chattychattybangbang.validators import validate_numeric_dict_with_known_keys, STR_KEYS_TYPE
from chattychattybangbang.jsonutil import json_or_none
from chattychattybangbang.castigators import default_castigator
from chattychattybangbang.openutil import ask_gpt
import random
from typing import List
from pprint import pprint

DEFAULT_MAX_RETRIES = 3



def castigate_until_valid(question:str, validator=None, castigator=None, max_retries:int=DEFAULT_MAX_RETRIES):
    """
    :param question:
    :param validator:     Function taking dict --> bool
    :param castigator:    Function taking castigator(question, response) --> str
    :param max_retries:
    :return:
    """
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


def castigate_until_numeric_dict(question:str, castigator=None, max_retries=DEFAULT_MAX_RETRIES):
    return castigate_until_valid(question=question, validator=validate_numeric_dict, max_retries=max_retries)


def castigate_until_numeric_dict_with_known_keys(valid_keys: STR_KEYS_TYPE,
                                                 question:str,
                                                 castigator=None,
                                                 max_retries=DEFAULT_MAX_RETRIES,
                                                 case_insensitive=True
                                                 ):
    """
    :param valid_keys:
    :param question:
    :param castigator:
    :param max_retries:
    :return:
    """
    def _validator(parsed_response: dict):
        return validate_numeric_dict_with_known_keys(parsed_response=parsed_response,
                                                     valid_keys=valid_keys,
                                                     case_insensitive=case_insensitive)
    return castigate_until_valid(question=question, castigator=castigator, validator=_validator, max_retries=max_retries)


def castigate_until_numeric_dict_with_known_keys_iteratively(valid_keys:STR_KEYS_TYPE,
                                                             question:str, castigator=None,
                                                             n_batch=5, randomize=False,
                                                             case_insensitive=True,
                                                             reverse=None) -> dict :
    """ Takes a list of valid_keys which are supposed to be assigned scores.
        Keeps iterating until all keys have been assigned numerical scores.

    :param valid_keys:     Dict or list or KeysView
    :param question:       'For the following presidents, provide a ranking of their popularity from 1 to 5 '
    :param castigator       Optional func taking  question, response arguments and returning str
    :param randomize        bool  whether to select items in random ordering
    :param n_batch          Number of scores to request per question
    :param case_insensitive If True, membership validation will be case insensitive
    :param reverse          If True, sorts reversed. If False, sorts. If None, does not sort.
    :return:
    """

    def _sort_dict_descending(d: dict, reverse:bool) -> dict:
        return dict(sorted(d.items(), key=lambda item: item[1], reverse=reverse))

    def _choose_next_items(items: list, count: int, randomize: bool) -> (List,List):
        # If the list has fewer items than requested, return the entire list
        if len(items) <= count:
            return items, []
        elif randomize:
            chosen = random.sample(items, count)
            remaining = [item for item in items if item not in chosen]
            return chosen, remaining
        else:
            return items[:count], items[count:]

    all_scores = dict()
    keys_left = [ k for k in list(valid_keys)]
    while keys_left:
        next_keys, keys_left = _choose_next_items(keys_left, count=n_batch, randomize=randomize)
        appended_question = question + ','.join([str(k).lower() for k in next_keys ])
        scores_dict = castigate_until_numeric_dict_with_known_keys(valid_keys=valid_keys,
                                                         question=appended_question,
                                                         castigator=castigator,
                                                         case_insensitive=case_insensitive
                                                         )
        if scores_dict is not None:
            all_scores.update(scores_dict)
            missing_keys = [ ky for ky in next_keys if not ky in scores_dict ]
            keys_left = list(missing_keys) + list(keys_left)
            print(f'  ...{len(keys_left)} keys remaining to be scored')
        else:
            print('   ... could not castigate a response this time')

    if reverse is not None:
        all_scores = _sort_dict_descending(all_scores, reverse=reverse)
    return all_scores



if __name__=='__main__':
    question = """
      I would like you to create a dictionary by choosing three tickers from companies
      that were in the sp500 index in 2011 and returning a dictionary with keys given by
      the tickers and values equal to a text description of the colors of the companies
      in question. 
    """
    d = castigate_until_valid(question=question)
    pprint(d)

