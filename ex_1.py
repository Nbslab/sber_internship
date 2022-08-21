def get_shape():
    i, j = input('Введите размерность матрицы(в формате: i,j): ').split(',')
    return int(i), int(j)


def get_matrix(i: int, j: int) -> list:
    matrix_list = []
    while len(matrix_list) < i:
        sample_tmp = input().split(',')
        sample_tmp = list(map(int, sample_tmp))
        if len(sample_tmp) != j:
            print(
                f'Number of cols {len(sample_tmp)} not equal matrix shape {j}')
        else:
            matrix_list.append(sample_tmp)
    return matrix_list


def return_matrix_minor(mat, i, j):
    return [row[:j] + row[j + 1:] for row in (mat[:i] + mat[i + 1:])]


def return_transpose(matrix_tmp: list):
    return [[matrix_tmp[j][i] for j in range(len(matrix_tmp))] for i in
            range(len(matrix_tmp[0]))]


def get_determinant(matrix_tmp: list) -> int:
    row = len(matrix_tmp)
    col = len(matrix_tmp[0])
    result = 0
    if len(matrix_tmp) == 2:
        return matrix_tmp[0][0] * matrix_tmp[1][1] - matrix_tmp[0][1] * matrix_tmp[1][0]
    elif len(matrix_tmp) == 3:
        result += (matrix_tmp[0][0] * matrix_tmp[1][1] * matrix_tmp[2][2] +
                   matrix_tmp[0][1] * matrix_tmp[1][2] * matrix_tmp[2][0] +
                   matrix_tmp[0][2] * matrix_tmp[1][0] * matrix_tmp[2][1])
        result -= (matrix_tmp[0][2] * matrix_tmp[1][1] * matrix_tmp[2][0] +
                   matrix_tmp[0][0] * matrix_tmp[1][2] * matrix_tmp[2][1] +
                   matrix_tmp[0][1] * matrix_tmp[1][0] * matrix_tmp[2][2])
        return result
    else:
        sign = -1
        row1 = [matrix_tmp[0][i] * (sign ** i) for i in range(col)]
        for x, y in enumerate(row1):
            mat = matrix_tmp[:][1:]
            sub_matrix = [[mat[i][j] for j in range(col) if j != x] for i in
                          range(row - 1)]
            result += y * get_determinant(sub_matrix)
        return result


def get_reverse(matrix_tmp: list, det: int, i: int, j: int):
    if i == 2:
        return [[matrix_tmp[1][1] / det, -1 * matrix_tmp[0][1] / det],
                [-1 * matrix_tmp[1][0] / det, matrix_tmp[0][0] / det]]
    else:
        cfs = []
        for r in range(i):
            cfRow = []
            for c in range(i):
                minor = return_matrix_minor(matrix_tmp, r, c)
                cfRow.append(((-1) ** (r + c)) * get_determinant(minor))
            cfs.append(cfRow)
        cfs = return_transpose(cfs)
        for r in range(len(cfs)):
            for c in range(len(cfs)):
                cfs[r][c] = round(cfs[r][c] / det, 1)
        return cfs


if __name__ == "__main__":
    i_shape, j_shape = get_shape()
    if i_shape == j_shape:
        matrix = get_matrix(i_shape, j_shape)
        determinant = get_determinant(matrix)
        if determinant == 0:
            print("Can't find reverse matrix: determinant = 0")
        else:
            reversed_matrix = get_reverse(matrix, determinant, i_shape, j_shape)
            for value in reversed_matrix:
                print(*value)
    else:
        print("Can't find reverse matrix with non-square shape")

# 0,1,2,3,4,5,6,7,8,9
# 1,1,0,0,0,0,0,0,0,8
# 2,0,1,0,0,0,0,0,0,7
# 3,0,0,1,0,0,0,0,0,6
# 4,0,0,0,1,0,0,0,0,5
# 5,0,0,0,0,1,0,0,0,4
# 6,0,0,0,0,0,1,0,0,3
# 7,0,0,0,0,0,0,1,0,2
# 8,0,0,0,0,0,0,0,1,1
# 9,0,0,0,0,0,0,0,0,0
