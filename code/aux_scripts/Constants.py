import numpy as np

def get_empty_numbers_matrix():

    matrix = np.ones((14,14), dtype=np.int64) * -1
    matrix[6,6] = 1
    matrix[6,7] = 2
    matrix[7,6] = 3
    matrix[7,7] = 4

    return matrix

def get_rule_matrix():
    matrix = np.full((14,14)," ")

    # + - / * 3 2 -

    matrix[0,0] = "3"
    matrix[0,6] = "3"
    matrix[0,7] = "3"
    matrix[0,13] = "3"
    matrix[6,0] = "3"
    matrix[6,13] = "3"
    matrix[7,0] = "3"
    matrix[7,13] = "3"
    matrix[13,0] = "3"
    matrix[13,6] = "3"
    matrix[13,7] = "3"
    matrix[13,13] = "3"

    for i in range(1,5):
        matrix[i,i] = "2"
        matrix[13-i,13-i] = "2"
        matrix[i, 13 - i] = "2"
        matrix[13 - i, i] = "2"

    matrix[1,4] = '/'
    matrix[1,9] = '/'
    matrix[12,4] = '/'
    matrix[12,9] = '/'
    matrix[4,1] = '/'
    matrix[4,12] = '/'
    matrix[9,1] = '/'
    matrix[9,12] = '/'

    matrix[2,5] = '-'
    matrix[2,8] = '-'
    matrix[11,5] = '-'
    matrix[11,8] = '-'
    matrix[5,2] = '-'
    matrix[5,11] = '-'
    matrix[8,2] = '-'
    matrix[8,11] = '-'

    matrix[3,6] = '+'
    matrix[4,7] = '+'
    matrix[10,7] = '+'
    matrix[9,6] = '+'
    matrix[6,4] = '+'
    matrix[6,10] = '+'
    matrix[7,3] = '+'
    matrix[7,9] = '+'

    matrix[3,7] = '*'
    matrix[4,6] = '*'
    matrix[10,6] = '*'
    matrix[9,7] = '*'
    matrix[6,3] = '*'
    matrix[6,9] = '*'
    matrix[7,4] = '*'
    matrix[7,10] = '*'

    matrix[6,6] = 'x'
    matrix[6,7] = 'x'
    matrix[7,6] = 'x'
    matrix[7,7] = 'x'

    return matrix
