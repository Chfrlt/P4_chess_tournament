from typing import Union


def input_is_valid_as_an_int(raw_input: str) -> bool:
    '''Check if user input is valid as an int and, if so,
    return bool True'''
    try:
        int(raw_input)
        return True
    except ValueError as e:
        error_invalid_user_input(e)


def error_invalid_user_input(error: Union[ValueError, IndexError]):
    if isinstance(error, ValueError):
        print('Invalid Input. Must be a number')
    elif isinstance(error, IndexError):
        print("Input didn't match any options")
    else:
        return


def get_input_for_selectors(max_index: int) -> int:
    '''takes user input, check if it is a valid int and
    if it is inferior to the max index.
    If both conditions are met, returns the index'''
    raw_input = input(' >> ')
    if input_is_valid_as_an_int(raw_input) is True:
        index = int(raw_input) - 1
        if index > max_index:
            error_invalid_user_input(error=IndexError)
        else:
            return index
