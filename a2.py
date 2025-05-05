from game import Game
from ui import UI


def main ():
   """
   Starts the game, handles setup and user commands.
   """
   rows = int(input(""))
   cols = int(input("")) 


   game = Game(rows,cols)


   config = input("")


   if config == "CONTENTS":
       contents = [] #should i split this into a function
       for i in range(rows):
           line = input()
           contents.append(list(line))
       print(contents)
       game.create_content_field(contents)
       game.resolve_matches()
      


   while True:
      
       UI.display_field(game)
       game.remove_matches()


       if game.check_virus():
           print('LEVEL CLEARED')
       command = input()


       if command.startswith("Q"):
           break
       if command.startswith("F"):
           game.create_faller(command)
       if not command:
           game.apply_gravity()
       if command.startswith("A"):
           game.rotate_clockwise()
       if command.startswith("B"):
           game.rotate_counter()
       if command.startswith("<"):
           game.move_left()
       if command.startswith(">"):
           game.move_right()
       if command.startswith("V"):
           game.create_virus(command)
       game.resolve_matches()
      
if __name__ == "__main__":
   main()
