import random
from chattychattybangbang.jsonutil import extract_dict_str, json_or_none


def castigate_dict_text(question, response):
    # Add logic to create a follow-up question based on the previous response

    choices = [f"Please reformat the response to the question '{question}' as a dictionary.",
               "I did not mean for you to answer with a dict whose every value is zero. That was just an example.",
               "Please provide the response as a dictionary, as requested, and provide nothing else in the response",
               r"I am going to repeat the question as this answer is not correct. Here is the question again +{question}"]

    try:
        d = json_or_none(extract_dict_str(response))
    except:
        d = None

    if d is not None:
        if isinstance(d, dict) and len(d):
            if all([v == 0 for k, v in d.items()]):
                return choices[3]

    follow_up_question = random.choice(choices)
    return follow_up_question


default_castigator = castigate_dict_text
