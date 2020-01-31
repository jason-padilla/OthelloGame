import tkinter
import start_up_menu_gui
import game_logic as gamelogic

FONT = ('Times New Roman', 20)

class GameBoard:
    def __init__(self,rows,cols,first_player,win_type):
        self.rows = rows
        self.cols = cols
        self.current_player = first_player
        self.corner_piece = 'WHITE'
        self.score = {'Black':2,'White':2}
        self.othello_game = gamelogic.OthelloGame(self.rows,self.cols,first_player,win_type)
        self.game_board = self.othello_game.game_board
        self._game_window = tkinter.Tk()
        self._game_window.title('Othello')
        #Starting dimension and position of the window
        self._game_window.geometry("435x350+500+200")
        
        #Black Score Label
        self._black_score_label = tkinter.Label(master = self._game_window, text = 'Black: ' + str(self.score['Black']), font = FONT, background = 'black', foreground = 'white')
        self._black_score_label.grid(row = 0, column = 0, sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W )
        
        #White Score Label
        self._white_score_label = tkinter.Label(master = self._game_window, text = 'White: '+ str(self.score['White']), font = FONT,background = 'white', foreground = 'black')
        self._white_score_label.grid(row = 0, column = 1, sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W )

        #Game Canvas -- where all the pieces will be placed
        self._game_canvas = tkinter.Canvas(master = self._game_window, background = 'green')
        self._game_canvas.grid(row = 1, column = 0, columnspan = 2, padx = 0, pady = 0,sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        #Turn Label
        self._turn_label = tkinter.Label(master = self._game_window, text = self.current_player + ' Player Your Turn', font = FONT, background = 'brown', foreground = 'white')
        self._turn_label.grid(row = 2, column = 0, columnspan = 2, sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W ) 

        #Weight for how fast to expand when resizing the window
        self._game_window.rowconfigure(0, weight = 1)
        self._game_window.rowconfigure(1, weight = 15)
        self._game_window.rowconfigure(2, weight = 0)
        self._game_window.columnconfigure(0, weight = 15)
        self._game_window.columnconfigure(1, weight = 15)

        self._game_canvas.bind('<Configure>', self.display_control)
        
    def Start(self):
        '''This function helps the game to start'''
        self._game_window.mainloop()

    def _display_cells_and_pieces(self):
        ''' 
            This function uses the game board and the amount of rows and columns to display
            the iniated pieces and spaces for the game to begin
        '''
        #Takes the width of the canvas and divides it by the amount of cols to get the width of each cell
        cell_width = self._game_canvas.winfo_width()/self.cols
        #Takes the height of the canvas and divides it by the amount of rows to get the height of each cell
        cell_height = self._game_canvas.winfo_height()/self.rows
        #For every row and every col it creates lines on the canvas to emulate cells in a board game
        for row in range(self.rows):
            for col in range(self.cols):
                x1 = col * cell_width
                y1 = row * cell_height
                x2 = x1 + cell_width 
                y2 = y1 + cell_height
                cell = self._game_canvas.create_rectangle(x1,y1,x2,y2,fill = 'green', outline = 'black', tag = (row,col))
                #If the cell is pressed than it will make the command move_made
                self._game_canvas.tag_bind(cell,'<ButtonPress-1>',self.move_made)
                #As it goes creating each square it checks to see if the the cell has a piece in the game_board
                #if it does, than it places an oval(a piece) on the canvas that is fitted to each corner of the cell
                if self.game_board[row][col] == 'B':
                    self._game_canvas.create_oval(x1+1,y1+1,x2-1,y2-1,fill='#000000')
                elif self.game_board[row][col] == 'W':
                    self._game_canvas.create_oval(x1+1,y1+1,x2-1,y2-1,fill='#FFFFFF')

    def display_control(self,event):
        '''
            This is a function as a response to the canvas being binded. It calls out to another function to display all the
            cells and the pieces.
        '''
        self._display_cells_and_pieces()     
      
    def change_turn(self,color:str):
        '''This function changes the color of self.first so that the game can rotate turns'''
        if self.othello_game.current_color == 'W':
            self.current_player = 'White'
        elif self.othello_game.current_color == 'B':
            self.current_player = 'Black'

    def move_made(self,event):
        ''' This function takes in the players mouse clicks and adds a piece to the according location. It also
            changes the score of the board. In addition it checks to see if the game should end or keep on going.
        '''
        x = event.x
        y = event.y
        #This will find the closest x and y coordinates where the user has clicked on
        cell = self._game_canvas.find_closest(x,y)[0]
        position = self._game_canvas.gettags(cell)
        move = [int(position[0]),int(position[1])]
        #Tries to make the move indicated by where the user has clicked on
        #if the move is invalid than the game logic will raise an InvalidMoveException
        #The Exception will print to the user that it is an invalid move and will allow them to try again
        try:
            #Will make move inside the game logic class
            self.othello_game.make_move(move)
            #This changes the score on screen depending on the results of the game
            self._black_score_label['text'] = 'Black:',self.othello_game.return_score()['Black']
            self._white_score_label['text'] = 'White:',self.othello_game.return_score()['White']

            self._display_cells_and_pieces()
            #Once the move has been made, change the indication of which player's turn it is
            self.change_turn(self.current_player)
            self._turn_label['text'] = self.current_player +' Player Your Turn'
            #If the game is over than this function will return True else it will be false and the game will continue
            if self.othello_game.game_over() == True:
                #Checks to see who the winner is and assigns the winner for it to be displayed
                if self.othello_game.decide_winner() == 'B':
                    winner = '  Black Player Wins!! '
                    GameOver(winner,self._game_window)                
                elif self.othello_game.decide_winner() == 'W':
                    winner = '  White Player Wins!! '
                    GameOver(winner,self._game_window)
                else:
                    winner = 'Its A Tie!'
                    GameOver(winner,self._game_window)
                # if self.othello_game.return_score()['Black'] < self.othello_game.return_score()['White']:
                #     winner = '  White Player Wins!! '
                #     #Displays the Game Over Window and the winner
                #     GameOver(winner,self._game_window)
                # elif self.othello_game.return_score()['Black'] > self.othello_game.return_score()['White']:
                #     winner = '  Black Player Wins!! '
                #     GameOver(winner,self._game_window)
                # else:
                #     winner = 'Its A Tie!'
                #     GameOver(winner,self._game_window)
        except:
            print("InvalidMoveError: Try a different cell")



class GameOver:
    '''
        This is a small pop up window that shows up after the game is over. It gives the option to play again or stop playing
    '''
    def __init__(self,results,window):
        #Previous window passed on to still display it in the bacl
        self._game_window = window
        #New current window with the result
        self._results_window = tkinter.Tk()
        self._results_window.geometry("+630+350")
        self._results_window.title("Game Over")

        #Winner Score Label
        self._winner_score = tkinter.Label(master = self._results_window, text = results, font = ('Times New Roman', 30),background = 'white', foreground = 'black')
        self._winner_score.grid(row = 0, column = 0, columnspan = 2, sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W )
        
        #Play Again Label
        self._play_again_button = tkinter.Button(master = self._results_window, text = 'Play Again', foreground = 'black')
        self._play_again_button.grid(row = 1, column = 0,padx = 10, pady = 10,sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W )
        self._play_again_button.bind('<ButtonPress-1>', self.play_again)

        #End Game Label
        self._end_game_button = tkinter.Button(master = self._results_window, text = 'End Game', foreground = 'black')
        self._end_game_button.grid(row = 1, column = 1, padx = 10, pady = 10, sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W )
        self._end_game_button.bind('<ButtonPress-1>', self.end_game)

    def play_again(self,event):
        ''' 
            This is a command function as a response to the 'play again' button. It will destroy the previous game window
            and will redirect to the Start window.
        '''
        self._game_window.destroy()
        self._results_window.destroy()
        start_up_menu_gui.StartUpMenu()

    def end_game(self,event):
        '''
            This is a command function as a response to the 'end game' button. It Will destroy the previous game and end
            any future interaction.
        '''
        self._results_window.destroy()
        self._game_window.destroy()
        





    
    
    
