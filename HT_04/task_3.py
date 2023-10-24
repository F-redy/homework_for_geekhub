# task 3.
# Create a Python script that takes an age as input.
# If the age is less than 18 or greater than 120, raise a custom exception called InvalidAgeError.
# Handle the InvalidAgeError by displaying an appropriate error message.


MIN_AGE = 18
MAX_AGE = 120


class InvalidAgeError(Exception):
    pass


def check_age(age: int):
    if not (MIN_AGE <= age <= MAX_AGE):
        message = ('You are too young for this shit...', 'Who are you, warrior?')[age > MAX_AGE]
        raise InvalidAgeError(message)
    print('Great!')


try:
    user_age = int(input('Enter your age: '))
    check_age(user_age)
except ValueError as e:
    print(e)
except InvalidAgeError as e:
    print(e)
