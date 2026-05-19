from abc import ABC , abstractmethod
from tkinter import *
from tkinter import messagebox
from datetime import date 

class Account(ABC) :
    @abstractmethod
    def deposit(self , amount):
        pass
    @abstractmethod
    def withdraw(self , amount):
        pass

class BankAccount(Account):
    def __init__(self , name , password , balance):
        self.name = name
        self.__password = password
        self.__balance = int(balance)
    def get_password(self):
        return self.__password
    def get_balance(self):
        return self.__balance
    def deposit(self, amount):
        self.__balance += amount
    def withdraw(self, amount):
        if amount > self.__balance :
            return False
        self.__balance -= amount
        return True
    def __str__(self):
        return f'{self.name} {self.__password} {self.__balance}'
    
current_user = None

def load_accounts():
    accounts = []
    try:
        with open('data.txt' , 'r') as f :
            for line in f :
                line = line.strip()
                if line =='':
                    continue
                name , password , balance = line.split()
                accounts.append( BankAccount(name , password , balance ))
    except FileNotFoundError :
        return []
    return accounts

def save_accounts(accounts):
    with open('data.txt' , 'w') as f :
        for acc in accounts :
            f.write( f'{acc.name} {acc.get_password()} {acc.get_balance()} \n')

def login():
    global current_user
    username = login_entry.get().strip()
    password = password_entry.get().strip()
    for acc in accounts :
        if username == acc.name and password == acc.get_password():
            current_user = acc
            
            login_label.pack_forget()
            login_entry.pack_forget()
            login_button.pack_forget()
            password_label.pack_forget()
            password_entry.pack_forget()
            create_button.pack_forget()
            amount_label.config(
                text=f' ACCOUNT BALANCE = {acc.get_balance()}'
            )
            amount_label.pack()
            amount_entry.pack()
            deposit_button.pack()
            withdraw_button.pack()
            transfer_button.pack()
            show_button.pack()
            logout_button.pack()

            return

    messagebox.showinfo('ERROR' , 'USERNAME OR PASSWORD ARE NOT ACCURATE')


def deposit():
    try:
        amount = int(amount_entry.get())
        if amount <= 0 :
            messagebox.showinfo('ERROR' , ' AMOUNT CAN NOT BE NEGATIVE NOR ZERO.')
            return
        current_user.deposit(amount)
        save_accounts(accounts)
        transaction(f'{current_user.name.upper()} DEPOSITED {amount} AT {date.today()} ')
        messagebox.showinfo('STATUS' , 'DEPOSIT SUCCESSFUL!')
        amount_label.config(
            text = f' ACCOUNT BALANCE = {current_user.get_balance()}'
        )
        amount_entry.delete(0,END)

    except:
        messagebox.showinfo('ERROR' , 'ENTER VALID NUMBER')
        amount_entry.delete(0,END)

def withdraw():
    try :
        amount = int(amount_entry.get())
        if amount <= 0 :
            messagebox.showinfo('ERROR' , ' AMOUNT CAN NOT BE NEGATIVE NOR ZERO.')
            return
        result = messagebox.askyesno('CONFIRM WITHDRAW' , ' ARE YOU SURE?')
        if not result :
            amount_entry.delete(0,END)
            return
        success = current_user.withdraw(amount)
        if success :
            save_accounts(accounts)
            transaction(f'{current_user.name.upper()} WITHDREW {amount} AT {date.today()} ')
            messagebox.showinfo('STATUS' , 'WITHDRAW SUCCESSFUL!')
            amount_label.config(
                text = f' ACCOUNT BALANCE = {current_user.get_balance()}'
            )
            amount_entry.delete(0,END)
        else:
            messagebox.showinfo(
                'ERROR',
                'BALANCE NOT ENOUGH'
            )

    except:
        messagebox.showinfo('ERROR' , 'ENTER VALID NUMBER')
        amount_entry.delete(0,END)

def transfer_money():
    amount_label.pack_forget()
    amount_entry.pack_forget()
    deposit_button.pack_forget()
    withdraw_button.pack_forget()
    transfer_button.pack_forget()
    show_button.pack_forget()
    logout_button.pack_forget()
    target_label.pack()
    target_entry.pack()
    transamount_label.pack()
    transamount_entry.pack()
    submittrans_button.pack()
    back_button.pack()


