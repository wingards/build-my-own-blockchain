
import os
import tkinter as tk
from tkinter import ttk

from sha import to_sha
from chain import BlockChain
from wallet import Wallet

class Main_Window():
    def __init__(self, window, wallet):

        self.window = window
        self.wallet = wallet
        self.blockchain = self.wallet.blockchain

        self.main_frame = tk.Frame(self.window)
        self.main_frame.pack()

        self.set_ui()

    def set_ui(self):

        #main window
        self.window.title('Mainpage')
        self.window.geometry('800x300')
        self.window.configure(background='dim gray')

        #top frame
        #
        self.top_frame = tk.Frame(window)
        self.top_frame.pack(fill=tk.X)

        #mine button
        mine_button = tk.Button(self.top_frame, text='mine', font='500', bg='red', fg='black', height=5, command=self.click_mine)
        mine_button.pack(side=tk.LEFT, fill=tk.X)

        #update button
        update_button = tk.Button(self.top_frame, text='update', font='500', bg='red', fg='black', height=5, command=self.click_update)
        update_button.pack(side=tk.LEFT, fill=tk.X)

        #clear button
        clear_button = tk.Button(self.top_frame, text='clear', font='500', bg='red', fg='black', height=5, command=self.click_clear)
        clear_button.pack(side=tk.LEFT, fill=tk.X)

        #connect info
        self.addrString = tk.StringVar()
        self.portString = tk.StringVar()

        self.addr_entry = tk.Entry(self.top_frame, width=20, textvariable=self.addrString)
        self.port_entry = tk.Entry(self.top_frame, width=20, textvariable=self.portString)
        
        self.addr_entry.pack(side=tk.LEFT, fill=tk.X)
        self.port_entry.pack(side=tk.LEFT, fill=tk.X)

        conn_button = tk.Button(self.top_frame, text='conn', font='500', bg='red', fg='black', height=5, command=self.click_conn)
        conn_button.pack(side=tk.LEFT, fill=tk.X)

        disc_button = tk.Button(self.top_frame, text='disc', font='500', bg='red', fg='black', height=5, command=self.click_disc)
        disc_button.pack(side=tk.LEFT, fill=tk.X)

        #exit
        exit_button = tk.Button(self.top_frame, text='exit', font='500', bg='snow', fg='red', height=5, command=self.click_exit)
        exit_button.pack(side=tk.LEFT, fill=tk.X)
        
        #bottom frame
        #
        self.bottom_frame = tk.Frame(window)
        self.bottom_frame.pack(fill=tk.X)

        self.mine_options = ttk.Combobox(self.bottom_frame, value=["Proof of Work", "Proof of Stack"], state='readonly', justify='center')
        self.mine_options.bind('<<ComboboxSelected>>', self.select_mine)
        self.mine_options.pack(side=tk.TOP, fill=tk.X)

        self.Chain_Info = tk.Text(self.bottom_frame, bg='black', fg='white')
        self.Chain_Info.pack(fill=tk.X)

    def click_mine(self):
        self.wallet.mine()
        self.edit_info(self.wallet.blockchain.to_json())

    def click_update(self):
        self.wallet.update_chains()
        self.edit_info(self.wallet.blockchain.to_json())
    
    def click_clear(self):
        self.blockchain.clear_chain()
        self.blockchain.init_chain()
        self.blockchain.save_chain()

        self.edit_info(self.wallet.blockchain.to_json())

    def click_conn(self):
        self.wallet.connect(self.addrString.get(), int(self.portString.get()))
        self.addr_entry.config(state='disabled')
        self.port_entry.config(state='disabled')

    def click_disc(self):

        self.wallet.disconnect(self.addrString.get(), int(self.portString.get()))

        self.addr_entry.delete(0, 'end')
        self.port_entry.delete(0, 'end')
        self.addr_entry.config(state='normal')
        self.port_entry.config(state='normal')

    def select_mine(self, event):
        pass

    def click_exit(self):
        print('Exit Program')
        self.exit_program()

    def exit_program(self):
        self.window.destroy()
        os._exit(1)

    def edit_info(self, info):
        self.Chain_Info.delete(1.0, "end")
        self.Chain_Info.insert(tk.END, info)

if __name__ == '__main__':
   
    wallet = Wallet()
    wallet.listen()

    window = tk.Tk()
    app = Main_Window(window, wallet)

    app.edit_info(wallet.blockchain.to_json())

    window.mainloop()

