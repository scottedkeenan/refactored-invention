from selenium import webdriver
from bs4 import BeautifulSoup


def find_empty(puzzle):
    """Returns location of next empty cell"""
    for row, row_values in enumerate(puzzle):
        for col, value in enumerate(row_values):
            if value is 0:
                return (row, col)
    return False


def insertValue(grid, value, x_pos, y_pos):
    """Inserts the given value into the given position of the given puzzle grid"""
    grid[x_pos][y_pos] = value
    return grid


def check_row_col(cand, num, slot):
    """Checks if cand contains num in the same row and column as the given slot"""
    if num not in cand[slot[0]]:
        col = [y[slot[1]] for y in cand]
        if num not in col:
            return True
        else:
            return False
    else:
        return False


def check_box(cand, num, slot):
    """Checks if num is in the same 3x3 box of cand as slot"""

    box = [
        slot[0] - slot[0] %3,
        slot[1] - slot[1]%3
    ]


    for i in range(3):
        for j in range(3):
            if cand[i+box[0]][j+box[1]] == num:
                return True
    return False


def solve(cand):
    """Solves puzzle using backtracking"""
    slot = find_empty(cand)
    if slot:
        for i in range(1,10):
            if check_row_col(cand, i, slot) and not check_box(cand, i, slot):
                insertValue(cand, i, slot[0], slot[1])
                if solve(cand):
                    return cand
                else:
                    insertValue(cand, 0, slot[0], slot[1])
    else:
        return cand
    return False


def scrape_puzzle(difficulty):
    """
    Scraoes a sokoku puzzle from https://sudoku.com/

    Difficulty is one of 'easy', 'medium', 'hard', 'expert'.
    """
    difficulties = ['easy', 'medium', 'hard', 'expert']
    if difficulty not in difficulties:
        raise ValueError('Difficulty must be one of: {0}, {1}, {2}, {3}'.format(*difficulties))
    driver = webdriver.Firefox()
    driver.get('https://sudoku.com/{}'.format(difficulty))

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # get the svg paths from the numpad
    numbers = soup.find_all('div', class_='numpad-item')
    svg_key = {}
    for number in numbers:
        svg_key[number.find('path').attrs['d']] = number.attrs['data-value']

    game = []
    game_rows = soup.find_all('tr', class_='game-row')
    for game_row in game_rows:
        row = []
        game_cells = game_row.find_all('td')
        for cell in game_cells:
            cell_value_div = cell.find('div', class_='cell-value')
            if cell_value_div.svg:
                cell_svg = cell_value_div.svg.path.attrs['d']
                row.append(int(svg_key[cell_svg]))
            else:
                row.append(0)
        game.append(row)
    driver.close()
    return game

if __name__ == "__main__":
    puzzle = scrape_puzzle('expert')
    print('Puzzle:')
    for row in puzzle:
        print(row)
    print('Solution:')
    for row in solve(puzzle):
        print(row)