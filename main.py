from sys import argv

from constants import transitions, constantsHL
from utils import to_decimal, to_xlsx, to_pretty


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


def main():
    try:
        sequence = argv[1]
    except IndexError:
        sequence = input('Input sequence: ')

    matrix = setup_matrix(sequence)
    calculated, best, result = calculate(constantsHL, transitions, matrix, sequence)
    pretty = to_pretty(calculated)
    file = to_xlsx(pretty, sequence, best, result)
    print(f'Successfully calculated! Look for the result in {file}')


if __name__ == '__main__':
    main()
