from HT_12.atm_3_0.database_operations.atm.DataBaseATM import DataBaseATM
from HT_12.atm_3_0.database_operations.atm.DataBaseATMBalance import \
    DataBaseATMBalance
from HT_12.atm_3_0.database_operations.atm.DataBaseATMCurrency import \
    DataBaseATMCurrency


class ATMDataBase(DataBaseATM, DataBaseATMBalance, DataBaseATMCurrency):
    pass
