from HT_12.atm_3_0.database_operations.users.DataBaseTransaction import \
    DataBaseTransaction
from HT_12.atm_3_0.database_operations.users.DataBaseUser import DataBaseUser


class UserDB(DataBaseUser, DataBaseTransaction):
    """
        Объединенный класс для работы с пользователями и транзакциями пользователей.

        Данный класс наследует методы для работы с пользователями (добавление, получение информации, удаление)
        и транзакциями (создание, получение транзакций пользователя).

        Attributes:
            Методы классов DataBaseUser и DataBaseTransaction, которые можно использовать
            для управления пользователями и их транзакциями в базе данных.

        Note:
            Для подробного описания каждого метода обратитесь к соответствующей документации
            классов DataBaseUser и DataBaseTransaction.

        """
    pass
