from ..base.create_table_from_list import TableFromListDTO


class BlockedAssetsTableDTO(TableFromListDTO):
    _table_name = "Ativos Bloqueados"
    _table_color = "darkred"
