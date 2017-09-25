import simpletest
from components.fifteen_puzzle import FifteenPuzzle


def test_shuffle_board(board):
    elements = [element for row in board for element in row]
    return len(elements) == len(set(elements)) == 16


def test_2x2(game):
    for row_num in range(len(game._grid)):
        for col_num in range(len(game._grid[0])):
            if game.current_position(row_num, col_num) != (row_num, col_num):
                return False
    return True


def run_test_suite():
    suite = simpletest.TestSuite()
    game = FifteenPuzzle()
    suite.run_test(game.board, [[0, 1, 2, 3], [4, 5, 6, 7],
                                [8, 9, 10, 11], [12, 13, 14, 15]], 'TEST #1')
    suite.run_test(game.is_finished(), True, 'TEST #2')
    game.shuffle_board()
    suite.run_test(test_shuffle_board(game.board), True, 'TEST #3')
    suite.run_test(game.is_finished(), False, 'TEST #4')
    board = [[2, 3, 4, 5], [6, 7, 8, 10], [9, 11, 12, 0], [14, 15, 13, 1]]
    game = FifteenPuzzle(board)
    suite.run_test(game.board, board, 'TEST #5')
    suite.run_test(game.is_finished(), False, 'TEST #6')

    # game.current_position()
    board = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
    game = FifteenPuzzle(board)
    suite.run_test(game.current_position(0, 0), (0, 0), 'TEST #7')
    suite.run_test(game.current_position(1, 2), (1, 2), 'TEST #8')
    suite.run_test(game.current_position(3, 0), (3, 0), 'TEST #9')

    board = [[2, 0, 11, 14], [6, 3, 8, 10], [9, 4, 12, 7], [5, 15, 13, 1]]
    game = FifteenPuzzle(board)
    suite.run_test(game.current_position(0, 0), (0, 1), 'TEST #10')
    suite.run_test(game.current_position(1, 2), (1, 0), 'TEST #11')
    suite.run_test(game.current_position(3, 0), (2, 2), 'TEST #12')

    # game.is_move_possible()
    board = [[2, 3, 4, 5], [6, 7, 8, 10], [9, 0, 12, 11], [14, 15, 13, 1]]
    game = FifteenPuzzle(board)
    suite.run_test(game.is_move_possible('U'), True, 'TEST #13')
    suite.run_test(game.is_move_possible('D'), True, 'TEST #14')
    suite.run_test(game.is_move_possible('L'), True, 'TEST #15')
    suite.run_test(game.is_move_possible('R'), True, 'TEST #16')

    board = [[2, 0, 4, 5], [6, 7, 8, 10], [9, 3, 12, 11], [14, 15, 13, 1]]
    game = FifteenPuzzle(board)
    suite.run_test(game.is_move_possible('U'), False, 'TEST #17')
    suite.run_test(game.is_move_possible('D'), True, 'TEST #18')
    suite.run_test(game.is_move_possible('L'), True, 'TEST #19')
    suite.run_test(game.is_move_possible('R'), True, 'TEST #20')

    board = [[2, 3, 4, 5], [6, 7, 8, 10], [9, 13, 12, 11], [14, 15, 0, 1]]
    game = FifteenPuzzle(board)
    suite.run_test(game.is_move_possible('U'), True, 'TEST #21')
    suite.run_test(game.is_move_possible('D'), False, 'TEST #22')
    suite.run_test(game.is_move_possible('L'), True, 'TEST #23')
    suite.run_test(game.is_move_possible('R'), True, 'TEST #24')

    board = [[2, 3, 4, 5], [6, 7, 8, 10], [0, 9, 12, 11], [14, 15, 13, 1]]
    game = FifteenPuzzle(board)
    suite.run_test(game.is_move_possible('U'), True, 'TEST #25')
    suite.run_test(game.is_move_possible('D'), True, 'TEST #26')
    suite.run_test(game.is_move_possible('L'), False, 'TEST #27')
    suite.run_test(game.is_move_possible('R'), True, 'TEST #28')

    board = [[2, 3, 4, 0], [6, 7, 8, 10], [9, 5, 12, 11], [14, 15, 13, 1]]
    game = FifteenPuzzle(board)
    suite.run_test(game.is_move_possible('U'), False, 'TEST #29')
    suite.run_test(game.is_move_possible('D'), True, 'TEST #30')
    suite.run_test(game.is_move_possible('L'), True, 'TEST #31')
    suite.run_test(game.is_move_possible('R'), False, 'TEST #32')

    # game.apply_move()
    board = [[2, 3, 4, 5], [6, 7, 8, 10], [9, 0, 12, 11], [14, 15, 13, 1]]
    game = FifteenPuzzle(board)
    game.apply_move('U')
    board_after_u = [[2, 3, 4, 5], [6, 0, 8, 10],
                     [9, 7, 12, 11], [14, 15, 13, 1]]
    suite.run_test(game.board, board_after_u, 'TEST #33')
    game.apply_move('D')
    suite.run_test(game.board, board, 'TEST #34')
    game.apply_move('L')
    board_after_l = [[2, 3, 4, 5], [6, 7, 8, 10],
                     [0, 9, 12, 11], [14, 15, 13, 1]]
    suite.run_test(game.board, board_after_l, 'TEST #35')
    game.apply_move('R')
    suite.run_test(game.board, board, 'TEST #36')

    grid = [[4, 2, 3, 7], [8, 5, 6, 10], [9, 1, 0, 11], [12, 13, 14, 15]]
    game = Puzzle(4, 4, grid)
    suite.run_test(game.lower_row_invariant(2, 2), True, 'TEST #1')

    grid = [[4, 2, 3, 7], [8, 5, 6, 10], [9, 13, 0, 11], [12, 1, 14, 15]]
    game = Puzzle(4, 4, grid)
    suite.run_test(game.lower_row_invariant(2, 2), False, 'TEST #2')

    # solve_interior_tile
    grid = [[1, 2, 3, 15], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 4, 0]]
    game = Puzzle(4, 4, grid)
    suite.run_test(game.lower_row_invariant(3, 3), True, 'TEST #3')
    game.solve_interior_tile(3, 3)
    suite.run_test(game.lower_row_invariant(3, 2), True, 'TEST #4')

    grid = [[1, 2, 3, 4], [5, 15, 7, 8], [9, 10, 11, 12], [13, 14, 6, 0]]
    game = Puzzle(4, 4, grid)
    suite.run_test(game.lower_row_invariant(3, 3), True, 'TEST #5')
    game.solve_interior_tile(3, 3)
    suite.run_test(game.lower_row_invariant(3, 2), True, 'TEST #6')

    grid = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [15, 14, 13, 0]]
    game = Puzzle(4, 4, grid)
    suite.run_test(game.lower_row_invariant(3, 3), True, 'TEST #7')
    game.solve_interior_tile(3, 3)
    suite.run_test(game.lower_row_invariant(3, 2), True, 'TEST #8')

    grid = [[1, 2, 3, 4], [5, 6, 7, 13], [9, 10, 11, 12], [8, 0, 14, 15]]
    game = Puzzle(4, 4, grid)
    suite.run_test(game.lower_row_invariant(3, 1), True, 'TEST #9')
    game.solve_interior_tile(3, 1)
    suite.run_test(game.lower_row_invariant(3, 0), True, 'TEST #10')

    # solve_col0_tile
    grid = [[12, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 1], [0, 13, 14, 15]]
    game = Puzzle(4, 4, grid)
    suite.run_test(game.lower_row_invariant(3, 0), True, 'TEST #11')
    game.solve_col0_tile(3)
    suite.run_test(game.lower_row_invariant(2, 3), True, 'TEST #12')

    grid = [[1, 12, 3, 4], [5, 6, 7, 8], [9, 10, 11, 2], [0, 13, 14, 15]]
    game = Puzzle(4, 4, grid)
    suite.run_test(game.lower_row_invariant(3, 0), True, 'TEST #13')
    game.solve_col0_tile(3)
    suite.run_test(game.lower_row_invariant(2, 3), True, 'TEST #14')

    grid = [[1, 2, 3, 4], [5, 6, 12, 8], [9, 10, 11, 7], [0, 13, 14, 15]]
    game = Puzzle(4, 4, grid)
    suite.run_test(game.lower_row_invariant(3, 0), True, 'TEST #15')
    game.solve_col0_tile(3)
    suite.run_test(game.lower_row_invariant(2, 3), True, 'TEST #16')

    grid = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [0, 13, 14, 15]]
    game = Puzzle(4, 4, grid)
    suite.run_test(game.lower_row_invariant(3, 0), True, 'TEST #17')
    game.solve_col0_tile(3)
    suite.run_test(game.lower_row_invariant(2, 3), True, 'TEST #18')

    grid = [[12, 11, 10, 9, 15], [7, 6, 5, 4, 3],
            [2, 1, 8, 13, 14], [0, 16, 17, 18, 19]]
    game = Puzzle(4, 5, grid)
    suite.run_test(game.lower_row_invariant(3, 0), True, 'TEST #19')
    game.solve_col0_tile(3)
    suite.run_test(game.lower_row_invariant(2, 4), True, 'TEST #20')

    # row1_invariant
    grid = [[4, 6, 1, 3], [5, 2, 0, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
    game = Puzzle(4, 4, grid)
    suite.run_test(game.row1_invariant(2), True, 'TEST #21')

    grid = [[4, 6, 1, 3], [5, 2, 0, 8], [7, 9, 10, 11], [12, 13, 14, 15]]
    game = Puzzle(4, 4, grid)
    suite.run_test(game.row1_invariant(2), False, 'TEST #22')

    # row0_invariant
    grid = [[4, 2, 0, 3], [5, 1, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
    game = Puzzle(4, 4, grid)
    suite.run_test(game.row0_invariant(2), True, 'TEST #23')

    grid = [[6, 2, 0, 3], [5, 1, 4, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
    game = Puzzle(4, 4, grid)
    suite.run_test(game.row0_invariant(2), False, 'TEST #24')

    # solve_row1_tile
    grid = [[1, 2, 3, 4], [7, 6, 5, 0], [8, 9, 10, 11], [12, 13, 14, 15]]
    game = Puzzle(4, 4, grid)
    suite.run_test(game.row1_invariant(3), True, 'TEST #25')
    game.solve_row1_tile(3)
    suite.run_test(game.row0_invariant(3), True, 'TEST #26')

    grid = [[1, 7, 3, 4], [5, 6, 2, 0], [8, 9, 10, 11], [12, 13, 14, 15]]
    game = Puzzle(4, 4, grid)
    suite.run_test(game.row1_invariant(3), True, 'TEST #27')
    game.solve_row1_tile(3)
    suite.run_test(game.row0_invariant(3), True, 'TEST #28')

    grid = [[1, 2, 3, 7], [5, 6, 4, 0], [8, 9, 10, 11], [12, 13, 14, 15]]
    game = Puzzle(4, 4, grid)
    suite.run_test(game.row1_invariant(3), True, 'TEST #29')
    game.solve_row1_tile(3)
    suite.run_test(game.row0_invariant(3), True, 'TEST #30')

    grid = [[6, 2, 4, 3], [5, 1, 0, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
    game = Puzzle(4, 4, grid)
    suite.run_test(game.row1_invariant(2), True, 'TEST #31')
    game.solve_row1_tile(2)
    suite.run_test(game.row0_invariant(2), True, 'TEST #32')

    # solve_row0_tile
    grid = [[3, 2, 1, 0], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
    game = Puzzle(4, 4, grid)
    suite.run_test(game.row0_invariant(3), True, 'TEST #33')
    game.solve_row0_tile(3)
    suite.run_test(game.row1_invariant(2), True, 'TEST #34')

    grid = [[1, 2, 4, 0], [3, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
    game = Puzzle(4, 4, grid)
    suite.run_test(game.row0_invariant(3), True, 'TEST #35')
    game.solve_row0_tile(3)
    suite.run_test(game.row1_invariant(2), True, 'TEST #36')

    grid = [[1, 2, 6, 0], [4, 5, 3, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
    game = Puzzle(4, 4, grid)
    suite.run_test(game.row0_invariant(3), True, 'TEST #37')
    game.solve_row0_tile(3)
    suite.run_test(game.row1_invariant(2), True, 'TEST #38')

    grid = [[1, 4, 0, 3], [2, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
    game = Puzzle(4, 4, grid)
    suite.run_test(game.row0_invariant(2), True, 'TEST #39')
    game.solve_row0_tile(2)
    suite.run_test(game.row1_invariant(1), True, 'TEST #40')

    # solve_2x2
    grid = [[3, 2], [1, 0]]
    game = Puzzle(2, 2, grid)
    game.solve_2x2()
    suite.run_test(test_2x2(game), True, 'TEST #41')

    grid = [[1, 3], [2, 0]]
    game = Puzzle(2, 2, grid)
    game.solve_2x2()
    suite.run_test(test_2x2(game), True, 'TEST #42')

    # solve_puzzle
    grid = [[1, 7, 3, 4], [5, 6, 2, 0], [8, 9, 10, 11], [12, 13, 14, 15]]
    game = Puzzle(4, 4, grid)
    # game.solve_puzzle()
    # suite.run_test(test_2x2(game), True, 'TEST #43')

    grid = [[1, 2, 3, 4], [5, 15, 7, 8], [9, 10, 11, 12], [13, 14, 6, 0]]
    game = Puzzle(4, 4, grid)
    # game.solve_puzzle()
    # suite.run_test(test_2x2(game), True, 'TEST #44')

    game = Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9],
                  [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]])
    path = game.solve_puzzle()
    game = Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9],
                  [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]])
    game.update_puzzle(path)
    suite.run_test(test_2x2(game), True, 'TEST #45')

    suite.report_results()

run_test_suite()
