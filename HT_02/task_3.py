# Write a script which accepts a <number> from user and print out a sum of the first <number> positive integers.


n = int(input('Enter number: '))

print(sum(range(n + 1)))
