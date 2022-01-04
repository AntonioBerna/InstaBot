import instaloader
import datetime
import json
import time
import sys

class Instagram:
    def __init__(self, victim_profile):
        self.config = json.load(open("config.json"))
        self.config["victim_profile"] = victim_profile

    def __searchAccount(self):
        print("Ricerca account in corso...")
        try:
            loader = instaloader.Instaloader()
            loader.login(self.config["my_username"], self.config["my_password"])
            self.profile = instaloader.Profile.from_username(loader.context, self.config["victim_profile"])
            print("Account Instagram Trovato!")
            return True
        except:
            print("Account Instagram Non Trovato!")
            return False

    def makeFileWithFollowers(self):
        if self.__searchAccount():
            now = datetime.datetime.now()
            file = open(f"({self.config['victim_profile']}) {now.day}-{now.month}-{now.year}.txt", "a+")
            for follower in self.profile.get_followers():
                file.write(follower.username + "\n")
            file.close()
            print("File Salvato!")
    
    def getFollowers(self):
        count = 0
        for follower in self.profile.get_followers():
            count += 1
            print(f"({count}) {follower.username}")
            time.sleep(0.125)


if len(sys.argv) < 2:
    print("ATTENZIONE! Bisogna passare il nome di un account Instagram come parametro!")
    sys.exit()

account = Instagram(sys.argv[1])
account.makeFileWithFollowers()
account.getFollowers()