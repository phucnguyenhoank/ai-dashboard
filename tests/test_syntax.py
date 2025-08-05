# test_syntax.py
def test_t1():
    a = {
        "name": "fine",
        "nguyen": "sam"
    }
    print({**a})
    assert {"id": "123", **a} == {"id": "123", "name": "fine", "nguyen": "sam"}