from typing import List

from func.src.repository.snapshot.base.create_table import BaseTableBuilder


class TableFromListBuilder(BaseTableBuilder):
    _table_name: str
    _table_color: str

    @classmethod
    def create_table(cls, user_data: List[dict]):
        if not user_data:
            return ""
        table = f"""
        <table>
            <caption><b><i>{cls._table_name}</i></b></caption>
            <tr>
                <th>{'</th><th>'.join(user_data[0].keys())}</th>
            </tr>
            <tr>
            {'</tr><tr>'.join((
                f"<td>{'</td><td>'.join(map(str, dictionary.values()))}</td>"
            for dictionary in user_data))}
            </tr>
        </table>"""
        styled_table = cls._style_table(table)
        return styled_table
