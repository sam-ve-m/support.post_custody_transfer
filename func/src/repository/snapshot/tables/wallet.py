from func.src.repository.snapshot.base.create_table_from_list import TableFromListBuilder


class WalletTableBuilder(TableFromListBuilder):
    _table_name = "Carteira"
    _table_color = "purple"
