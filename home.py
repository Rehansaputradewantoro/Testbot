
from tkinter import  ttk
import tkinter
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class Home(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter. Frame.__init__(self, parent)
        self.controller = controller
      
        self.parent=parent
        self.grid( row=0,column=0, sticky='nsew',ipadx=1530,ipady=800)
        self.tab = ttk.Notebook(self)
        
        self.tab.grid(row=0, column=0, sticky='nsew',ipadx=1530,ipady=800)
        self.trade_tab = tkinter.Frame(self.tab, relief='groove',background='green')
        self.history_tab = tkinter.Frame(self.tab, relief='groove', borderwidth=1,background='green')
        self.order_book_tab = tkinter.Frame(self.tab, relief='groove', borderwidth=1,background='purple')
        self.settings_tab = tkinter.Frame(self.tab, relief='groove', borderwidth=1,background='green')
        self.about_tab = tkinter.Frame(self.tab, relief='groove', borderwidth=1,background='orange')
        self.transactions_tab = tkinter.Frame(self.tab, relief='groove', borderwidth=1,background='blue')
        self.transactions_label = tkinter.Label(self.transactions_tab, 
                                                text='Transactions', 
                                               borderwidth=1)
     

        self.transactions_list = tkinter.Listbox(self.transactions_tab, selectmode=tkinter.SINGLE, height=20, width=600)
        self.transactions_list.place(x=0, y=20, width=600, height=400)
        self.transactions_list.config(yscrollcommand=self.transactions_list.yview)
        
        read_transactions = pd.read_csv('ledger_transactions.csv')

        self.offers_list = tkinter.Listbox(self.transactions_tab, selectmode=tkinter.SINGLE, height=20, width=1100)
        self.offers_list.place(x=700, y=20, width=600, height=400)
      
        offers = pd.read_csv('ledger_offers.csv')
        self.offers_list.insert(tkinter.END, str(offers.__str__())  + '\n')
              
        self.transactions_list.insert(tkinter.END, str(read_transactions.__str__()+'\n'))
     
        self.offers_list.config(yscrollcommand=self.offers_list.yview)

       
        self.send_money_tab = tkinter.Frame(self.tab, relief='groove', borderwidth=1,background='gray')
        self.send_money_tab.grid(row=2, column=0, sticky='nsew')

        self.send_money_label = tkinter.Label(self.send_money_tab, text='Send Money', relief='groove', borderwidth=1)
        self.send_money_label.grid(row=1, column=0, sticky='nsew')

        self.receive_money_tab = tkinter.Frame(self.tab, relief='groove', borderwidth=1,background='gray')
        self.receive_money_tab.grid(row=2, column=0, sticky='nsew')

        self.receive_money_label = tkinter.Label(self.receive_money_tab, text='Receive Money', relief='groove', borderwidth=1)
        self.receive_money_label.grid(row=2, column=1, sticky=' nsew')

        self.licence_tab = tkinter.Frame(self.tab, relief='groove', borderwidth=1,background='gray')
        self.licence_tab.grid(row=5, column= 0,  rowspan=2, sticky='nsew')

        self.licence_label = tkinter.Label(self.licence_tab, text='Licence', relief='groove', borderwidth=1)
        self.licence_label.grid(row=6, column=0, sticky='nsew')

        self.about_tab = tkinter.Frame(self.tab, relief='groove', border=1,background='gray')
        self.about_tab.grid(row=6, column=1, sticky='nsew')

        self.balance_label = tkinter.Label(self.transactions_tab, text='Balance', relief='ridge')
        self.balance_label.grid(row=7, column=0, sticky='nsew')
        

                 
        read=pd.read_csv('balances.csv')
        
        self.balance_tree = ttk.Treeview(self.transactions_tab, selectmode='extended')
        self.balance_tree.place(x=10, y=20)

        columns = ('asset_code','asset_type','asset_code','limit','buying_liabilities','selling_liabilities','last_modified_ledger','is_authorized','is_authorized.1','is_authorized_to_maintain_liabilities','asset_code')
        self.balance_tree['columns'] = columns
        self.balance_tree['show'] = 'headings'
        self.balance_tree.heading('asset_code', text='Asset Code')
        self.balance_tree.heading('asset_type', text='Asset Type')
      
        self.balance_tree.heading('limit', text='Limit')
        self.balance_tree.heading('buying_liabilities', text='Buying Liabilities')
        self.balance_tree.heading('selling_liabilities', text='Selling Liabilities')
        self.balance_tree.heading('last_modified_ledger', text='Last Modified Ledger')
        self.balance_tree.heading('is_authorized', text='Is Authorized')
        self.balance_tree.heading('is_authorized.1', text='Is Authorized.1')
        self.balance_tree.heading('is_authorized_to_maintain_liabilities', text='Is Authorized To Maintain Liabilities')
        self.balance_tree.heading('asset_code', text='Asset Code')
        
        for index, row in read.iterrows():

            print(index,row)
            
            self.balance_tree.insert('', 'end', text=(row['asset_code'], row['asset_type'], row['limit'], row['buying_liabilities'], row['selling_liabilities'], row['last_modified_ledger'], row['is_authorized'], row['is_authorized.1'], row['is_authorized_to_maintain_liabilities']))
        

        self.account_tab =  tkinter.Frame(self.tab, relief='groove', borderwidth=1,background='gray')
        self.account_tab.place(x=0, y=0)
        self.account_canvas = tkinter.Canvas(self.account_tab, width=1400, height = 700,background= 'black',border=9)
        self.account_canvas.place(x=0, y=10)
        self.trade_server_text = tkinter.StringVar()
     
        self.toggled_button1 = tkinter.Button(self.trade_tab,bg='green',fg='white', text="START",width=20, command=lambda:self.start_bot())
        self.toggled_button1.place(x=400, y=410)                                                                                                                       
        self.toggled_button = tkinter.Button(self.trade_tab,bg='red',fg='white',text='STOP',width=20, command=lambda:self.stop_bot())
        self.toggled_button.place(x=600, y=410)

        self.trade_tree =  ttk.Treeview(self.trade_tab, selectmode='extended')
        self.trade_tree.place(x=0, y=500, width=1400)
        self.trade_tree['columns'] = ('symbol','timestamp','open', 'high', 'low', 'close', 'base_volume', 'counter_volume', 'trade_count')
        self.trade_tree['show'] = 'headings'
        self.trade_tree.heading('timestamp', text='timestamp')
        self.trade_tree.heading('symbol', text='symbol')
        self.trade_tree.heading('open', text='open')
        self.trade_tree.heading('high', text='high')
        self.trade_tree.heading('low', text='low')
        self.trade_tree.heading('close', text='close')
        self.trade_tree.heading('base_volume', text='base_volume')
        self.trade_tree.heading('counter_volume', text='counter_volume')
        self.trade_tree.heading('trade_count', text='trade_count')
       

        
        self.order_book_canvas = tkinter.Canvas( self.order_book_tab,relief='groove',background='black', borderwidth=1)
        self.order_book_canvas.place(x=10, y=100, width=1300, height=660)

        self.order_book_tree =  ttk.Treeview(self.order_book_tab, selectmode='browse')
        self.order_book_tree.place(x=0, y=30, width=300, height=760)
        self.order_book_tree['columns'] = ('price', 'quantity')
        self.order_book_tree['show'] = 'headings'
        self.order_book_tree.heading('price', text='price')
        self.order_book_tree.heading('quantity', text='quantity')
        order_book = pd.read_csv('order_book.csv')
        for index, row in order_book.iterrows():
            print(index,row)
            self.order_book_tree.insert('', 'end', text=(row['price'], row['quantity']))
        
        offers = pd.read_csv('ledger_offers.csv')
        self.offers_canvas = tkinter.Canvas( self.history_tab, width=300, height=700,bg='green', relief='groove',background='black', bd= 3)
        self.offers_canvas.place(x=300, y=30, width=300, height= 700,anchor= 'nw')
        self.offers_canvas.create_text(300, 40, text=offers.__str__(), font=('Arial',14), anchor= 'nw')

        self.history_canvas = tkinter.Canvas( self.history_tab, width=1300, height=300,bg='green', relief='groove',background='black',bd= 3)
        self.history_canvas.place(x=10, y=30 ,anchor= 'nw')
        self.history_canvas.create_text(300, 200, text='history', font=('Arial',14), anchor= 'nw')
        
        
        self.transactions_canvas = tkinter.Canvas( self.transactions_tab, width=1200, height=700,bg='green', relief='groove',background='black',bd= 3)
        self.transactions_canvas.place(x=0, y=30, width=1500, height= 700,anchor= 'nw')
        self.transactions=pd.read_csv('ledger_transactions.csv')
        self.transactions_canvas.create_text(10, 0, text='Transactions', font=('Arial',14), anchor= 'nw')
        self.transactions_canvas.create_text(300, 200, text=[f+'\n' for f in self.transactions].__str__(), font=('Arial',14), anchor= 'nw')
        self.account= pd.read_csv('account.csv')
        # Create a candlestick chart
        fig, ax = plt.subplots(figsize=(10, 6))

        plt.xticks(rotation=45)
       
        self.trade_canvas = tkinter.Canvas( self.trade_tab, relief='groove',background='black')
        self.trade_canvas.place(x=0, y=10, width= 1300, height= 400)
        self.trade_canvas.create_text(10, 310, text='', font=('Arial',14), anchor= 'nw')
        self.chart_tab = tkinter.Frame(self.tab, relief='groove', borderwidth=1 , background='gray')
        self.chart_canvas = tkinter.Canvas(self.chart_tab, width=1500, height = 660,background= 'black', bd= 3)
        self.chart_canvas.place(x=0, y=5)
        self.trade_canvas.place(x=0, y=10)
        figure_canvas = FigureCanvasTkAgg(fig, master=self.chart_canvas)
        figure_canvas.draw()
        figure_canvas.get_tk_widget().place(x=200, y=60)
        ax.xaxis_date()
        ax.autoscale_view()
        ax.set_xlabel('Timestamp')
        ax.set_ylabel('Price')
        fig.autofmt_xdate()
        fig.autofmt_xdate(rotation=45)
        fig.tight_layout()
        fig.subplots_adjust(top=0.95)

        fig.canvas.mpl_connect('scroll_event', self.on_scroll)
       
        plt.xticks(rotation=45)



        plt.tight_layout()


        self.send_money_image_label = tkinter.Label(self.send_money_tab,image= tkinter.PhotoImage(file='images/send_money.png'),width=200, height = 100)
        self.send_money_image_label.place(x=400, y=20, anchor= 'nw')
        self.send_money_label = tkinter.Label(self.send_money_tab, text='Send Money', font=('Arial',14))
        self.send_money_label.place(x=400, y=50, anchor= 'nw',width=20, height= 20)
        self.send_money_address = tkinter.Label(self.send_money_tab, text='Enter Address', font=('Arial',14),height=20, width=200) 
        self.send_money_address.place(x=40, y=30,  anchor= 'nw', height= 20)
        self.send_money_address_entry = tkinter.Entry(self.send_money_tab, width=20 , font=('Arial',14), bg='white', fg='black') 
        self.send_money_address_entry.place(x=50, y=30,  anchor= 'nw',width=20, height= 20)
        self.send_money_amount = tkinter.Label(self.send_money_tab, text='Enter Amount', font=('Arial',14), height=20, width=200                                            )
        self.send_money_amount.place(x=40, y=60,  anchor= 'nw', height= 20) 
        self.send_money_amount_entry = tkinter.Entry(self.send_money_tab, width=20, font=('Arial',14), bg='white', fg='black') 
        self.send_money_amount_entry.place(x=50, y=60, anchor= 'nw',width=20, height= 20)
        self.send_money_asset = tkinter.Label(self.send_money_tab, text='Enter Asset', font =('Arial',14), height=20, width=200) 
        self.send_money_asset.place(x=40, y=90, relwidth=1, relheight=1, anchor= 'nw', height= 20)
        self.send_money_asset_entry = tkinter.Entry(self.send_money_tab, width=20, font=('Arial',14), bg='white', fg='black')
        self.send_money_asset_entry.place(x=50, y=90, relwidth=1, relheight=1, anchor= 'nw',width=20, height= 20)
        self.send_money_button = tkinter.Button(self.send_money_tab, text='Send', font=('Arial',14), command=lambda:self.controller.bot.send_money(
            self.send_money_address_entry.get(),
            self.send_money_amount_entry.get(),
            self.send_money_asset_entry.get()))

        self.receive_money = tkinter.Label(self.send_money_tab, text='Receive Money', font=('Arial',14),image= tkinter.PhotoImage(file='images/receive_money.png'))
        self.receive_money.place(x=200, y=10,  anchor= 'nw',width=1400, height= 20)
        
        
        self.balances_tab = tkinter.Frame(self.tab, relief='groove', borderwidth=1 , background='gray')
        self.balances_canvas = tkinter.Canvas(self.balances_tab, width=1500, height = 660,background= 'black', bd= 3)
        self.balances_canvas.place(x=0, y=0)
    
        self.tab.add(self.trade_tab, text='Server')
        self.tab.add(self.chart_tab, text='Charts')
        self.tab.add(self.order_book_tab, text='OrderBook')
        self.tab.add(self.account_tab, text='Account')
        self.tab.add(self.balances_tab, text='Balances')
        self.tab.add(self.history_tab, text='History')
        self.tab.add(self.transactions_tab, text='Transactions')
        self.tab.add(self.send_money_tab, text='Send Money')
        self.tab.add(self.receive_money_tab, text='Receive Money')
        self.tab.add(self.settings_tab, text='Settings')
        self.tab.add(self.licence_tab, text='Licence')
        self.tab.add(self.about_tab, text='About')
        #self.trade_tree.bind('<<TreeviewSelect>>', self.on_treeview)]
        #Update the GUI
        self.updateMe()
    
    def on_scroll(self, event)->None:
        self.trade_canvas.xview_scroll(int(event.x), 'units')
        self.chart_canvas.xview_scroll(int(event.x), 'units')
    def stop_bot(self)->None:

        self.controller.bot.stop()
        self.toggled_button1.config( background='green',fg='yellow',state='normal',text='START')
        self.toggled_button.config(background='gray',fg='yellow',state='disabled',text='STOP')

    def start_bot(self  )->None:
       self.controller.bot.start()

       self.toggled_button1.config( background='gray',fg='yellow',state='disabled',text='START')
       self.toggled_button.config(background='red',fg='yellow',state='normal',text='STOP')
    
    
    def updateMe(self)->None:
        self.candles = pd.read_csv('candles.csv')#read_sql('SELECT * FROM candles', con=self.controller.bot.db, index_col='timestamp')
        if self.candles['symbol'] is not None:
           self.trade_tree.insert('', 'end', text='timestamp', values=( self.candles['timestamp'].sort_index( ascending=False)))
        trades =pd.read_csv('ledger_trades.csv')
        self.history_canvas.create_text(400, 200, text=str(trades.__str__()), font= ('Arial',14),fill='white' )
        self.trade_tree.delete(*self.trade_tree.get_children()) 
        self.trade_tree.insert('', 'end', text='timestamp', values=(self.candles['timestamp'].sort_index( ascending=False)))
        self.trade_canvas.create_text(150, 10, text= 'Status:', font= ('Arial',14), fill='lightgreen')
        self.trade_canvas.create_text(400, 10, text= self.controller.bot.server_msg['status'], font= ('Arial',14), fill='lightgreen')
        self.trade_canvas.create_text(150, 60, text= 'Type:', font= ('Arial',14), fill='red')
        self.trade_canvas.create_text(400, 60, text= self.controller.bot.server_msg['type'], font= ('Arial',14), fill='white')
        self.trade_canvas.create_text(150, 90, text= 'Message:', font= ('Arial',14), fill='green')
        self.trade_canvas.create_text(500, 90, text= self.controller.bot.server_msg['message'], font= ('Arial',14), fill='white')
        account =self.account 
        self.account_canvas.create_text(300, 10, text= 'Account ID:', font= ('Arial',14), fill='white')
        self.account_canvas.create_text(500, 10, text= account['account_id'].__str__(), font= ('Arial',14), fill='white')
        self.account_canvas.create_text(300, 30, text= 'Balance:', font= ('Arial',14), fill='white')
        self.account_canvas.create_text(500, 30, text= account['balance'].__str__(), font= ('Arial',14), fill='white')
        # self.account_canvas.create_text(300, 170, text= 'asset_code:', font= ('Arial',14), fill='white')
        # self.account_canvas.create_text(500, 170, text= account['asset_code'].__str__(), font= ('Arial',14), fill='white')
        # self.account_canvas.create_text(300, 210, text= 'asset_issuer:', font= ('Arial',14), fill='white')
        # self.account_canvas.create_text(500, 210, text= account['asset_issuer'].__str__(), font= ('Arial',14), fill='white')
        # self.account_canvas.create_text(300, 230, text= 'flags:', font= ('Arial',14), fill='white')
        # self.account_canvas.create_text(500, 230, text= account['flags'], font= ('Arial',14), fill='white')
        # self.account_canvas.create_text(300, 250, text= 'last_modified_ledger:', font= ('Arial',14), fill='white')
        # self.account_canvas.create_text(500, 250, text= account['last_modified_ledger'], font= ('Arial',14), fill='white')        
        self.after(1000, self.updateMe)


        
      
   


  
          
