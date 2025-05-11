import shlex


class Game:
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.field = self.create_empty_field()
        self.faller = None
        self.matches_to_clear = []

    def create_empty_field(self) -> list[list]:
        """"
        Creates the game field


        Returns:
          list[list]: Empty 2D array
        """
        return [[' ' for _ in range(self.cols)] for _ in range(self.rows)]

    def create_content_field(self, contents: list) -> None:
        """
        Given lines of input, initializes a field with specific content


        Arguments:
          contents: list of lines from user input #maybe be more specific later
        """

        self.field = [[' ' for _ in range(self.cols)]
                      for _ in range(self.rows)]
        for r in range(self.rows):
            for c in range(self.cols):
                self.field[r][c] = contents[r][c]

    def create_faller(self, command: str) -> None:
        """
        Creates a faller symbol in middle of field


        Arguments:
          command: list of user input
        """

        if self.faller is not None:
            return

        parts = shlex.split(command)
        left, right = parts[1], parts[2]

        if self.cols % 2 == 1:
            left_col = self.cols // 2 - 1
            right_col = self.cols // 2
        else:
            left_col = self.cols // 2 - 1
            right_col = self.cols // 2

        if self.field[0][left_col] != ' ' or self.field[0][right_col] != ' ':
            return

        self.faller = {
            'row': 1,
            'left_col': left_col,
            'right_col': right_col,
            'left_color': left,
            'right_color': right,
            'state': 'falling',
            'rotation': 0
        }

    def faller_start_state(self) -> None:
        row = self.faller['row']
        left_col = self.faller['left_col']
        right_col = self.faller['right_col']

        if row == 1:
            if self.field[row + 1][left_col] == ' ' and self.field[row + 1][right_col] == ' ':
                self.faller['state'] = 'falling'
            elif self.field[row][left_col] != ' ' and self.field[row][right_col] == ' ':
                return False
            else:
                self.faller['state'] = 'landed'

    def can_create_faller(self, row: int, left_col: int, right_col: int) -> bool:
        # returns game over if occupied by viruses as well
        return self.field[row][left_col] == ' ' and self.field[row][right_col] == ' '

    def apply_gravity_faller(self) -> None:
        """
        Keeps track of faller state, and also moves faller down everytime 'Enter' is input.
        """
        if not self.faller:
            return

        row = self.faller['row']
        left_col = self.faller['left_col']
        right_col = self.faller['right_col']
        rotation = self.faller['rotation']
        if rotation == 0 or rotation == 180:
            if row + 1 < self.rows and self.field[row + 1][left_col] == ' ' and self.field[row + 1][right_col] == ' ':
                self.faller['row'] += 1
                if row + 2 >= self.rows or self.field[row + 2][left_col] != ' ' or self.field[row + 2][right_col] != ' ':
                    self.faller['state'] = 'landed'
                else:
                    self.faller['state'] = 'falling'
            elif self.faller['state'] == 'falling':
                self.faller['state'] = 'landed'
            elif self.faller['state'] == 'landed':
                self.faller['state'] = 'frozen'
                self.freeze_faller()

        if rotation == 90 or rotation == 270:
            if row + 1 < self.rows and self.field[row + 1][left_col] == ' ':
                self.faller['row'] += 1
                if row + 2 >= self.rows or self.field[row + 2][left_col] != ' ':
                    self.faller['state'] = 'landed'
                else:
                    self.faller['state'] = 'falling'
            elif self.faller['state'] == 'falling':
                self.faller['state'] = 'landed'
            elif self.faller['state'] == 'landed':
                self.faller['state'] = 'frozen'
                self.freeze_faller()

    def get_gravity_vitamin(self) -> list:
        vitamin_list = []
        copy_field = [row[:] for row in self.field]

        for row in range(self.rows - 2, -1, -1):
            for col in range(self.cols):
                if self.field[row][col] in ['R', 'Y', 'B']:
                    if copy_field[row + 1][col] == ' ':
                        vitamin_list.append((row, col))
                        copy_field[row][col] = ' '
        return vitamin_list

    def apply_gravity_vitamin(self) -> None:
        vitamin_list = self.get_gravity_vitamin()
        for row, col in vitamin_list:
            self.field[row + 1][col] = self.field[row][col]
            self.field[row][col] = ' '

        return

    def freeze_faller(self) -> None:
        """
        When faller is frozen, saves faller instance onto field.
        """

        if not self.faller:
            return

        row = self.faller['row']
        left_col = self.faller['left_col']
        right_col = self.faller['right_col']
        left_color = self.faller['left_color']
        right_color = self.faller['right_color']
        rotation = self.faller['rotation']

        if rotation == 0:
            self.field[row][left_col] = f"{left_color}-"
            self.field[row][right_col] = f"-{right_color}"
        if rotation == 90:
            self.field[row - 1][left_col] = f"{left_color}"
            self.field[row][left_col] = f"{right_color}"
        if rotation == 180:
            self.field[row][left_col] = f"{right_color}-"
            self.field[row][right_col] = f"-{left_color}"
        if rotation == 270:
            self.field[row - 1][left_col] = f"{right_color}"
            self.field[row][left_col] = f"{left_color}"
        self.faller = None

    def check_virus(self) -> bool:
        """
        Iterates through created field to check if a virus exists


        Returns:
          bool: True or False #should i be more specific about this

        """
        for row in self.field:
            for cell in row:
                if cell in ['r', 'y', 'b']:
                    return False

        return True

    def rotate_clockwise(self) -> None:
        """
        Rotates faller clockwise, and keeps track of rotated position
        """
        if not self.faller:
            return

        current_rotation = self.faller['rotation']
        new_rotation = (current_rotation + 90) % 360

        row = self.faller['row']
        left_col = self.faller['left_col']

        if new_rotation == 90 or new_rotation == 270:

            if row - 1 < 0 or self.field[row - 1][left_col] != ' ' or self.field[row][left_col] != ' ':
                return

            self.faller['right_col'] = left_col

        elif new_rotation == 0 or new_rotation == 180:

            if left_col + 1 >= self.cols:
                return

            elif self.field[row][left_col + 1] != ' ':
                if self.field[row][left_col - 1] == ' ':
                    self.faller['left_col'] -= 1
                    self.field[row][left_col] = ' '
                    self.faller['right_col'] = left_col
                else:
                    return
            elif self.field[row][left_col + 1] == ' ':
                self.faller['right_col'] = left_col + 1

        self.faller['rotation'] = new_rotation

    def rotate_counter(self) -> None:
        """
        Rotates faller counter clockwise, and keeps track of rotated position
        """

        if not self.faller:
            return

        current_rotation = self.faller['rotation']
        new_rotation = (current_rotation + 270) % 360

        row = self.faller['row']
        left_col = self.faller['left_col']

        if new_rotation == 90 or new_rotation == 270:
            if row - 1 < 0 or self.field[row - 1][left_col] != ' ' or self.field[row][left_col] != ' ':
                return

            self.faller['right_col'] = left_col

        elif new_rotation == 0 or new_rotation == 180:

            if left_col + 1 >= self.cols:
                return

            elif self.field[row][left_col + 1] != ' ':
                if self.field[row][left_col - 1] == ' ':
                    self.faller['left_col'] -= 1
                    self.field[row][left_col] = ' '
                    self.faller['right_col'] = left_col
                else:
                    return

            elif self.field[row][left_col + 1] == ' ':
                self.faller['right_col'] = left_col + 1

        self.faller['rotation'] = new_rotation

    def move_left(self) -> bool:
        """
        Shifts faller to the left if adjacent cell is available


        Returns:
          bool: True or False
        """
        if not self.faller:
            return False

        left_col = self.faller['left_col']
        right_col = self.faller['right_col']
        row = self.faller['row']
        rotation = self.faller['rotation']

        if rotation == 0 or rotation == 180:
            if left_col > 0:
                if self.field[row][left_col - 1] == ' ' and self.field[row][right_col - 1] == ' ':
                    self.faller['left_col'] -= 1
                    self.faller['right_col'] -= 1

                if row < self.rows - 1:
                    if self.field[row - 1][self.faller['left_col']] == ' ' and self.field[row - 1][self.faller['right_col']] == ' ' and self.faller['state'] == 'landed':
                        self.faller['state'] = 'falling'
                    elif self.field[row + 1][self.faller['left_col']] != ' ' or self.field[row + 1][self.faller['right_col']] != ' ' and self.faller['state'] == 'falling':
                        self.faller['state'] = 'landed'


            return True
        elif rotation == 90 or rotation == 270:
            if left_col > 0:
                if self.field[row - 1][left_col - 1] == ' ' and self.field[row][left_col - 1] == ' ':
                    self.faller['left_col'] -= 1
                    if self.field[row - 1][self.faller['left_col']] and self.faller['state'] == 'landed':
                        self.faller['state'] = 'landed'
                    if row > 0 and self.faller['state'] == 'falling':
                        self.faller['state'] = 'landed'
                        
            return True

    def move_right(self) -> bool:
        """
        Shifts faller to the right if adjacent cell is available


        Returns:
          bool: True or False
        """
        if not self.faller:
            return False

        left_col = self.faller['left_col']
        right_col = self.faller['right_col']
        row = self.faller['row']
        rotation = self.faller['rotation']

        if rotation == 0 or rotation == 180:
            if right_col < self.cols - 1:

                if self.field[row][left_col + 1] == ' ' and self.field[row][right_col + 1] == ' ':
                    self.faller['left_col'] += 1
                    self.faller['right_col'] += 1
                    if row < self.rows - 1:
                        if self.field[row - 1][self.faller['left_col']] == ' ' and self.field[row - 1][self.faller['right_col']] == ' ' and self.faller['state'] == 'landed':
                            self.faller['state'] = 'falling'
                        elif self.field[row + 1][self.faller['left_col']] != ' ' or self.field[row + 1][self.faller['right_col']] != ' ' and self.faller['state'] == 'falling':
                            self.faller['state'] = 'landed'
            return True
        elif rotation == 90 or rotation == 270:
            if left_col < self.cols - 1:
                if self.field[row - 1][left_col + 1] == ' ' and self.field[row][left_col + 1] == ' ':
                    self.faller['left_col'] += 1
                    if self.field[row - 1][self.faller['left_col']] and self.faller['state'] == 'landed':
                        self.faller['state'] = 'falling'
                    
                    if row < self.rows  and self.faller['state'] == 'falling':
                        self.faller['state'] = 'landed'
            return True

    def create_virus(self, command: str) -> None:
        """
        Given user-specificed position, creates a virus within the field
        """
        parts = shlex.split(command)
        row = int(parts[1])
        col = int(parts[2])
        color = parts[3].lower()

        if self.field[row][col] == ' ':
            self.field[row][col] = color
        else:
            return

    def resolve_matches(self) -> bool:
        """
        Compiles all the matches; marks them; initalizes list of cells to be cleared


        Returns:
          bool: True if length of matched_cells list is greater than 0, false if not
        """

        matched_cells = []

        matched_cells.extend(self.find_horizontal_match())
        matched_cells.extend(self.find_vertical_match())

        if matched_cells:
            self.mark_matches(matched_cells)
            self.matches_to_clear = matched_cells

        return len(matched_cells) > 0

    def find_horizontal_match(self) -> list[tuple]:
        """
        Iterates through every row to find horizontally matching cells.

        Returns:
            list[tuple]: List of (row, col) tuples representing horizontal matches.
        """
        matched_cells = []

        for r in range(self.rows):
            c = 0
            while c < self.cols - 3:
                cell = self.field[r][c].strip('-').strip()

                if not cell or cell[0].lower() not in ['r', 'y', 'b']:
                    c += 1
                    continue

                match_char = cell[0].lower()
                run = [(r, c)]

                for i in range(1, self.cols - c):
                    next_cell = self.field[r][c + i].strip('-').strip()
                    if next_cell and next_cell[0].lower() == match_char:
                        run.append((r, c + i))
                    else:
                        break

                if len(run) >= 4:
                    matched_cells.extend(run)

                c += len(run)

        return matched_cells

    def find_vertical_match(self) -> list[tuple]:
        """
        Iterates through every column to find vertically matching cells.

        Returns:
            list[tuple]: List of (row, col) tuples representing vertical matches.
        """
        matched_cells = []

        for c in range(self.cols):
            r = 0
            while r < self.rows - 3:
                cell = self.field[r][c].strip('-').strip()

                if not cell or cell[0].lower() not in ['r', 'y', 'b']:
                    r += 1
                    continue

                match_char = cell[0].lower()
                run = [(r, c)]

                for i in range(1, self.rows - r):
                    next_cell = self.field[r + i][c].strip('-').strip()

                    if next_cell and next_cell[0].lower() == match_char:
                        run.append((r + i, c))
                    else:
                        break

                if len(run) >= 4:
                    matched_cells.extend(run)

                r += len(run)

        return matched_cells

    def mark_matches(self, matched_cells) -> None:
        """
        Marks all matches with '*'


        Arguments:
          matched_cells = list of coordinates from matched cells
        """
        for r, c in matched_cells:
            cell = self.field[r][c].strip('-').strip()
            if not cell:
                continue

            if cell.lower() not in ['r', 'y', 'b']:
                continue

            elif cell in ['r', 'R', 'y', 'Y', 'b', 'B']:
                self.field[r][c] = f"*{cell}*"
            elif cell in ['R-', 'Y-', 'B-']:
                self.field[r][c] = f"*{cell}*"
            elif cell in ['-R', '-Y', '-B']:
                self.field[r][c] = f"*{cell}*"

    def remove_matches(self) -> None:
        """
        Clears all matched cells
        """
        for r, c in self.matches_to_clear:
            self.field[r][c] = ' '

            if c + 1 < self.cols and '-' in self.field[r][c + 1]:
                self.field[r][c + 1] = self.field[r][c + 1].replace('-', ' ')
            elif c - 1 >= 0 and '-' in self.field[r][c - 1]:
                self.field[r][c - 1] = self.field[r][c - 1].replace('-', ' ')

        self.matches_to_clear = []
