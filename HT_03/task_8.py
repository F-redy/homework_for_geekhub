# 8. Створити цикл від 0 до ... (вводиться користувачем).
# В циклі створити умову, яка буде виводити поточне значення, якщо остача від ділення на 17 дорівнює 0.


user_input = int(input('Enter random number: '))

for num in range(user_input):
    if num % 17 == 0:
        print(num)
