import openai
import json
from hypothesis import given
from hypothesis.strategies import dictionaries, text
from credentials import set_credentials
set_credentials()

# Implements retrys until the response meets a validator


def ask_gpt(question):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=question,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()



def parse_response(response):
    try:
        parsed_response = json.loads(response)
        return parsed_response
    except json.JSONDecodeError:
        return None


@given(dictionaries(keys=text(), values=text()))
def validate_response(parsed_response):
    # Add your validation code here
    return True


def generate_follow_up_question(question, response):
    # Add logic to create a follow-up question based on the previous response
    follow_up_question = f"Please reformat the response to the question '{question}' as a dictionary with the following keys: key1, key2, key3."
    return follow_up_question



MAX_RETRIES = 3


def ask_with_format_retry(question:str, validator):

    retries = 0

    while retries < MAX_RETRIES:
        response = ask_gpt(question)
        parsed_response = parse_response(response)

        if parsed_response and validate_response(parsed_response):
            break

        question = generate_follow_up_question(question, response)
        retries += 1

    if retries == MAX_RETRIES:
        print("Failed to get a valid response.")
    else:
        print("Valid response:", parsed_response)

