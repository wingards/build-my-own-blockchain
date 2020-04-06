
import os
import tkinter as tk

from app import Main_Window

from wallet import Wallet

if __name__ == '__main__':
   
    wallet = Wallet()
    wallet.listen()

    App = Main_Window(tk.Tk(), wallet, False)
