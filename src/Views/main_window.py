import customtkinter as ctk
ORANGE_FLIPPER = "#FF8C00"
DARK_BG = "#222121"
LCD_COLOR = "#FFB84D"
TEXT_DARK = "#1A1A1A"
class ClientView(ctk.CTk):
    def  __init__(self):
        super().__init__()        
        self.title("CibertoolBox/Menu")
        self.eval('tk::PlaceWindow . center')
        self.geometry("650x400")
        self.configure(fg_color=DARK_BG)
        self.resizable(False,False)
    