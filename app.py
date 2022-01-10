from tkinter import *
from tkinter.font import Font
import instaloader
import datetime
import json

class InstaApp:
    def __init__(self, root):
        self.config = json.load(open("config.json"))

        self.root = root
        self.root.title("InstagramBot - Clever Code")
        self.root.geometry("1010x750")
        self.root.resizable(width=False, height=False)
        self.root.config(bg="black")

        self.title_label = Label(self.root, text="Instagram Followers App", bg="black", fg="white", font=self.setFont(25))
        self.title_label.grid(row=0, column=1, pady=20)

        # High Frame
        self.high_frame = Frame(self.root, bg="black")
        self.high_frame.grid(row=1, column=1, pady=20)

        self.account_name_label = Label(self.high_frame, text="Account:", bg="black", fg="white", font=self.setFont(20))
        self.account_name_label.grid(row=0, column=0)

        self.account_name_entry = Entry(self.high_frame, width=20, font=self.setFont(20))
        self.account_name_entry.grid(row=0, column=1)

        # Low Frame
        self.low_frame = Frame(self.root, bg="black")
        self.low_frame.grid(row=2, column=1, pady=20)

        self.make_file_button = Button(self.low_frame, text="Get", bg="white", fg="black", font=self.setFont(20), command=self.makeFileWithFollowers)
        self.make_file_button.grid(row=0, column=0, padx=20)

        self.clear_button = Button(self.low_frame, text="Clear", bg="white", fg="black", font=self.setFont(20), command=self.clear)
        self.clear_button.grid(row=0, column=1, padx=20)

        # Updates Frame
        self.updates_frame = Frame(self.root, bg="black")
        self.updates_frame.grid(row=3, column=1, pady=20)

        self.updates_label = Label(self.updates_frame, text="", bg="black", fg="white", font=self.setFont(25))
        self.updates_label.grid(row=0, column=0)

        # Followers And UnFollowers Labels
        self.followers_label = Label(self.root, text="Lista Followers", bg="black", fg="white", font=self.setFont(20))
        self.followers_label.grid(row=2, column=0, pady=20)

        self.un_followers_label = Label(self.root, text="Lista UnFollowers", bg="black", fg="white", font=self.setFont(20))
        self.un_followers_label.grid(row=2, column=2, pady=20)

        # Followers Listbox
        self.followers_listbox_frame = Frame(self.root, bg="black")
        self.followers_listbox_frame.grid(row=3, column=0, padx=20, pady=20)
        
        self.followers_listbox = Listbox(self.followers_listbox_frame, font=self.setFont(20), width=20, height=20, bg="white", bd=0, fg="black", highlightthickness=0, selectbackground="#a6a6a6", activestyle="none")
        self.followers_listbox.pack(side=LEFT, fill=BOTH)

        self.followers_scrollbar = Scrollbar(self.followers_listbox_frame)
        self.followers_scrollbar.pack(side=RIGHT, fill=BOTH)

        self.followers_listbox.config(yscrollcommand=self.followers_scrollbar.set)
        self.followers_scrollbar.config(command=self.followers_listbox.yview)

        # UnFollowers Listbox
        self.un_followers_listbox_frame = Frame(self.root, bg="black")
        self.un_followers_listbox_frame.grid(row=3, column=2, padx=20, pady=20)

        self.un_followers_listbox = Listbox(self.un_followers_listbox_frame, font=self.setFont(20), width=20, height=20, bg="white", bd=0, fg="black", highlightthickness=0, selectbackground="#a6a6a6", activestyle="none")
        self.un_followers_listbox.pack(side=LEFT, fill=BOTH)

        self.un_followers_scrollbar = Scrollbar(self.un_followers_listbox_frame)
        self.un_followers_scrollbar.pack(side=RIGHT, fill=BOTH)

        self.un_followers_listbox.config(yscrollcommand=self.un_followers_scrollbar.set)
        self.un_followers_scrollbar.config(command=self.un_followers_listbox.yview)

    
    def setFont(self, size):
        return Font(family="Courier New", size=size, weight="bold")
    
    def __searchAccount(self):
        try:
            loader = instaloader.Instaloader()
            loader.login(self.config["my_username"], self.config["my_password"])
            self.profile = instaloader.Profile.from_username(loader.context, self.config["victim_profile"])
            return True
        except:
            return False

    def makeFileWithFollowers(self):
        if self.account_name_entry.get() != "":
            self.config["victim_profile"] = self.account_name_entry.get()
            if self.__searchAccount():
                now = datetime.datetime.now()
                file = open(f"({self.config['victim_profile']}) {now.day}-{now.month}-{now.year}.txt", "a+")
                counter = 0
                for follower in self.profile.get_followers():
                    file.write(follower.username + "\n")
                    self.followers_listbox.insert(END, follower.username)
                    counter += 1
                file.close()
                un_followers = self.__getUnFollowers()
                self.updates_label.config(text=f"Followers Trovati: {counter}\n\nUnFollowers Trovati: {len(un_followers)}")
            else:
                self.updates_label.config(text="Account Instagram Non Trovato!")
        else:
            self.updates_label.config(text="Account Inserito\nNon Valido!")
    
    def __getUnFollowers(self):
        l = []

        try:
            now = datetime.datetime.now()
            first_file = open(f"({self.config['victim_profile']}) {now.day - 1}-{now.month}-{now.year}.txt", "r")
            first_l = first_file.readlines()
        except FileNotFoundError:
            print(f"File Del {now.day - 1}-{now.month}-{now.year} Non Trovato!")
            return l
        
        try:
            now = datetime.datetime.now()
            second_file = open(f"({self.config['victim_profile']}) {now.day}-{now.month}-{now.year}.txt", "r")
            second_l = second_file.readlines()
        except FileNotFoundError:
            print(f"File Del {now.day}-{now.month}-{now.year} Non Trovato!")
            return l
        
        sup, inf = [], []
        if len(first_l) > len(second_l):
            sup = first_l
            inf = second_l
        elif len(first_l) < len(second_l):
            sup = second_l
            inf = first_l
        else:
            sup = first_l # = second_l
            inf = sup
        
        for i in range(0, len(sup)):
            if sup[i] not in inf:
                l.append(sup[i])
        
        if l != []:
            for i in l:
                self.un_followers_listbox.insert(END, i)
        
        return l


    def clear(self):
        self.account_name_entry.delete(0, END)
        self.updates_label.config(text="")
        self.followers_listbox.delete(0, END)
        self.un_followers_listbox.delete(0, END)

root = Tk()
my_gui = InstaApp(root)
root.mainloop()