def trans_submit():
    target_name = target_entry.get().strip()
    target_account = None
    for acc in accounts :
        if target_name == acc.name :
            target_account = acc
            break
    if target_account == None :
        messagebox.showinfo('ERROR' , 'ACCOUNT NOT FOUND')
        target_entry.delete(0,END)
        transamount_entry.delete(0,END)
        return
    try :
        amount = int(transamount_entry.get())
    except :
        messagebox.showinfo('ERROR' , 'ENTER VALID NUMBER')
        transamount_entry.delete(0,END)
        return
    if amount <= 0 :
        messagebox.showinfo('ERROR' , ' AMOUNT CAN NOT BE NEGATIVE NOR ZERO.')
        return
    if target_account == current_user :
        messagebox.showinfo('ERROR' , ' CAN NOT TRANSFER TO YOUR OWN ACCOUNT.')
        return

    success = current_user.withdraw(amount)
    if success :
        target_account.deposit(amount)
        save_accounts(accounts)
        transaction(f'{current_user.name.upper()} TRANSFERED {amount} TO {target_account.name.upper()} AT {date.today()}')
        messagebox.showinfo('TRANSFER' , ' TRANSFER SUCCESSFUL!')
        target_entry.delete(0,END)
        transamount_entry.delete(0 ,END)
        amount_label.config(text=f'ACCOUNT BALANCE = {current_user.get_balance()}')
        return
    messagebox.showinfo('ERROR' , ' BALANCE NOT ENOUGH')
def back():
    target_label.pack_forget()
    target_entry.pack_forget()
    transamount_label.pack_forget()
    transamount_entry.pack_forget()
    submittrans_button.pack_forget()
    back_button.pack_forget()
    amount_label.pack()
    amount_entry.pack()
    deposit_button.pack()
    withdraw_button.pack()
    transfer_button.pack()
    show_button.pack()
    logout_button.pack()


def show_history():
    with open('transaction.txt' , 'r') as f :
       lines = f.readlines()
    user_history = []
    for line in lines :
        if line.startswith(current_user.name.upper() + ' '):
            user_history.append(line)
    history_text = ''.join(user_history)
    if not user_history :
        history_text = ' NO TRANSACTIONS YET.'
    messagebox.showinfo('HISTORY' , history_text)
       

def logout():
    global current_user
    current_user = None
    amount_label.pack_forget()
    amount_entry.pack_forget()
    deposit_button.pack_forget()
    withdraw_button.pack_forget()
    transfer_button.pack_forget()
    show_button.pack_forget()
    logout_button.pack_forget()
    login_label.pack()
    login_entry.pack()
    password_label.pack()
    password_entry.pack()
    login_button.pack()
    create_button.pack()
    login_entry.delete(0,END)
    password_entry.delete(0,END)

def create_account():
    login_entry.delete(0,END)
    password_entry.delete(0,END)
    login_label.pack_forget()
    login_entry.pack_forget()
    password_label.pack_forget()
    password_entry.pack_forget()
    login_button.pack_forget()
    create_button.pack_forget()
    create_label.pack()
    create_entry.pack()
    crepass_label.pack()
    crepass_entry.pack()
    balance_label.pack()
    balance_entry.pack()
    submitcreate_button.pack()
    createback_button.pack()

def submit():
    username = create_entry.get().strip()
    password = crepass_entry.get()
    try:
        balance = int(balance_entry.get())
    except :
        messagebox.showinfo("ERROR" , 'ENTER VALID NUMBER .')
        return
    for acc in accounts :
        if username == acc.name :
            messagebox.showinfo("ERROR" , 'ACCOUNT ALREADY EXISTS.')
            return
    accounts.append(BankAccount(username , password , balance))
    save_accounts(accounts)
    messagebox.showinfo("STATUS" , 'ACCOUNT CREATED SUCCESSFULY.')
    create_entry.delete(0,END)
    crepass_entry.delete(0,END)
    balance_entry.delete(0,END)
    create_label.pack_forget()
    create_entry.pack_forget()
    crepass_label.pack_forget()
    crepass_entry.pack_forget()
    balance_label.pack_forget()
    balance_entry.pack_forget()
    submitcreate_button.pack_forget()
    createback_button.pack_forget()
    login_label.pack()
    login_entry.pack()
    password_label.pack()
    password_entry.pack()
    login_button.pack()
    create_button.pack()

