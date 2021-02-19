import tkinter
from PIL import ImageTk,Image
import game_board_gui as Gui
FONT = ('Times New Roman', 25)

class StartUpMenu:
    def __init__(self):
        self._start_up_menu_window = tkinter.Tk()
        self._start_up_menu_window.resizable(False,False)
        self._start_up_menu_window.title("Start Up Menu")
        self._start_up_menu_window.config(background = "#2C9342")
        #default size of window + starting position on screen
        self._start_up_menu_window.geometry("558x340+500+200")
        
        #Header
        self.welcome_label = tkinter.Label(master = self._start_up_menu_window, text = 'Welcome To Othello!', font = ('Times New Roman', 30),background = 'black', foreground = 'white')
        self.welcome_label.grid(row= 0, column = 0,columnspan = 2,sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W )

        #Othello Image
        logo_image = Image.open("images/logo4.jpg")
        logo_image = logo_image.resize((150,150),Image.ANTIALIAS)
        self.my_img = ImageTk.PhotoImage(logo_image)
        self._logo_label = tkinter.Label(master = self._start_up_menu_window, image = self.my_img,background = '#2C9342',pady = 10)
        self._logo_label.grid(row= 1, column = 0,columnspan = 2 )

        #Rows Selection Dropdown
        #Frame encapsulates the 'Row' label and the dropdown in row 2, col 0 of the window
        self._row_frame = tkinter.Frame(master = self._start_up_menu_window,background = '#2C9342')
        self._row_frame.grid(row = 2, column = 0)
        #Rows label
        self._row_label = tkinter.Label(master = self._row_frame,text = 'Rows:',font = FONT,background = '#2C9342')
        self._row_label.grid(row = 0, column = 0)
        #Rows dropdown
        self._rows_default_value = tkinter.IntVar()
        self._rows_default_value.set(8)
        self._row_menu = tkinter.OptionMenu(self._row_frame,self._rows_default_value, 4,6,8,10,12,14,16)
        self._row_menu.grid(row = 0, column = 1,padx = 20, pady = 10)
        self._row_menu.config(bg = '#2C9342')

        #Cols Selection Dropdown
        #Frame encapsulates the 'Cols' label and the dropdown in row 2, col 1 of the window
        self._cols_frame = tkinter.Frame(master = self._start_up_menu_window,background = '#2C9342')
        self._cols_frame.grid(row = 2, column = 1)
        #Cols label
        self._column_label = tkinter.Label(master = self._cols_frame,text = 'Columns:',font = FONT,background = '#2C9342')
        self._column_label.grid(row = 0, column = 0)
        #Cols dropdown
        self._cols_default_value = tkinter.IntVar()
        self._cols_default_value.set(8)
        self._cols_menu = tkinter.OptionMenu(self._cols_frame,self._cols_default_value, 4,6,8,10,12,14,16)
        self._cols_menu.grid(row = 0, column = 1,padx = 10, pady = 10)
        self._cols_menu.config(bg = '#2C9342')
        
        #First Player Selection Dropdown
        #Frame encapsulates the 'First Player' label and the dropdown in row 3, col 0 of the window
        self._player_frame = tkinter.Frame(master = self._start_up_menu_window,background = '#2C9342')
        self._player_frame.grid(row = 3, column = 0, pady=10)
        #First Player label
        self._player_label = tkinter.Label(master = self._player_frame,text = 'First Player:',font = FONT,background = '#2C9342')
        self._player_label.grid(row = 0, column = 0)
        #First Player dropdown
        self._players_default_variable = tkinter.StringVar()
        self._players_default_variable.set('Black')
        self._player_menu = tkinter.OptionMenu(self._player_frame,self._players_default_variable,'Black','White')
        self._player_menu.grid(row = 0, column = 1)
        self._player_menu.config(bg = '#2C9342')
        
        #Victory Type Selection Dropdown
        #Frame encapsulates the 'First Player' label and the dropdown in row 3, col 1 of the window
        self._type_frame = tkinter.Frame(master = self._start_up_menu_window,background = '#2C9342')
        self._type_frame.grid(row = 3, column = 1, padx = 10, pady = 10)
        #Victory Type label
        self._type_label = tkinter.Label(master = self._type_frame,text = 'Victory Type:',font = FONT,background = '#2C9342')
        self._type_label.grid(row = 0, column = 0)
        #Victory Type dropdown
        self._types_default_value = tkinter.StringVar()
        self._types_default_value.set('Most')
        self._type_menu = tkinter.OptionMenu(self._type_frame,self._types_default_value,'Most','Least')
        self._type_menu.grid(row = 0, column = 1)
        self._type_menu.config(bg = '#2C9342')

        #Start Game button
        self.start_button = tkinter.Button(master = self._start_up_menu_window, text = 'Start Game', font = FONT, highlightbackground = 'blue')
        self.start_button.grid(row= 4, column = 0, sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        self.start_button.bind('<ButtonPress-1>', self.start_game)
        
        #Cancel Game button
        self.cancel_button = tkinter.Button(master = self._start_up_menu_window, text = 'Cancel Game', font = FONT, highlightbackground = 'red')
        self.cancel_button.grid(row= 4, column = 1, sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        self.cancel_button.bind('<ButtonPress-1>', self.cancel_game)

    def initiate(self):
        self._start_up_menu_window.mainloop()
        
    def start_game(self,event):
        '''
            This is a command function for 'self.start_button'. Once the button is pressed
            it closes the current tkinter window and opens a new one with the gameboard displayed.
        '''
        self._start_up_menu_window.destroy()
        rows = int(self._rows_default_value.get())
        cols = int(self._cols_default_value.get())
        first_player = self._players_default_variable.get()
        win_type = self._types_default_value.get()
        Gui.GameBoard(rows,cols,first_player,win_type).Start()

    def cancel_game(self,event):
        '''
            This is a command function for 'self.cancel_button'. Once the button is pressed
            it will close the window.
        '''
        self._start_up_menu_window.destroy()

if __name__ == '__main__':
    StartUpMenu().initiate()

        
        
    


    
