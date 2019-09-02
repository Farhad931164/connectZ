"""
    Game main script file
"""

import utils.input_reader

from utils.argument_reader import check_input_file
from contracts.outputs import GameOutputs
from connectz_engine.connectz_game import ConnectZGame
from connectz_engine.connectz_game import IllegalGameSpecError, IllegalColumnError, IllegalRowError, IllegalContinue


def main():
    input_file = check_input_file()  # checking the input file
    if input_file is None:
        print("Provide one input file")
    else:  # command line argument exists
        try:
            input_file_reader = utils.input_reader.FileReader(input_file)  # Instantiating input FileReader
            game = ConnectZGame(input_file_reader.game_specs)
            game_output = GameOutputs.INCOMPLETE  # default result, otherwise game engine should raise something

            for line in input_file_reader:
                game_output = game.drop(line - 1)  # 1 indexed column converted to 0 indexed column

            output = game_output

        except FileNotFoundError:  # Python file not found error
            output = GameOutputs.FILE_ERROR
        except utils.input_reader.FileContentError:  # Internal exception when file content is bad
            output = GameOutputs.INVALID_FILE
        except IllegalGameSpecError:  # Illegal game size
            output = GameOutputs.ILLEGAL_GAME
        except IllegalRowError:  # Bad row
            output = GameOutputs.ILLEGAL_ROW
        except IllegalColumnError:  # Bad column
            output = GameOutputs.ILLEGAL_COL
        except IllegalContinue:  # Illegal continue when the game has finished already
            output = GameOutputs.ILLEGAL_CONTINUE

        print(f"{output}")

if __name__ == '__main__':
    main()
