
from chattychattybangbang.castigateuntilvalid import castigate_until_numeric_dict_with_known_keys_iteratively
from pprint import pprint

us_presidents = [
    "George Washington", "John Adams", "Thomas Jefferson", "James Madison", "James Monroe",
    "John Quincy Adams", "Andrew Jackson", "Martin Van Buren", "William Henry Harrison", "John Tyler",
    "James K. Polk", "Zachary Taylor", "Millard Fillmore", "Franklin Pierce", "James Buchanan",
    "Abraham Lincoln", "Andrew Johnson", "Ulysses S. Grant", "Rutherford B. Hayes", "James A. Garfield",
    "Chester A. Arthur", "Grover Cleveland", "Benjamin Harrison", "Grover Cleveland", "William McKinley",
    "Theodore Roosevelt", "William Howard Taft", "Woodrow Wilson", "Warren G. Harding", "Calvin Coolidge",
    "Herbert Hoover", "Franklin D. Roosevelt", "Harry S. Truman", "Dwight D. Eisenhower", "John F. Kennedy",
    "Lyndon B. Johnson", "Richard Nixon", "Gerald Ford", "Jimmy Carter", "Ronald Reagan",
    "George H.W. Bush", "Bill Clinton", "George W. Bush", "Barack Obama", "Donald Trump",
    "Joe Biden"
]

if __name__=='__main__':
    question = """For the following presidents, I would like you to provide a score from 1 to 10 representing their
                  appreciation of poetry. Provide a score of 1 if they dislike poetry. Provide a score of 10 if they
                  really loved poetry. Reply with a python dict and nothing else in your answer, please."""
    poetry_appreciation = castigate_until_numeric_dict_with_known_keys_iteratively(valid_keys=us_presidents,
                                                                                   question=question,
                                                                                   reverse=True)
    pprint(poetry_appreciation)