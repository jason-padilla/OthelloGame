BLACK = 'B'
WHITE = 'W'

class InvalidMoveException(Exception):
    ''' Raised whenever there is an invalid move '''
    
class OthelloGame:
    def __init__(self, rows: int, cols: int, starting_color: str, win_type:str):
        ''' Initialize all of the games settings and creates the board. '''
        self.rows = rows
        self.cols = cols
        self.dimension = rows
        self.current_color = starting_color
        self.win_type = win_type
        self.game_board = self.create_game_board(starting_color, rows, cols)

    def create_game_board(self,starting_color:str, rows: int, cols:int) -> [[str]]:
        '''
            Creates the game board by making a list of lists [[],[]] and implementing
            the first four center pieces of the game.
        '''
        board = []
        #Create the initial 2D array
        for row in range(rows):
            board.append([])
            for col in range(cols):
                board[-1].append('.')

        #Add the starting peices based on the first player
        if starting_color == 'Black':
            self.current_color = BLACK
            board[(rows//2 - 1)][(cols//2 - 1)] = 'B' #TopLeft
            board[(rows//2 - 1)][(cols//2)] = 'W'     #TopRight
            board[(rows//2)][(cols//2)] = 'B'         #BottomLeft
            board[(rows//2)][(cols//2 - 1)] = 'W'     #BottomRight

        else:
            self.current_color = WHITE
            board[(rows//2 - 1)][(cols//2 - 1)] = 'W' #TopLeft
            board[(rows//2 - 1)][(cols//2)] = 'B'     #TopRight
            board[(rows//2)][(cols//2)] = 'W'         #BottomLeft
            board[(rows//2)][(cols//2 - 1)] = 'B'     #BottomRight
        return board

    def print_board(self) -> None:
        '''
            ***Only to be used with the Tkinter Interface***
            Prints out a 2D array row by row with its contents including either: 'B','W' or '.'
            
        '''
        #prints numbers at the top of the displayed game board
        for num in range(self.dimension):
            print(num, end = ' ')
        #prints out each piece of the game board either: 'B','W' or '.'
        for row in range(self.rows):
            print('\n')
            for col in range(self.cols):
                print(self.game_board[row][col], end = ' ')
        print('\n')

    def make_move(self,move:[int,int]) -> None:
        '''
            This function takes in a move[int,int] and First checks if the space
            is available and within board boundaries. Second it checks to see if there 
            are any opposite colored pieces it can transform. Third it sees if there is 
            a same colored piece in that direction to complete its process. Once all the 
            requirements are met it places the piece in the desired location and changes 
            any opposite colored pieces.
            If the move or direction is invalid it will raise an Invalid Exception.
        '''
        #Checks to see if there is an empty space and that it is within boundaries
        if self.is_cell_available(move):
            #Checks to see if that move has any opposites in 8 directions
            opposite_pieces = self.find_surrounding_opposites(move)
            if(len(opposite_pieces) != 0):
                flipped = 0
                for direction in opposite_pieces:
                    #Check to see if their is going to be a piece of the same color in that direction
                    if(self.is_valid_direction(move,direction)):
                        #If it is a valid direction than start changing pieces in that direction
                        self.flip_opposite_cells(move,direction)
                        flipped += 1
                        #place a piece of the current color in that location
                        self.game_board[move[0]][move[1]] = self.current_color
                #a move could be available and the direction could be valid but
                #if it didnt flip any tiles than it wasnt a valid move
                if (flipped == 0):
                    raise InvalidMoveException()
            #if there are no opposite colored pieces in that move than raise InvalidException
            else:
                raise InvalidMoveException()
        #change the color of to the next players turn
        self.current_color = self.opposite_color(self.current_color)   
        #If a move is not possible to be made for the next player
        #Than change the color back and the current player goes again
        if not (self.is_move_possible()):
            self.current_color = self.opposite_color(self.current_color)   

    def is_cell_available(self,move:[int,int]) -> bool:
        '''
            This function returns True only if the move is not out of bounds ([0-7,0-7])
            and if it is not already occupied by a piece 'B' or 'W'.
            Else it raises an exception.
        '''
        if(self.move_out_of_bounds(move)):
            raise InvalidMoveException()
        if (self.game_board[move[0]][move[1]] == 'B' or self.game_board[move[0]][move[1]] == 'W'):
            raise InvalidMoveException()
        else:
            return True


    def move_out_of_bounds(self,move:[int,int]) -> bool:
        '''
            This is a helper function that just checks to see if a move is within the
            game board's boundaries
        '''
        if (move[0] < 0 or move[1] < 0):
            return True
        elif(move[0] >= self.dimension or move[1] >= self.dimension):
            return True
        else:
            return False

    def is_valid_direction(self,starting_position:[int,int],direction:[int,int]) -> bool:
        '''
            This function checks to see if there is a piece of the same color in that direction.
            It does so by adding the direction to the starting position.
            If there is no piece of the same color than it goes out of bounds and return False.

            Ex: starting: [0,0] direction: [2,2] thats bottom right
                to keep moving bottom right you need to add 2,2 to 0,0 then 4,4 then 6,6 etc.
        '''
        #Variables that will keep changing in order to keep moving forward
        direction_x = direction[0]
        direction_y = direction[1]
    
        while True:
            #If the out of bounds function returns True than the direction is invalid
            if(self.move_out_of_bounds([starting_position[0] + direction_x,starting_position[1] + direction_y])):
                return False

            if(self.game_board[starting_position[0] + direction_x][starting_position[1] + direction_y] == self.current_color):
                return True

            #Adds it by its own direction in order to keep looking forward
            direction_x += direction[0]
            direction_y += direction[1]
    
    def find_surrounding_opposites(self,move:[int,int]) -> [[int,int]]:
        '''
            This function checks in 8 directions to see if there is a piece of an opposite color. 
            If there is than it it stores the location in an array of arrays and returns the array. 
        '''
        opposite_surroundings = []
        #-1 to 2 is the amount needed to add to go from the current position to a certain direction
        for row in range(-1,2):
            for col in range(-1,2):
                #Check to see if the direction that we are going to check isnt going to be an out of bounds cell
                if not self.move_out_of_bounds([move[0] + row,move[1] + col]):
                    #Stores the color of the possible direction
                    possible_direction = self.game_board[move[0] + row][ move[1] + col]
                    #if the color is opposite to the current color than add the direction to the array
                    if(possible_direction == self.opposite_color(self.current_color)):
                        #Include only the number for the direction and not the checked cell 
                        #so it can continue to check in that direction and not just one cell
                        direction = [row,col]
                        opposite_surroundings.append(direction)
        return opposite_surroundings

    def flip_opposite_cells(self,starting_position:[int,int],direction:[int,int]) -> None:
        '''
            This function takes the chosen valid move as the starting position and then increments it
            by the directiontional x and y axis. It checks if the next position is not of the same color
            than it will flip it.
        '''
        #Variables that will keep changing in order to keep moving forward
        direction_x = direction[0]
        direction_y = direction[1]
        
        #While the piece isnt of the same color than keep changing the color
        while(self.game_board[starting_position[0] + direction_x][starting_position[1] + direction_y] != self.current_color ):
            self.game_board[starting_position[0] + direction_x][starting_position[1] + direction_y] = self.current_color
            direction_x += direction[0]
            direction_y += direction[1]
        
    def opposite_color(self,color: str) -> None:
        '''
            This is a helper function that simply returns the opposite color than what is given
        '''
        if color == BLACK:
            return WHITE
        if color == WHITE:
            return BLACK

    def is_move_possible(self) -> bool:
        '''
            This function iterates through an array of empty cells and then checks to see if a move is 
            possible from that cell. This then indicates wether a player can continue playing because it has
            valid moves it can make.
        '''
        empty_cells = self.find_empty_cells()
        for cell in empty_cells:
            #Checks to see if that move has any opposites in 8 directions
            opposite_pieces = self.find_surrounding_opposites(cell)
            if(len(opposite_pieces) != 0):
                for direction in opposite_pieces:
                    #Check to see if their is going to be a piece of the same color in that direction
                    if(self.is_valid_direction(cell,direction)):
                        return True
        return False

    def find_empty_cells(self) -> [[int,int]]:
        '''
            This is a helper function that returns an array of arrays with empty cells
        '''
        empty_cells = []
        for row in range(self.rows):
            for col in range(self.cols):
                if(self.game_board[row][col] == '.'):
                    empty_cells.append([row,col])
        return empty_cells

    def return_score(self) -> {str:int,str:int}:
        '''
            This function counts all the Black pieces and all the White pieces and returns 
            a dict with the score of each one.
        '''
        scores = {'Black':0,'White':0}

        for row in range(self.rows):
            for col in range(self.cols):
                if self.game_board[row][col] == 'B':
                    scores['Black'] += 1
                if self.game_board[row][col] == 'W':
                    scores['White'] += 1
        return scores

    def game_over(self) -> bool:
        '''
            This function checks to see if the either of the players can make a move in the
            current state of the game. If neither can than the game will end
        '''
        #current player checks to see if it has a possible move to make
        player1 = self.is_move_possible()
        #switches color to see if the next player has a possible move to make
        self.current_color = self.opposite_color(self.current_color)
        player2 = self.is_move_possible()
        self.current_color = self.opposite_color(self.current_color)
        #if player1 is False and player2 is False than return True(it is over) otherwise False(it is not over)
        if not player1:
            if not player2:
                return True
        return False

    def decide_winner(self) -> str:
        '''
            This function counts all the Black and White pieces and compares to see
            which one has the either the most or the least depending on the Win Type.
        '''

        black = 0
        white = 0
        for row in self.game_board:
            for cell in row:
                if cell == BLACK:
                    black += 1
                if cell == WHITE:
                    white += 1
                    
        if self.win_type == 'Most':
            if(black > white):
                return BLACK
            if(white > black):
                return WHITE
            else:
                return "tie"
        elif self.win_type == 'Least':
            if(black < white):
                return BLACK
            if(white < black):
                return WHITE
            else:
                return "tie"

### This is if you would like to play the game without the Tkinter Interface ###
# if __name__ == '__main__':
#     Game = OthelloGame(6,6,WHITE)
#     Game.print_board()
#     while(!Game.game_over()):
#         try:
#             print("Player's Turn is: " + Game.current_color)
#             col_input = input("Enter the col: ")
#             row_input = input("Enter the row: ")
#             Game.make_move([int(row_input),int(col_input)])
#             Game.print_board()
#         except:
#             Game.print_board()
#             print("Please enter a valid move")
#     print(Game.decide_winner())


    

