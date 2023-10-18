# Write a script which accepts a <number> from user and print out a sum of the first <number> positive integers.


def get_sum_numbers(list_numbers: list[int], user_number: int) -> int:
    return sum(list_numbers[1:user_number + 1])


n = int(input('Enter number: '))
numbers = [i for i in range(n)]

sum_numbers = get_sum_numbers(list_numbers=numbers, user_number=n)

print(sum_numbers)
