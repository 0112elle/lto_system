from view.formatters import format_license, format_registration, format_violation


def test_format_license():
    row = ('L-12345', 'Student', 'Active', '2020-01-01', '2025-01-01', 'A,B', 'None')
    out = format_license(row)
    assert 'L-12345' in out
    assert 'Student' in out
    assert 'Expires' in out or '2025-01-01' in out


def test_format_registration():
    row = ('R-0001', '2023-01-01', '2024-01-01', 'active', 'OR-001', '2023-01-02', None, 'owned', None, '2023-01-01', None, 10)
    out = format_registration(row)
    assert 'R-0001' in out
    assert 'OR-001' in out
    assert 'Vehicle' in out


def test_format_violation():
    row = (1, '2024-04-01', 500.0, 'unpaid', 'Speeding', 'ABC123', 'Metro Manila', 'NCR')
    out = format_violation(row)
    assert 'Violation 1' in out
    assert 'Speeding' in out
    assert 'Metro Manila' in out
