# task 6.
# Напишіть функцію,яка прймає рядок з декількох слів і повертає довжину найкоротшого слова.
# Реалізуйте обчислення за допомогою генератора.

def get_shorter_string(string: str) -> int:
    return min(len(st) for st in string.split())


if __name__ == '__main__':
    print('length of the shortest word: ', get_shorter_string('Напишіть функцію,яка прймає рядок з декількох слів і'))
    print('length of the shortest word: ', get_shorter_string('повертає довжину найкоротшого слова.'))
