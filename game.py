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


       self.field = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]
       for r in range(self.rows):
           for c in range(self.cols):
               print(contents[r][c])
               self.field[r][c] = contents[r][c]


   def create_faller(self, command: str) -> None:
       """
       Creates a faller symbol in middle of field


       Arguments:
         command: list of user input
       """
       parts = shlex.split(command)
       left, right = parts[1], parts[2]
      
       if self.cols % 2 == 1:
           left_col = self.cols // 2 - 1
           right_col = self.cols // 2
       else:
           left_col = self.cols // 2 - 1
           right_col = self.cols // 2
          
       self.faller = {
           'row': 1,
           'left_col': left_col,
           'right_col': right_col,
           'left_color': left,
           'right_color': right,
           'state': 'falling',
           'rotation': 0
       }


   def apply_gravity(self) -> None:
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
               self.faller['state'] = 'falling'
               print('falling')
           elif self.faller['state'] == 'falling':
               self.faller['state'] = 'landed'
               print('landed')
           elif self.faller['state'] == 'landed':
               self.faller['state'] = 'frozen'
               self.freeze_faller()
               print('frozen')


       if rotation == 90 or rotation == 270:
           if row + 1 < self.rows and self.field[row + 1][left_col] == ' ':
               self.faller['row'] += 1
               self.faller['state'] = 'falling'
               print('falling')
           elif self.faller['state'] == 'falling':
               self.faller['state'] = 'landed'
               print('landed')
           elif self.faller['state'] == 'landed':
               self.faller['state'] = 'frozen'
               self.freeze_faller()
               print('frozen')


   def freeze_faller(self) -> None: #perhaps move this to ui.py
       """
       When faller is frozen, saves faller instance onto field.
       """


       if not self.faller:
           return
      
       print("Freeze", self.faller)


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
       self.faller['rotation'] = (self.faller['rotation'] + 90) % 360


   def rotate_counter(self) -> None: #implement a method later to check if position is available
       """
       Rotates faller counter clockwise, and keeps track of rotated position
       """
       self.faller['rotation'] = (self.faller['rotation'] + 270) % 360
  
   def move_left(self) -> bool: #have to fix logic, why is the empty cell not actually empty
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
      
       if left_col > 0:
           if self.field[row][left_col - 1] == ' ' and self.field[row][right_col - 1] == ' ':
               self.faller['left_col'] -= 1
               self.faller['right_col'] -= 1
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
               if self.field[row][left_col + 1] == ' ' and self.field[row][right_col + 1] == ' ': #this logic works for a horizontal faller
                   self.faller['left_col'] += 1
                   self.faller['right_col'] += 1
           return True
       elif rotation == 90 or rotation == 270:
           if left_col < self.cols - 1:
               if self.field[row - 1][left_col + 1] == ' ' and self.field[row][left_col + 1]  == ' ':
                   self.faller['left_col'] += 1


   def create_virus(self, command: str) -> None:
       """
       Given user-specificed position, creates a virus within the field
       """
       parts = shlex.split(command)
       row = int(parts[1])
       col = int(parts[2])
       color = parts[3].lower()


       self.field[row][col] = color


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


   def find_horizontal_match(self) -> list[tuple]: #ask about whether i should specify what is stored inside the list
       """
       Iterates through every column, in order to find horizontal matches.


       Returns:
         list[tuple]: List of tuples with row and columns of respective matches.
      
       """
       matched_cells = []
       for r in range(self.rows):
           c = 0
           while c < self.cols - 3:
               base = self.field[r][c].strip('-')
               if base and base[0] in ['r', 'y', 'b', 'R','Y','B']:
                   match_char = base[0].lower()
                   run = [(r,c)]
                   for i in range(1, self.cols - c):
                       next_cell = self.field[r][c + i]
                       if next_cell.strip() and next_cell[0].lower() == match_char:
                           run.append((r, c + i))
                       else:
                           break
                   if len(run) >= 4:
                       matched_cells.extend(run)
                   c += len(run)
               else:
                   c += 1
       return matched_cells


   def find_vertical_match(self) -> list[tuple]:
       """
       Iterates through every row in order to finds cells that match vertically


       Returns:
         list[tuple]: List of tuples with row and columns of respective vertical matches.
       """
        
       matched_cells = []
       for c in range(self.cols):
           r = 0
           while r < self.rows - 3:
               base = self.field[r][c].strip()
               if base and base[0] in ['r','y','b', 'R', 'Y', 'B']:
                   match_char = base[0].lower()
                  
                   run = [(r, c)]
                   for i in range(1, self.rows - r):
                       next_cell = self.field[r + i][c]
                       # next_cell.strip()[0].lower() == match_char:
                       if next_cell.strip() and next_cell[0].lower() == match_char:
                          
                           run.append((r + i, c))
                       else:
                           break
                   if len(run) >= 4:
                       matched_cells.extend(run)
                   r += len(run)
               else:
                   r += 1


       return matched_cells


       
   def mark_matches(self, matched_cells) -> None:
       """
       Marks all matches with '*'


       Arguments:
         matched_cells = list of coordinates from matched cells
       """
       for r, c in matched_cells:
           cell = self.field[r][c]
           if not cell.strip():
               continue
      
           color = cell[0].lower()
           if color not in ['r','y','b']:
               continue
          
           elif cell in ['r','R','y','Y','b', 'B']:
               self.field[r][c] = f"*{cell}*"
           elif cell in ['R-','Y-','B-']:
               self.field[r][c] = f"*{cell[0]}*"
               self.field[r][c ]
           elif cell in ['-R','-Y','-B']:
               self.field[r][c] = f"*{cell[0]}*"
  
   def remove_matches(self) -> None:
       """
       Clears all matched cells
       """
       for r, c in self.matches_to_clear:
           self.field[r][c] = ' '


           if c + 1 < self.cols and '-' in self.field[r][c + 1]:
               self.field[r][c + 1] = self.field[r][c + 1].replace('-', ' ')
           elif c - 1 >= 0 and  '-' in self.field[r][c - 1]:
               self.field[r][c - 1] = self.field[r][c - 1].replace('-', ' ')


       self.matches_to_clear = []


