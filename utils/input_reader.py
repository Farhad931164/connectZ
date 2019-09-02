"""
    Input file reader module
"""


class FileContentError(BaseException):
    pass


class FileReader:
    def __init__(self, input_file_path: str):  # constructor
        self._input_file_path = input_file_path
        self._input_file = None  # handle to the input file, needed later
        try:
            with open(input_file_path, 'r') as in_file:
                first_line = in_file.readline()

            cols, rows, connects = first_line.split(' ')
            self._cols = int(cols)
            self._rows = int(rows)
            self._connects = int(connects)

        except ValueError:
            raise FileContentError

    def __del__(self):  # destructor
        if self._input_file is not None:
            self._input_file.close()

    @property
    def game_specs(self):
        return self._cols, self._rows, self._connects

    def __iter__(self):  # iterator on the file content
        self._input_file = open(self._input_file_path, 'r')
        self._input_file.readline()  # jump over the first line
        return self

    def __next__(self):
        current_line: str = self._input_file.readline()
        if current_line == "" and not current_line.endswith('\n'):
            self._input_file.close()
            raise StopIteration

        try:
            value = int(current_line)
            return value
        except ValueError:
            raise FileContentError
