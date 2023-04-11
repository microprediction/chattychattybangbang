import json

def json_or_none(response):
    try:
        parsed_response = json.loads(response)
        return parsed_response
    except json.JSONDecodeError:
        return None
