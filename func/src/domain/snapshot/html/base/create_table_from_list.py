from typing import List

from func.src.domain.snapshot.html.base.create_table import BaseTableDTO
from func.src.domain.snapshot.model import Row


class TableFromListDTO(BaseTableDTO):
    _table_name: str
    _table_color: str

    @classmethod
    def create_table(cls, user_data: List[Row]):
        if not user_data:
            return ""
        table = f"""
        <table>
            <caption><b><i>{cls._table_name}</i></b></caption>
            <tr>
                <th>{'</th><th>'.join(cell.label for cell in user_data[0])}</th>
            </tr>
            <tr>
            {'</tr><tr>'.join((
                f"<td>{'</td><td>'.join(map(str, (cell.value for cell in row)))}</td>"
            for row in user_data))}
            </tr>
        </table>"""
        styled_table = cls._style_table(table)
        return styled_table
