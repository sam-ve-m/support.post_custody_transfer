from unittest.mock import patch

from src.domain.builders.base.create_table import BaseTableBuilder
from src.domain.models.tables.base.model import TableFromList

dummy_table = "<table><b><th><td>"
dummy_table_name = "Table Name"
dummy_color = "Color"


def test_style_table():
    styled_table = BaseTableBuilder._style_table(dummy_table, "dummy")
    assert '<div style="display: inline-block">' in styled_table
    assert '<table style="' in styled_table
    assert '<b style="' in styled_table
    assert '<th style="' in styled_table
    assert '<td style="' in styled_table


dummy_empty_user_data = TableFromList(columns=[], rows=[])
expected_empty_table = """
        <table>
            <caption><b><i>Table Name</i></b></caption>
            <tr>
                <th></th>
            </tr>
            <tr>
            
            </tr>
        </table>"""


@patch.object(BaseTableBuilder, "_style_table", side_effect=lambda x, *args: x)
def test_create_table_from_list_without_user_data(mocked_style):
    response = BaseTableBuilder._create_table_from_list(dummy_empty_user_data, dummy_table_name, dummy_color)
    assert response == expected_empty_table


dummy_user_data = TableFromList(columns=["Field 1", "Field 2"], rows=[[159159, 951159], [159159, 951159]])
expected_table = """
        <table>
            <caption><b><i>Table Name</i></b></caption>
            <tr>
                <th>Field 1</th><th>Field 2</th>
            </tr>
            <tr>
            <td>159159</td><td>951159</td></tr><tr><td>159159</td><td>951159</td>
            </tr>
        </table>"""


@patch.object(BaseTableBuilder, "_style_table", side_effect=lambda x, *args: x)
def test_create_table_from_list(mocked_table_style):
    response = BaseTableBuilder._create_table_from_list(dummy_user_data, dummy_table_name, dummy_color)
    assert response == expected_table


dummy_empty_user_dict = {}
expected_empty_table_with_collumns = """
        <table>
            <caption><b><i>Table Name</i></b></caption>
            <tr>
                <th>Campo</th>
                <th>Valor</th>
            </tr>
            <tr>
            
            </tr>
        </table>"""


@patch.object(BaseTableBuilder, "_style_table", side_effect=lambda x, *args: x)
def test_create_table_from_dict_without_user_data(mocked_style):
    response = BaseTableBuilder._create_table_from_dict(dummy_empty_user_dict, dummy_table_name, dummy_color)
    assert response == expected_empty_table_with_collumns


dummy_user_data_dict = {"Field 1": 159159, "Field 2": 951159}
expected_table_dict = """
        <table>
            <caption><b><i>Table Name</i></b></caption>
            <tr>
                <th>Campo</th>
                <th>Valor</th>
            </tr>
            <tr>
            
               <td>Field 1</td>
               <td>159159</td>
            </tr><tr>
               <td>Field 2</td>
               <td>951159</td>
            
            </tr>
        </table>"""


@patch.object(BaseTableBuilder, "_style_table", side_effect=lambda x, *args: x)
def test_create_table_from_dict(mocked_table_style):
    response = BaseTableBuilder._create_table_from_dict(dummy_user_data_dict, dummy_table_name, dummy_color)
    assert response == expected_table_dict
