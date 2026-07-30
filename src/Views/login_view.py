import customtkinter as ctk
from src.Controller.auth_controller import Auth_validacao
# --- CONFIGURAÇÕES DE TEMA ---
ORANGE_FLIPPER = "#FF8C00"
DARK_BG = "#222121"
LCD_COLOR = "#FFB84D"
TEXT_DARK = "#1A1A1A"
class LoginClientView(ctk.CTk):
    def  __init__(self):
        super().__init__()        
        self.title("CibertoolBox/Login")
        self.eval('tk::PlaceWindow . center')
        self.geometry("650x400")
        self.resizable(False,False)
        self.configure(fg_color=DARK_BG)
        self.login_inicial()
    def login_inicial(self):
    # Container principal para troca de telas
        self.lcd = ctk.CTkFrame(self, fg_color=LCD_COLOR, width=300, height=120, corner_radius=10)
        self.lcd.pack(pady=20)
        self.lcd_label = ctk.CTkLabel(
            self.lcd, text="> CIBER_TOOLBOX\n> STATUS: LOCKED\n> INSERT KEY",
            text_color=TEXT_DARK, font=("Consolas", 16, "bold")
        )
        self.lcd_label.place(relx=0.5, rely=0.5, anchor="center")
        self.user = ctk.CTkEntry(self, placeholder_text="Operator ID", width=250, border_color=ORANGE_FLIPPER)
        self.user.pack(pady=10)
        self.pwd = ctk.CTkEntry(self, placeholder_text="Access Code", show="*", width=250, border_color=ORANGE_FLIPPER)
        self.pwd.pack(pady=10)

        self.btn = ctk.CTkButton(
            self, text="UNLOCK SYSTEM", fg_color=ORANGE_FLIPPER, 
            text_color="black", font=("Arial", 14, "bold"), command=lambda: Auth_validacao.validar_login(self.user, self.pwd))
        self.btn.pack(pady=20)
