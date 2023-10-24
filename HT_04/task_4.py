# task 4.
# Write a Python program that demonstrates exception chaining.
# Create a custom exception class called CustomError and another called SpecificError.
# In your program (could contain any logic you want), raise a SpecificError,
# and then catch it in a try/except block, re-raise it as a CustomError with the original exception as the cause.
# Display both the custom error message and the original exception message.

class CustomError(Exception):
    pass


class SpecificError(Exception):
    pass


try:
    sleep = 'I want to sleep. And the program logic goes away..'
    raise SpecificError('some kind of SpecificError')
except SpecificError as specific_error:
    try:
        raise CustomError('An error occurred in the custom logic.') from specific_error
    except CustomError as custom_error:
        print(f'Custom error message: {custom_error}')
        print(f'Original exception message: {specific_error}')
