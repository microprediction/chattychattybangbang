import json

def json_or_none(response):
    try:
        parsed_response = json.loads(response)
        return parsed_response
    except json.JSONDecodeError:
        return None


def extract_dict_str(input_string):
    import re
    pattern = r'\{(.*?)\}'
    result = re.search(pattern, input_string, re.DOTALL)
    if result:
        extracted_string = result.group(1)
        return '{' + extracted_string + '}'
    else:
        return ""