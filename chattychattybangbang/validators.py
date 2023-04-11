from hypothesis import given
from hypothesis.strategies import dictionaries, text

# Example validators

def validate_text_dict(parsed_response:dict):
    return True


def validate_yes_or_no(parsed_response:dict):
    value = list(parsed_response.values())[0]
    return isinstance(value,str) and (('yes' in value.lower()) or ('no' in value.lower()))


default_validator = validate_text_dict

