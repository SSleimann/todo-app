from app.kernel.domain.value_objects import ValueUUID


def test_value_uuid_type():
    obj = ValueUUID.next_id()
    assert isinstance(obj, ValueUUID)
    assert str(obj) is not None
