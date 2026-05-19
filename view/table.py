from typing import List, Sequence, Iterable

def render_table(headers: Sequence[str], rows: Iterable[Sequence], max_col_width: int = 60) -> str:
    print('')
    # build string table and return it (also printable)
    cols = len(headers)
    # force rows into a list so we can sort and iterate multiple times
    rows_list = list(rows)

    # Attempt to detect a primary key column from headers (common patterns)
    pk_idx = None
    common_ids = set(['id','driver_id','driverid','violation_id','violationid','license_id','licenseid','vehicle_id','vehicleid','registration_id','registrationid'])
    for i, h in enumerate(headers):
        hn = h.lower() if h else ''
        if hn in common_ids or hn.endswith('_id') or hn == 'id':
            pk_idx = i
            break

    # convert rows to string cells and normalize lengths
    data = [list(map(lambda x: '' if x is None else str(x), row)) for row in rows_list]

    # if we found a pk column, sort data ascending by that column when possible
    if pk_idx is not None:
        def _key(r):
            try:
                v = r[pk_idx]
                if v is None or v == '':
                    return float('inf')
                return int(v)
            except Exception:
                try:
                    return str(r[pk_idx])
                except Exception:
                    return ''
        data.sort(key=_key)
    # normalize rows length
    for r in data:
        if len(r) < cols:
            r.extend([''] * (cols - len(r)))
        elif len(r) > cols:
            # trim extras
            del r[cols:]

    widths = [len(h) for h in headers]
    for r in data:
        for i, cell in enumerate(r[:cols]):
            widths[i] = max(widths[i], min(len(cell), max_col_width))

    def fit(s, w):
        s = '' if s is None else str(s)
        if len(s) > w:
            return s[:w-3] + '...'
        return s

    sep = '+'.join('-' * (w + 2) for w in widths)
    sep = '+' + sep + '+'
    lines = [sep]
    # header
    hdr_cells = [' ' + headers[i].ljust(widths[i]) + ' ' for i in range(cols)]
    lines.append('|' + '|'.join(hdr_cells) + '|')
    lines.append(sep)
    for r in data:
        row_cells = [' ' + fit(r[i], widths[i]).ljust(widths[i]) + ' ' for i in range(cols)]
        lines.append('|' + '|'.join(row_cells) + '|')
    lines.append(sep)
    out = '\n'.join(lines)
    print(out)
    # add a single blank line after the table for visual separation
    print()
    return out
