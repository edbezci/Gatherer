from gatherer import gatherer


def test_gatherer(monkeypatch):
    test_query = "machine learning"
    test_amount = 20
    resps = iter([test_query, test_amount])
    monkeypatch.setattr("builtins.input", lambda msg: next(resps))
    test_gath = gatherer()
    test_df = test_gath.gather()
    assert test_df.shape == (test_amount, 5)
