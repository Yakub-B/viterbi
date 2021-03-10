from decimal import Decimal

import xlsxwriter


def to_decimal(num: float) -> Decimal:
    """
    Rounds float to decimal number with 3 decimal places
    """
    return Decimal("{:.3f}".format(num))


def to_pretty(matrix: list) -> list:
    """
    Matrix with floats to matrix in Decimals
    """
    for row_idx, row in enumerate(matrix):
        for elem_idx, elem in enumerate(row):
            matrix[row_idx][elem_idx] = to_decimal(elem)

    return matrix


def to_xlsx(matrix, seq, best, result):
    """
    Write results to xlsx file
    """
    workbook = xlsxwriter.Workbook('result.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write_row(0, 1, seq)
    worksheet.write_column(1, 0, ['H', 'L'])
    for row, data in enumerate(matrix):
        worksheet.write_row(row + 1, 1, data)
    worksheet.write_row(3, 1, best)
    worksheet.write_string(5, 4, 'Result:')
    worksheet.write_number(5, 5, result)
    workbook.close()