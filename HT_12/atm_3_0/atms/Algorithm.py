class Algorithm:
    @staticmethod
    def get_available_denomination(amount: int, currency: dict) -> dict:
        """ Оставляем только нужные номиналы """
        return {denomination: quantity
                for denomination, quantity in currency.items()
                if denomination <= amount and quantity > 0}

    def greedy_algorithm(self, amount: int, currency: dict) -> dict:
        """ Жадный алгоритм выдачи суммы """
        available_denominations = self.get_available_denomination(amount, currency)
        sorted_denominations = sorted(available_denominations.keys(), reverse=True)
        selected_denominations = {}
        for current_denomination in sorted_denominations:
            if amount >= current_denomination:
                max_quantity = min(amount // current_denomination, available_denominations.get(current_denomination))
                selected_denominations[current_denomination] = max_quantity
                amount -= current_denomination * max_quantity
        return selected_denominations

    def dynamic_algorithm(self, amount: int, currency: dict) -> dict:
        """
         Динамический алгоритм выдачи суммы

         подсмотрено: https://github.com/codedokode/pasta/blob/master/algorithm/atm.md
        """
        available_denominations = self.get_available_denomination(amount, currency)
        sorted_denominations = sorted(
            [denomination for denomination, quantity in available_denominations.items() for _ in range(quantity)],
            reverse=True)

        possible_sums = {0: 0}
        for denomination in sorted_denominations:
            new_sums = {}
            for current_sum in possible_sums.keys():
                new_sum = current_sum + denomination

                if new_sum > amount:
                    continue
                elif new_sum not in possible_sums.keys():
                    new_sums[new_sum] = denomination

            possible_sums.update(new_sums)
            if amount in possible_sums.keys():
                break

        remaining_amount = amount
        used_denominations = []

        try:
            while remaining_amount > 0:
                used_denominations.append(possible_sums[remaining_amount])
                remaining_amount -= possible_sums[remaining_amount]

            selected_denominations_count = {denomination: used_denominations.count(denomination)
                                            for denomination in used_denominations}

            return selected_denominations_count
        except KeyError:
            return {0: 0}

    @staticmethod
    def get_sum_currency(currency: dict):
        """
        Вычисляет общую сумму денежных средств в банкомате на основе данных о наличности.

        Args:
            currency (dict): Словарь, содержащий информацию о наличности в банкомате, где ключ - номинал купюры,
                             значение - количество купюр данного номинала.

        Returns:
            int: Общая сумма денежных средств в банкомате, вычисленная на основе данных о наличности.
        """
        return sum([denomination * quantity for denomination, quantity in currency.items()])

    def count_cash(self, amount: int, currency: dict) -> dict | None:
        """
           Подсчитывает минимальное количество монет для запрошенной суммы.

           Args:
               amount (int): Запрошенная сумма, для которой необходимо подсчитать минимальное количество монет.
               currency (dict): Имеющаяся валюта в банкомате.

           Returns:
               dict or None: Словарь, содержащий минимальное количество монет каждого номинала для суммы.
               Если подсчет невозможен, возвращается None.

           Метод сначала использует жадный алгоритм для подсчета минимального количества монет.
           Если жадный алгоритм не выдает нужную сумму, то применяется динамический алгоритм,
           который может вернуть необходимую сумму монет.
           В итоге возвращается результат с монетами, минимальное количество которых необходимо для указанной суммы.
           """
        greedy_result = self.greedy_algorithm(amount, currency)
        result = greedy_result
        greedy_sum = self.get_sum_currency(greedy_result)
        if greedy_sum != amount:
            dynamic_result = self.dynamic_algorithm(amount, currency)
            dynamic_sum = self.get_sum_currency(dynamic_result)
            if dynamic_sum == amount:
                result = dynamic_result

        if self.get_sum_currency(result) == amount:
            return dict(sorted(result.items(), reverse=True))

        return

    @staticmethod
    def show_withdrawn_money(withdrawn_money: dict) -> None:
        line = '-' * 24
        print(f'\n{line}\nВыданные купюры:')
        for denomination, quantity in withdrawn_money.items():
            print(f'{"":<5}{denomination:<6} |{"":>3} {quantity}')
        print(line)
