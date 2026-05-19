from view.table import render_table


def test_render_table_basic():
    headers = ['A', 'B']
    rows = [(1, 'x'), (2, 'y')]
    out = render_table(headers, rows)
    assert 'A' in out and 'B' in out
    assert '1' in out and 'x' in out
