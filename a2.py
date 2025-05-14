from game import Game
from ui import UI


def main():
    """
    Starts the game, handles setup and user commands.
    """
    try:
        rows = int(input(""))
        cols = int(input(""))
    except ValueError:
        return
    
    middle = cols//2
    left_col = middle - 1
    right_col = middle

    game = Game(rows, cols)

    config = input("")

    if config == "CONTENTS":
        contents = []
        for i in range(rows):
            try:
                line = input()
                if len(line) != cols:
                    return
                contents.append(list(line))
            except:
                return
        try:
            game.create_content_field(contents)
            game.resolve_matches()
        except:
            return

    while True:
        try:
            UI.display_field(game)
            game.remove_matches()

            if game.check_virus():
                print('LEVEL CLEARED')
            command = input()

            if command.startswith("Q"):
                break
            if command.startswith("F"):
                try:
                    game.create_faller(command)
                    game.faller_start_state()
                    if not game.can_create_faller(1, left_col, right_col):
                        UI.display_field(game)
                        print("GAME OVER")
                        break
                except:
                    pass

            if not command:
                game.apply_gravity_faller()
                game.apply_gravity_vitamin()

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
            
        except:
            break


if __name__ == "__main__":
    main()
