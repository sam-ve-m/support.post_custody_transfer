from typing import List

from ..base.create_table import BaseTableDTO
from ...model import Cell


class TableFromDictDTO(BaseTableDTO):
    _table_name: str
    _table_color: str

    @classmethod
    def create_table(cls, user_data: List[Cell]):
        if not user_data:
            return ""
        table = f"""
        <table>
            <caption><b><i>{cls._table_name}</i></b></caption>
            <tr>
                <th>Campo</th>
                <th>Valor</th>
            </tr>
            <tr>
            {'</tr><tr>'.join((f'''
               <td>{field.label}</td>
               <td>{field.value}</td>
            ''' for field in user_data))}
            </tr>
        </table>"""
        styled_table = cls._style_table(table)
        return styled_table
