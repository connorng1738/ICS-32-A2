from game import Game


class UI:
   @staticmethod
   def display_field(state: Game) -> None:
       """"
       Given the state of the game, displays the field and relevant objects.


      
       Arguments:
         state: Game logic including field information and faller movement
      
       """
       for r in range(state.rows):
           print('|', end='')
           c = 0
           while c < state.cols:
               faller_piece = get_faller_symbol(r, c, state.faller)
               if faller_piece:
                   print(faller_piece, end = '')
                   c += 1
                   continue

               cell = state.field[r][c]
               if cell == ' ':
                   print('   ', end='')
               elif cell in 'rby':
                   print(f'{cell:^3}', end='')
               elif c + 1 < state.cols and cell.endswith('-') and state.field[r][c + 1].startswith('-'):
                   combined = f'{cell}{state.field[r][c + 1]}'
                   print(f"{combined:^6}", end = '')
                   c += 2
                   continue
               else:
                   print(f'{cell:^3}', end='') 
              
               c += 1
           print('|')
       print(' ' + '-' * (3 * state.cols) + ' ')

def get_faller_symbol(row: int, col: int, faller: dict) -> str:
   """"
   Getter function that returns faller rotation state
  
   Arguments:
     row: Current row of faller
     col: Current column of faller
     faller: Dictionary of relevant faller information


   Return:
     str: Symbol of faller piece at given position
   """
   if faller is None:
       return None

   r = faller['row']
   l_col = faller['left_col']
   r_col = faller['right_col']
   l_color = faller['left_color']
   r_color = faller['right_color']
   state = faller['state']
   rotation = faller['rotation']
  
   return get_rotation(rotation, r, l_col, r_col, l_color, r_color, state, row, col)

def get_rotation(rotation: int, r: int, l_col: int, r_col: int, l_color: str, r_color:str, state:str,  row: int, col: int):
   if rotation == 0:
       return _rotate_0(r, l_col, r_col, l_color, r_color, state, row, col)


   elif rotation == 90:
       return _rotate_90(r, l_col, l_color, r_color, state, row, col)
   elif rotation == 180:
       return _rotate_180(r, l_col, r_col, l_color, r_color, state, row, col)
  
   elif rotation == 270:
       return _rotate_270(r, l_col, l_color, r_color, state, row, col)
  
def _rotate_0(r: int, l_col: int, r_col: int, l_color: str, r_color:str, state:str,  row: int, col: int) -> str:
   """
   Returns the symbol of a faller rotated at 0 degrees (default position)
  
   Arguments:
     r: Row position of faller
     l_col: Left column of faller
     r_col: Right column of faller
     l_color: Left color of faller
     r_color: Right color of faller
     state: Current state of faller
     row: Current row being checked
     col: Current column being checked


   Returns:
     str: Symbol of faller piece at given position
   """
   if row == r:
           if col == l_col:
               if state == 'falling':
                   return f"[{l_color}-"
               elif state == 'landed':
                   return f"|{l_color}-"
               else:
                   return f"{l_color}-"
           elif col == r_col:
               if state == 'falling':
                   return f"-{r_color}]"
               elif state == 'landed':
                   return f"-{r_color}|"
               else:
                   return f"-{r_color}"
   return None


def _rotate_90(r: int, l_col: int, l_color: str, r_color: str, state: str, row: int, col: int) -> str:
   """
   Returns the symbol of a faller rotated at 90 degrees (rotated position)
  
   Arguments:
     r: Row position of faller
     l_col: Left column of faller
     r_col: Right column of faller
     l_color: Left color of faller
     r_color: Right color of faller
     state: Current state of faller
     row: Current row being checked
     col: Current column being checked


   Returns:
     str: Symbol of faller piece at given position
   """
  
   if col == l_col:
           if row == r - 1:
               if state == 'falling':
                   return f"[{l_color}]"
               elif state == 'landed':
                   return f"|{l_color}|"
               else:
                   return f"{l_color}"
           if row == r:
               if state == 'falling':
                   return f"[{r_color}]"
               elif state == 'landed':
                   return f"|{r_color}|"
               else:
                   return f"{r_color}"
   return None

def _rotate_180(r: int, l_col: int, r_col: int, l_color: str, r_color:str, state:str, row: int, col: int) -> str:
   """
   Returns the symbol of a faller rotated at 180 degrees (rotated position)
  
   Arguments:
     r: Row position of faller
     l_col: Left column of faller
     r_col: Right column of faller
     l_color: Left color of faller
     r_color: Right color of faller
     state: Current state of faller
     row: Current row being checked
     col: Current column being checked


   Returns:
     str: Symbol of faller piece at given position
   """
   if row == r:
           if col == l_col:
               if state == 'falling':
                   return f"[{r_color}-"
               elif state == 'landed':
                   return f"|{r_color}-"
               else:
                   return f"{r_color}-"
           elif col == r_col:
               if state == 'falling':
                   return f"-{l_color}]"
               elif state == 'landed':
                   return f"-{l_color}|"
               else:
                   return f"-{l_color}"
   return None


def _rotate_270(r: int, l_col: int, l_color: str, r_color: str, state: str, row: int, col: int) -> str:
   """
   Returns the symbol of a faller rotated at 270 degrees (rotated position)
  
   Arguments:
     r: Row position of faller
     l_col: Left column of faller
     r_col: Right column of faller
     l_color: Left color of faller
     r_color: Right color of faller
     state: Current state of faller
     row: Current row being checked
     col: Current column being checked


   Returns:
     str: Symbol of faller piece at given position
   """
   if col == l_col:
           if row == r - 1:
               if state == 'falling':
                   return f"[{r_color}]"
               elif state == 'landed':
                   return f"|{r_color}|"
               else:
                   return f"{r_color}"
           if row == r:
               if state == 'falling':
                   return f"[{l_color}]"
               elif state == 'landed':
                   return f"|{l_color}|"
               else:
                   return f"{l_color}"
    
   return None  
