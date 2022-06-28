from func.src.domain.snapshot.html.base.create_table_from_dict import TableFromDictDTO
from unittest.mock import patch

from func.src.domain.snapshot.model import Cell

dummy_empty_user_data = {}


def test_create_table_without_user_data():
    response = TableFromDictDTO.create_table(dummy_empty_user_data)
    assert response == ""


dummy_user_data = [Cell(label="Field 1", value=159159), Cell(label="Field 2", value=951159)]
dummy_table_name = "Table Name"
expected_table = """
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


@patch.object(TableFromDictDTO, "_style_table", side_effect=lambda x: x)
def test_create_table(mocked_table_style):
    setattr(TableFromDictDTO, "_table_name", dummy_table_name)
    response = TableFromDictDTO.create_table(dummy_user_data)
    assert response == expected_table

