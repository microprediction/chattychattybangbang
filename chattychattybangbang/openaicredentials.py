import os
import openai


def set_credentials(api_key=None):
    if api_key is None:
        try:
            from chattychattybangbang.privatecredentials import API_KEY  # noqa: E402
            openai.api_key = API_KEY
        except ImportError:
            api_key = os.environ.get('OPEN_AI_KEY')
            if api_key is None:
                raise Exception('Create privatecredential.py with API_KEY please, or OPEN_AI_KEY env var')
            else:
                openai.api_key = api_key
    else:
        openai.api_key = api_key
