from utils.security import clean_input


def test_clean_input_basic():
    raw = "<b>Hello, WORLD!!</b>"
    out = clean_input(raw)
    assert isinstance(out, str)
    assert "hello" in out
    assert "<" not in out and ">" not in out
