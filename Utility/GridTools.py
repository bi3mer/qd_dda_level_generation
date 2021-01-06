def columns_into_rows(columns):
    column_length = len(columns[0])
    rows = ["" for _ in range(column_length)]

    for col in columns:
        i = column_length - 1
        j = 0

        while i >= 0:
            rows[j] = f'{rows[j]}{col[i]}'

            i -= 1
            j += 1

    return rows

def columns_into_grid_string(columns):
    return '\n'.join(columns_into_rows(columns))
