from func.src.repository.snapshot.base.create_table_from_list import TableFromListBuilder


class BlockedAssetsTableBuilder(TableFromListBuilder):
    _table_name = "Ativos Bloqueados"
    _table_color = "darkred"
