# task 5.
# Напишіть функцію,яка приймає на вхід рядок та повертає кількість окремих регістро-незалежних букв та цифр,
# які зустрічаються в рядку більше ніж 1 раз. Рядок буде складатися лише з цифр та букв (великих і малих).
# Реалізуйте обчислення за допомогою генератора.
#     Example (input string -> result):
#     "abcde" -> 0            # немає символів, що повторюються
#     "aabbcde" -> 2          # 'a' та 'b'
#     "aabBcde" -> 2          # 'a' присутнє двічі і 'b' двічі (`b` та `B`)
#     "indivisibility" -> 1   # 'i' присутнє 6 разів
#     "Indivisibilities" -> 2 # 'i' присутнє 7 разів та 's' двічі
#     "aA11" -> 2             # 'a' і '1'
#     "ABBA" -> 2             # 'A' і 'B' кожна двічі

def get_count_unique_letters(string: str) -> int:
    string = string.lower()
    return sum(1 for letter in set(string) if string.count(letter) > 1)


if __name__ == '__main__':
    tests = [
        ("abcde", 0),
        ("aabbcde", 2),
        ("aabBcde", 2),
        ("indivisibility", 1),
        ("Indivisibilities", 2),
        ("aA11", 2),
        ("ABBA", 2)
    ]

    for indx, (example, answer) in enumerate(tests):
        result = get_count_unique_letters(example)
        assert result == answer, f'TEST №{indx + 1} - ERROR!\n{result} != {answer}\nERROR in:\n {example}'
        print(f'TEST №{indx + 1} - OK: Result = {result}')
