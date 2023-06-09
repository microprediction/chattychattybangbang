from chattychattybangbang.openaicredentials import set_credentials
from chattychattybangbang.validators import default_validator, validate_numeric_dict
from chattychattybangbang.validators import validate_numeric_dict_with_known_keys, STR_KEYS_TYPE, is_in
from chattychattybangbang.jsonutil import json_or_none, extract_dict_str
from chattychattybangbang.castigators import default_castigator
from chattychattybangbang.openutil import ask_gpt
import random
from typing import List
from pprint import pprint

DEFAULT_MAX_RETRIES = 3


def castigate_until_valid(question:str, validator=None, castigator=None,
                          max_retries:int=DEFAULT_MAX_RETRIES, echo=False):
    """
    :param question:
    :param validator:     Function taking dict --> bool
    :param castigator:    Function taking castigator(question, response) --> str
    :param max_retries:
    :param echo:          Print the responses to stdout
    :return:
    """


    if validator is None:
        validator = default_validator
    if castigator is None:
        castigator = default_castigator

    retries = 0
    failure_print_count = 5

    while retries < max_retries:
        raw_response = ask_gpt(question)
        trimmed_response = extract_dict_str(raw_response)
        parsed_response = json_or_none(trimmed_response)

        if parsed_response and validator(parsed_response):
            break

        # If fail, maybe print the question and response for debugging
        if echo and failure_print_count>0:
            print('      ... example question: ')
            print(question)
            print('      ... example of failed response >> ')
            print(raw_response)
            print('       ... << ')
            failure_print_count -= 1

        # Modify the question
        question = castigator(question, raw_response)
        retries += 1

    if retries == max_retries:
        return None
    else:
        return parsed_response


def castigate_until_numeric_dict(question:str, castigator=None, max_retries=DEFAULT_MAX_RETRIES, echo=False):
    return castigate_until_valid(question=question, validator=validate_numeric_dict, max_retries=max_retries, echo=echo)


def castigate_until_numeric_dict_with_known_keys(valid_keys: STR_KEYS_TYPE,
                                                 question:str,
                                                 castigator=None,
                                                 max_retries=DEFAULT_MAX_RETRIES,
                                                 case_insensitive=True,
                                                 echo = False
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

    d = castigate_until_valid(question=question, castigator=castigator,
                                 validator=_validator, max_retries=max_retries,
                                 echo=echo)
    return dict([(k,float(v)) for k,v in d.items()])


def castigate_until_numeric_dict_with_known_keys_iteratively(valid_keys:STR_KEYS_TYPE,
                                                             question:str, castigator=None,
                                                             n_batch=5, randomize=False,
                                                             max_retries = 5,
                                                             case_insensitive=True,
                                                             reverse=None,
                                                             skip=True,echo=False) -> dict :
    """ Takes a list of valid_keys which are supposed to be assigned scores.
        Keeps iterating until all keys have been assigned numerical scores.

    :param valid_keys:     Dict or list or KeysView
    :param question:       'For the following presidents, provide a ranking of their popularity from 1 to 5 '
    :param castigator       Optional func taking  question, response arguments and returning str
    :param randomize        bool  whether to select items in random ordering
    :param n_batch          Number of scores to request per question
    :param case_insensitive If True, membership validation will be case insensitive
    :param skip             If True, will skip over a batch that fails completely
    :param reverse          If True, sorts reversed. If False, sorts. If None, does not sort.
    :return:
    """

    def _sort_dict_descending(d: dict, reverse: bool) -> dict:
        try:
            return dict(sorted(d.items(), key=lambda item: item[1], reverse=reverse))
        except TypeError:
            try:
                return dict(sorted(d.items(), key=lambda item: float(item[1]), reverse=reverse))
            except TypeError:
                return dict(sorted(d.items(), key=lambda item: str(item[1]), reverse=reverse))

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
    printed_question = False
    import time
    while keys_left:
        time.sleep(0.01)
        next_keys, keys_left = _choose_next_items(keys_left, count=n_batch, randomize=randomize)
        instruct_keys = 'Here is the list: '+ ','.join(next_keys)+' .'
        instruct_head = ' So the output you give me should look like the following :'
        instruct_example = '{'+ ','.join( [ f'"{key}": 0' for key in next_keys ] )+ '}'
        instruct_tail = ' except that the zeros should be replaced by values as instructed.'
        instruct = question + instruct_keys + instruct_head + instruct_example + instruct_tail
        if echo and not printed_question:
            print('Question :' + instruct)
            printed_question = True
        scores_dict = castigate_until_numeric_dict_with_known_keys(valid_keys=next_keys,
                                                         question=instruct,
                                                         castigator=castigator,
                                                         case_insensitive=case_insensitive,
                                                                   max_retries=max_retries, echo=echo
                                                         )
        if scores_dict is not None:
            all_scores.update(scores_dict)
            if case_insensitive:
                missing_keys = [ky for ky in next_keys if not is_in(ky,scores_dict)]
            else:
                missing_keys = [ ky for ky in next_keys if ky not in scores_dict ]
            print(f'  ... successfully added scores for '+','.join(list(scores_dict.keys())))

        else:
            print('   ... failed to get a response after retries for ' + ','.join(next_keys))
            if skip:
                import numpy as np
                scores_dict = dict([ (k,np.nan) for k in next_keys ])
                all_scores.update(scores_dict)
                missing_keys = []
                print('       ... giving up on them')
            else:
                missing_keys = [k for k in next_keys]
        keys_left = list(missing_keys) + list(keys_left)
        print(f'  ...{len(keys_left)} keys remaining to be scored')

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

