def error_handler():
    print("this is an error message")

def ask_for_user_input(function_number):
    if function_number==1:
        user_input = input("Hello, please input intended keywords, e.g. Western Chicken: ")
        return user_input
