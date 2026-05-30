import json
import importlib


def test_chatbot_known_unknown(tmp_path, monkeypatch):
    data = [
        {"question": "what is python", "answer": "Python is a language"},
        {"question": "what is numpy", "answer": "NumPy for numeric"}
    ]
    dfile = tmp_path / "dataset.json"
    dfile.write_text(json.dumps(data, ensure_ascii=False))
    monkeypatch.chdir(tmp_path)
    import model
    importlib.reload(model)
    bot = model.Chatbot()
    assert "python" in bot.get_response("what is python").lower()
    assert "sorry" in bot.get_response("qwerty unrelated").lower()