def create_back():
    create_label.pack_forget()
    create_entry.pack_forget()
    crepass_label.pack_forget()
    crepass_entry.pack_forget()
    balance_label.pack_forget()
    balance_entry.pack_forget()
    submitcreate_button.pack_forget()
    createback_button.pack_forget()
    login_label.pack()
    login_entry.pack()
    password_label.pack()
    password_entry.pack()
    login_button.pack()
    create_button.pack()

def transaction(text):
    with open ('transaction.txt' , 'a' ) as f :
        f.write(text + '\n' )

accounts = load_accounts()
window = Tk()
window.title("ATM SYSTEM")
window.attributes('-fullscreen' , True)
window.bind( '<Escape>' ,
            lambda event : window.attributes('-fullscreen' , False)
            )

login_label = Label(
    window ,
    text= " ENTER YOUR USERNAME :" ,
    font=('arial' , 50 )
)
login_entry = Entry( 
    window , 
    font = ('arial' , 50 )
)
login_button = Button( 
    window , 
    command= login , 
    text = 'LOGIN' ,
    font=('arial' , 50 )
)
login_label.pack()
login_entry.pack()

password_label = Label(
    window ,
    text= " ENTER YOUR PASSWORD :" ,
    font=('arial' , 50 ))

password_entry = Entry( 
    window , 
    font = ('arial' , 50 ) , 
    show='*'
)
password_label.pack()
password_entry.pack()
login_button.pack()
create_button = Button(
    window , 
    text= ' CREATE ACCOUNT ' , 
    command= create_account , 
    font=('arial' , 50 )
)
create_button.pack()

# after logged in 
amount_label = Label( 
    window , 
    text= ' AMOUNT : ' , 
    font=('arial' , 50 )
)
amount_entry = Entry(
    window ,
    font=('arial' , 50 )
)
deposit_button = Button(
    window , 
    text= ' DEPOSIT ' , 
    command= deposit , 
    font=('arial' , 50 )
)
withdraw_button = Button(
    window , 
    text= ' WITHDRAW ' , 
    command= withdraw , 
    font=('arial' , 50 )
)
logout_button = Button(
    window , 
    text= ' LOGOUT ' , 
    command= logout , 
    font=('arial' , 50 )
)
transfer_button = Button(
    window , 
    text= ' TRANSFER MONEY  ' , 
    command= transfer_money , 
    font=('arial' , 50 )
)
show_button = Button(
    window , 
    text= ' SHOW HISTORY ' , 
    command= show_history , 
    font=('arial' , 50 )
)

target_label= Label(
    window , 
    text= ' TARGETED ACCOUNT : ' , 
    font=('arial' , 50 )
)
target_entry = Entry(
    window , 
    font=('arial' , 50 )
)
transamount_label = Label(
    window , 
    text= ' AMOUNT : ' , 
    font=('arial' , 50 )
    )
transamount_entry = Entry(
    window , 
    font=('arial' , 50 )
)
submittrans_button = Button(
    window , 
    text= ' SUBMIT TRANSFER ' , 
    command= trans_submit , 
    font=('arial' , 50 )
)
back_button = Button(
    window , 
    text= ' BACK' , 
    command= back , 
    font=('arial' , 50 ) 
)
create_label = Label(
    window , 
    text= ' USERNAME :' ,
    font= ('arial' , 50 )
)
create_entry = Entry(
    window ,
    font= ('arial' , 50 )
)
crepass_label = Label(
    window , 
    text= ' PASSWORD' ,
    font= ('arial' , 50 )
    )
crepass_entry = Entry(
    window ,
    font= ('arial' , 50 ) , 
    show = '*'
    )
submitcreate_button = Button(
    window , 
    text = "CREATE" , 
    command= submit , 
    font=('arial',50)
)
balance_label = Label(
    window , 
    text= ' BALANCE ' ,
    font= ('arial' , 50 )
)
balance_entry = Entry(
    window , 
    font= ('arial' , 50 )
)
createback_button = Button(
    window , 
    text = "BACK" , 
    command= create_back , 
    font=('arial',50)
)






window.mainloop()