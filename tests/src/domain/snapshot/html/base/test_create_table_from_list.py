from unittest.mock import patch
from func.src.domain.snapshot.html.base.create_table_from_list import TableFromListDTO
from func.src.domain.snapshot.model import Cell

dummy_empty_user_data = []


def test_create_table_without_user_data():
    response = TableFromListDTO.create_table(dummy_empty_user_data)
    assert response == ""


dummy_user_data = [
    [Cell(label="Field 1", value=159159), Cell(label="Field 2", value=951159)],
    [Cell(label="Field 3", value=159159), Cell(label="Field 4", value=951159)]
]
dummy_table_name = "Table Name"
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


@patch.object(TableFromListDTO, "_style_table", side_effect=lambda x: x)
def test_create_table(mocked_table_style):
    setattr(TableFromListDTO, "_table_name", dummy_table_name)
    response = TableFromListDTO.create_table(dummy_user_data)
    assert response == expected_table

