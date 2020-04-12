
import os
import tkinter as tk
from tkinter import ttk

from wallet import Wallet

class Main_Window():
    def __init__(self, wallet, run = True):

        self.window = tk.Tk()
        self.wallet = wallet
        self.blockchain = self.wallet.blockchain

        self.main_frame = tk.Frame(self.window)
        self.main_frame.pack()

        self.set_ui()

        if run:
            self.run_ui()
        else:
            print("Main_Window running in background...")

    def set_ui(self):

        #main window
        self.window.title('Mainpage')
        self.window.geometry('800x300')
        self.window.configure(background='dim gray')

        #top frame
        #
        self.top_frame = tk.Frame(self.window)
        self.top_frame.pack(fill=tk.X)

        #mine button
        self.mine_button_text = tk.StringVar()
        self.mine_button_text.set('mine')
        mine_button = tk.Button(self.top_frame, textvariable=self.mine_button_text, font='500', bg='red', fg='black', height=5)
        mine_button.pack(side=tk.LEFT, fill=tk.X)
        mine_button.bind('<Button-1>', self.click_mine)
        mine_button.bind('<Button-3>', self.click_mine)

        #update button
        update_button = tk.Button(self.top_frame, text='update', font='500', bg='red', fg='black', height=5, command=self.click_update)
        update_button.pack(side=tk.LEFT, fill=tk.X)

        #clear button
        clear_button = tk.Button(self.top_frame, text='clear', font='500', bg='red', fg='black', height=5, command=self.click_clear)
        clear_button.pack(side=tk.LEFT, fill=tk.X)

        #connect info
        self.conn_frame = tk.Frame(self.top_frame)
        self.conn_frame.pack(side=tk.LEFT, fill=tk.X)

        self.addrString = tk.StringVar()
        self.portString = tk.StringVar()

        self.addr_entry = tk.Entry(self.conn_frame, width=20, textvariable=self.addrString)
        self.port_entry = tk.Entry(self.conn_frame, width=20, textvariable=self.portString)
        self.addr_entry.grid(row=0, column=0)
        self.port_entry.grid(row=0, column=1)

        self.conn_list = tk.Listbox(self.conn_frame, height=4)
        self.conn_list.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S)

        conn_button = tk.Button(self.top_frame, text='conn', font='500', bg='red', fg='black', height=5, command=self.click_conn)
        conn_button.pack(side=tk.LEFT, fill=tk.X)

        disc_button = tk.Button(self.top_frame, text='disc', font='500', bg='red', fg='black', height=5, command=self.click_disc)
        disc_button.pack(side=tk.LEFT, fill=tk.X)

        #exit
        exit_button = tk.Button(self.top_frame, text='exit', font='500', bg='snow', fg='red', height=5, command=self.click_exit)
        exit_button.pack(side=tk.LEFT, fill=tk.X)

        #bottom frame
        #
        self.bottom_frame = tk.Frame(self.window)
        self.bottom_frame.pack(fill=tk.X)

        self.mine_options = ttk.Combobox(self.bottom_frame, value=["Proof of Work", "Proof of Stack"], state='readonly', justify='center')
        self.mine_options.bind('<<ComboboxSelected>>', self.select_mine)
        self.mine_options.pack(side=tk.TOP, fill=tk.X)

        self.Chain_Info = tk.Text(self.bottom_frame, bg='black', fg='white')
        self.Chain_Info.pack(fill=tk.X)

    def click_mine(self, event):

        if event.num == 3:#right click
            if self.mine_button_text.get() == 'mine':
                self.mine_button_text.set("keep\nmining")
            else:
                self.mine_button_text.set("mine")
            return

        self.wallet.mine()
        self.edit_info(self.wallet.blockchain.to_json())

    def click_update(self):
        self.wallet.update_chains()

        self.update_connect()
        self.edit_info(self.wallet.blockchain.to_json())

    def click_clear(self):
        self.blockchain.clear_chain()
        self.blockchain.init_chain()
        self.blockchain.save_chain()

        self.edit_info(self.wallet.blockchain.to_json())

    def update_connect(self):
        self.conn_list.delete(0, 'end')

        for (addr, port) in self.wallet.list_connect():
            self.conn_list.insert("end", "{}:{}".format(addr, int(port)))

    def wallet_connect(self, addr, port):
        self.wallet.connect(addr, int(port))

        self.update_connect()

    def click_conn(self):
        self.wallet_connect(self.addrString.get(), int(self.portString.get()))

        self.addr_entry.delete(0, 'end')
        self.port_entry.delete(0, 'end')
        #self.addr_entry.config(state='disabled')
        #self.port_entry.config(state='disabled')

    def click_disc(self):
        
        idx = self.conn_list.curselection()
        if not idx:
            return
        info = self.conn_list.get(idx).split(":")
        self.wallet.disconnect(info[0], int(info[1]))

        self.update_connect()

        #self.addr_entry.config(state='normal')
        #self.port_entry.config(state='normal')

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

    def run_ui(self):
        print("Activate User Interface")
        self.update_connect()
        self.window.mainloop()

if __name__ == '__main__':
    wallet = Wallet()
    wallet.listen()

    app = Main_Window(wallet, False)

    app.edit_info(wallet.blockchain.to_json())
    app.wallet_connect("127.0.0.1", 9527)

    app.run_ui()
