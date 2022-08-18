from src.domain.models.snapshot.input.warranty import WarrantyResume

dummy_value = "value"
stub_warranty = {"available": dummy_value}


def test_instance_with_content():
    warranty = WarrantyResume(**stub_warranty)
    assert warranty.available == dummy_value


def test_instance_empty():
    warranty = WarrantyResume()
    assert warranty.available is None




