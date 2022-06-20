from func.src.repository.snapshot.base.create_table import BaseTableBuilder


class TableFromDictBuilder(BaseTableBuilder):
    _table_name: str
    _table_color: str

    @classmethod
    def create_table(cls, user_data: dict):
        if not user_data:
            return ""
        table = f"""
        <table>
            <caption><b><i>{cls._table_name}</i></b></caption>
            <tr>
                <th>{'</th><th>'.join(('Campo', 'Valor'))}</th>
            </tr>
            <tr>
            {'</tr><tr>'.join((f'''
               <td>{field}</td>
               <td>{value}</td>
            ''' for field, value in user_data.items()))}
            </tr>
        </table>"""
        styled_table = cls._style_table(table)
        return styled_table
