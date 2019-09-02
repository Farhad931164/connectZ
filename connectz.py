import utils.input_reader
from utils.argument_reader import check_input_file
from contracts.outputs import GameOutputs
from connectz_engine.connectz_game import ConnectZGame
from connectz_engine.connectz_game import IllegalGameSpecError, IllegalColumnError, IllegalRowError, IllegalContinue


def main():
    input_file = check_input_file()
    if input_file is None:
        print("Provide one input file")
    else:  # command line argument exists
        try:
            input_file_reader = utils.input_reader.FileReader(input_file)
            game = ConnectZGame(input_file_reader.game_specs)

            winner = GameOutputs.INCOMPLETE  # default result, otherwise game engine should raise something

            for line in input_file_reader:
                winner = game.drop(line-1)

            output = winner

        except FileNotFoundError:
            output = GameOutputs.FILE_ERROR
        except utils.input_reader.FileContentError:
            output = GameOutputs.INVALID_FILE
        except IllegalGameSpecError:
            output = GameOutputs.ILLEGAL_GAME
        except IllegalRowError:
            output = GameOutputs.ILLEGAL_ROW
        except IllegalColumnError:
            output = GameOutputs.ILLEGAL_COL
        except IllegalContinue:
            output = GameOutputs.ILLEGAL_CONTINUE

        print(f"output : {output}")

        for row in game._game_bed:
            for col in row:
                if col is not None:
                    print(str(col), '| ', end='')
                else:
                    print('  | ', end='')
            print('')


if __name__ == '__main__':
    main()
