from src.domain.models.snapshot.input.blocks import Blocks

dummy_value = "value"
stub_blocks = {
    "date": dummy_value,
    "block_type": dummy_value,
    "description": dummy_value,
    "lawsuit_number": dummy_value,
}


def test_instance_with_content():
    blocks = Blocks.from_dict(stub_blocks)
    assert blocks.date == dummy_value
    assert blocks.block_type == dummy_value
    assert blocks.description == dummy_value
    assert blocks.lawsuit_number == dummy_value


def test_instance_empty():
    blocks = Blocks.from_dict(None)
    assert blocks.date is None
    assert blocks.block_type is None
    assert blocks.description is None
    assert blocks.lawsuit_number is None




