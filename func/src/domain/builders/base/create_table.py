from abc import ABC, abstractmethod
from ...models.tables.base.model import TableFromList


class BaseTableBuilder(ABC):

    @staticmethod
    def _create_table_from_dict(table_cells: dict, table_name: str, color: str) -> str:
        table = f"""
        <table>
            <caption><b><i>{table_name}</i></b></caption>
            <tr>
                <th>Campo</th>
                <th>Valor</th>
            </tr>
            <tr>
            {'</tr><tr>'.join((f'''
               <td>{label}</td>
               <td>{value}</td>
            ''' for label, value in table_cells.items()))}
            </tr>
        </table>"""
        styled_table = BaseTableBuilder._style_table(table, color)
        return styled_table

    @staticmethod
    def _create_table_from_list(table_cells: TableFromList, table_name: str, color: str) -> str:
        table = f"""
        <table>
            <caption><b><i>{table_name}</i></b></caption>
            <tr>
                <th>{'</th><th>'.join(label for label in table_cells.columns)}</th>
            </tr>
            <tr>
            {'</tr><tr>'.join((
                f"<td>{'</td><td>'.join(map(str, (cell for cell in row)))}</td>"
            for row in table_cells.rows))}
            </tr>
        </table>"""
        styled_table = BaseTableBuilder._style_table(table, color)
        return styled_table

    @classmethod
    def _style_table(cls, table: str, color: str) -> str:
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
            border: 3px solid {color};
            background: {color};
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

    @abstractmethod
    def build(self) -> str:
        pass
