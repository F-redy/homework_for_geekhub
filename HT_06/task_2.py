# task 2.
# Написати функцію <bank> , яка працює за наступною логікою:
# користувач робить вклад у розмірі <a> одиниць строком на <years> років під <percents> відсотків
# (кожен рік сума вкладу збільшується на цей відсоток,
# ці гроші додаються до суми вкладу і в наступному році на них також нараховуються відсотки).
# Параметр <percents> є необов'язковим і має значення по замовчуванню <10> (10%).
# Функція повинна принтануть суму, яка буде на рахунку, а також її повернути (але округлену до копійок).


def bank(deposit: int, years: int, percents: int = 10) -> float:
    for _ in range(years):
        deposit += deposit * percents / 100
    result_deposit = round(deposit, 2)
    print(f'The amount in the account after {years} years: {result_deposit}')
    return result_deposit


if __name__ == '__main__':
    print(bank(1000, 5, 17))
    print(bank(40000, 5))
