# Random Sudoku Matrix Generator in Python
# by Kait0u (2022)

from random import randint, choice, shuffle

# Easily prints a 2D matrix to standard output
def print_nested(x: list):
    for el in x:
        print(el)

# Turns a Sudoku column into a list, for easier processing
def column(x: list, col: int):
    return [x[r][col] for r in range(len(x))]

# Returns the number of a box using the row-column coordinates
def box_number(r: int, c: int) -> int:
    row = r // 3
    col = c // 3
    return  3 * row + col

# Returns the column and the row of the top-left corner of a 3x3 box, given by its number
def box_topleft(num: int):
    x = 3 * (num % 3)
    y = 3 * (num // 3)

    return (x, y)

# Turns a 3x3 box into a single list
def box(x: list, num: int):
    box = []
    c = box_topleft(num)[0]
    r = box_topleft(num)[1]
    for n in range(3):
        for m in range(3):
            box.append(x[r + n][c + m])
    return box

# Returns a list of digits 1-9, which do not appear in a given list
def missing_digits(x: list):
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    missing = []

    for num in numbers:
        if num not in x:
            missing.append(num)
    return missing


# Finds the intersection of two given lists
def intersect(x: list, y: list):
    intersection = []
    for el in x:
        if el in y:
            intersection.append(el)
    return intersection


# Checks if there are no empty cells left
def is_filled(x: list):
    if len(x) == 9 and len(choice(x)) == 9:
        for row in x:
            if 0 in row: return False
    return True

# Checks if a given Sudoku abides the rules - no repetitions in rows, columns and 3x3 boxes
def is_valid(x: list):
    if len(x) == 9 and len(choice(x)) == 9:
        for n in range(9):
            if missing_digits(x[n]) != [] or missing_digits(column(x, n)) != [] or missing_digits(box(x, n)) != []: return False
        return True
    return False

# Generates a completely random 3x3 box without repetitions
def rand_box():
    box = []

    while len(box) < 9:
        number = randint(1, 9)
        if number not in box:
            box.append(number)
    return box

# Fills the three diagonal 3x3 boxes of a Sudoku matrix: top-left, central and bottom-right
# The first stage of filling the Sudoku
def fill_diagonal(x: list):
    if len(x) == 9 and len(choice(x)) == 9:
        if x[0][0] == x[3][3] == x[6][6] == 0:
            for n in range(3):
                rbox = rand_box()
                for r in range(3):
                    for c in range(3):
                        number = rbox[3 * r + c]
                        x[3 * n + r][3 * n + c] = number
    return x

# Fills the remaining, empty cells of a Sudoku matrix - meant to be used as the second step
# Uses a backtracking method - thanks to the first stage it is relatively fast
def fill_grid(x: list):
    if len(x) == 9 and len(choice(x)) == 9:
        for cell in range(81):
            row = cell // 9
            col = cell % 9
            if x[row][col] == 0:
                pool = missing_digits(x[row])
                pool = intersect(pool, missing_digits(column(x, col)))
                pool = intersect(pool, missing_digits(box(x, box_number(row, col))))
                shuffle(pool)
                for candidate in pool:
                    x[row][col] = candidate
                    if is_filled(x) and is_valid(x): return x
                    elif fill_grid(x):
                        return x
                break
        x[row][col] = 0
                
# Completes a given Sudoku
def fill_sudoku(x: list):
    fill_diagonal(x)
    fill_grid(x)

# Generates a new, random Sudoku from scratch
def generate_sudoku() -> list:
    sudoku = [9*[0] for n in range(9)]
    fill_sudoku(sudoku)
    return sudoku

if __name__ == "__main__":
    sudoku = generate_sudoku()
    print_nested(sudoku)