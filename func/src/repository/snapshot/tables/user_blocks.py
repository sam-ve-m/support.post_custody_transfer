from func.src.repository.snapshot.base.create_table_from_dict import BaseTableBuilder, TableFromDictBuilder


class UserBlocksTableBuilder(TableFromDictBuilder):
    _table_name = "Bloqueio"
    _table_color = "darkred"
