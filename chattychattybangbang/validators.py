from hypothesis import given
from hypothesis.strategies import dictionaries, text
from typing import Dict, List, Union, KeysView, Any

# Example validators


def validate_text_dict(parsed_response:dict):
    return isinstance(parsed_response,dict)


def validate_numeric_dict(parsed_response:dict):
    try:
        for k,v in parsed_response.items():
            v_float = float(v)
        return True
    except Exception as e:
        return False


STR_KEYS_TYPE = Union[List[str], Dict[str, Any], KeysView[str]]


def validate_numeric_dict_with_known_keys(parsed_response: dict,
                                          valid_keys:STR_KEYS_TYPE,
                                          case_insensitive=True):

    def _is_in(s: str, string_set: set) -> bool:
        # Case-insensitive membership
        s_lower = s.lower()
        lower_set = {item.lower() for item in list(string_set)}
        return s_lower in lower_set

    try:
        for k, v in parsed_response.items():
            v_float = float(v)
            if case_insensitive:
                assert _is_in(k, valid_keys)
            else:
                assert k in valid_keys

        return True
    except Exception as e:
        return False


def validate_yes_or_no(parsed_response:dict):
    value = list(parsed_response.values())[0]
    return isinstance(value,str) and (('yes' in value.lower()) or ('no' in value.lower()))


default_validator = validate_text_dict

