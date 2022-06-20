from abc import ABC, abstractmethod
from typing import List


class BaseTableBuilder(ABC):
    _table_name: str
    _table_color: str

    @classmethod
    @abstractmethod
    def create_table(cls, user_data: dict):
        pass

    @classmethod
    def _style_table(cls, table: str) -> str:
        table = table.replace("<table>", f'''<table style="display: inline-table;
            border-collapse: collapse;
            border-spacing: 0;
            border: 3px solid black;
            table-layout: fixed;
            width: max-content;
            min-width: 400px;
            border-top: 0px
        ">''').replace("<b>", f'''<b style="text-align: center;
            display: block !important;
            border: 3px solid {cls._table_color};
            background: {cls._table_color};
            color: white
        ">''').replace("<th>", f'''<th style="padding: 0px 5px;
            border: 1px solid black;
            align-content: center;
            text-align: center
        ">''').replace("<td>", f'''<td style="padding: 1px 5px;
            border: 1px solid black;
            align-content: center;
            text-align: center
        ">''')
        return f'<div style="display: inline-block">{table}</div>'
