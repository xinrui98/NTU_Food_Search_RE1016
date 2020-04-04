import string


def error_handler():
    print("this is an error message")

def ask_for_user_input(function_number):
    if function_number==1:
        user_input = input("Hello, please input intended keywords, e.g. Western Chicken: ")
        return user_input

def capitalise_first_letter(word):
    return string.capwords(word)

def error_handling_no_type_of_food(number_of_relevant_searches_found):
    if number_of_relevant_searches_found==0:
        print("No food stalls found with input keyword(s), please try again")
        return True