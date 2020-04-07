import string


def error_handler():
    print("this is an error message")

def capitalise_first_letter(word):
    return string.capwords(word)

def error_handling_no_type_of_food(number_of_relevant_searches_found):
    if number_of_relevant_searches_found==0:
        print("No food stalls found with input keyword(s), please try again")
        return True