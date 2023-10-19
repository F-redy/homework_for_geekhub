# 9. Користувачем вводиться початковий і кінцевий рік.
# Створити цикл, який виведе всі високосні роки в цьому проміжку (границі включно).
# P.S. Рік є високосним, якщо він кратний 4, але не кратний 100, а також якщо він кратний 400.


start_year = int(input('Enter start year: '))
end_year = int(input('Enter finish year \033[31m(must be more start year)\033[0m: '))

for year in range(start_year, end_year + 1):
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        print(year, end=' ')
