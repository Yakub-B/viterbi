from decimal import Decimal

import xlsxwriter

sequence = 'GGCACTGAA'

constantsHL = {
    'H': {'A': -2.322, 'C': -1.737, 'G': -1.737, 'T': -2.322},
    'L': {'A': -1.737, 'C': -2.322, 'G': -2.322, 'T': -1.737},
}

transitions = {
    'start': -1,
    'HH': -1,
    'LL': -0.737,
    'HL': -1,
    'LH': -1.322,
}


def to_decimal(num: float) -> Decimal:
    """
    Rounds float to decimal number with 3 decimal places
    """
    return Decimal("{:.3f}".format(num))


def setup_matrix(seq: str) -> list:
    """
    Set up simple 2d matrix with 2 rows and len(seq) columns
    """
    return [[0 for _ in range(len(seq))] for _ in range(2)]


def calculate(const_hl: dict, transitions_: dict, matrix: list, seq: str) -> tuple:
    """
    Calculates matrix, HL sequence and result probability
    """
    best = []
    result_value = None
    for idx, elem in enumerate(seq):
        if idx == 0:
            h_value = transitions_['start'] + const_hl['H'][elem]
            l_value = transitions_['start'] + const_hl['L'][elem]
        else:
            h_value = const_hl['H'][elem] + max(
                matrix[0][idx - 1] + transitions_['HH'],
                matrix[1][idx - 1] + transitions_['LH']
            )
            l_value = const_hl['L'][elem] + max(
                matrix[0][idx - 1] + transitions_['HL'],
                matrix[1][idx - 1] + transitions_['LL']
            )
        matrix[0][idx] = h_value
        matrix[1][idx] = l_value
        if to_decimal(h_value) > to_decimal(l_value):
            best.append('H')
        elif to_decimal(h_value) == to_decimal(l_value):
            best.append(best[-1])
        else:
            best.append('L')

        result_value = max(h_value, l_value)

    return matrix, best, 2 ** result_value


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
    workbook = xlsxwriter.Workbook('bi.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write_row(0, 1, seq)
    worksheet.write_column(1, 0, ['H', 'L'])
    for row, data in enumerate(matrix):
        worksheet.write_row(row + 1, 1, data)
    worksheet.write_row(3, 1, best)
    worksheet.write_string(5, 4, 'Result:')
    worksheet.write_number(5, 5, result)
    workbook.close()


def main():
    matrix = setup_matrix(sequence)
    calculated, best, result = calculate(constantsHL, transitions, matrix, sequence)
    pretty = to_pretty(calculated)
    to_xlsx(pretty, sequence, best, result)


if __name__ == '__main__':
    main()
