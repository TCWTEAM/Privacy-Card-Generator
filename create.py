import requests
from bs4 import BeautifulSoup as bs
from random import *
import random
import json
import string
import os
from utils import c_logging, n_logging
import time

with open("config.json") as file:
    config = json.load(file)
    file.close()

os.remove("cards.txt")
f = open("cards.txt", "w+")
f.close()

def main():
    loggedin = False
    s = requests.session()

    num = config['numtocreate']
    email = config['email']
    passw = config['password']
    limit = config['limit']
    cname = config['cardname']

    headers = {
        'Accept':'application/json, text/plain, */*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'en-US,en;q=0.9',
        'Connection':'keep-alive',
        'Content-Type':'application/json;charset=UTF-8',
        'Host':'privacy.com',
        'Origin':'https://privacy.com',
        'Referer':'https://privacy.com/login',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
    }

    b = s.post("https://privacy.com/login", headers=headers)
    cookies = s.cookies.get_dict()
    sessionid = cookies["sessionID"]
    headers["Cookie"] = 'sessionID={}; abtests=%5B%7B%22name%22%3A%22extension-install-test%22%2C%22value%22%3A%22signup-step%22%7D%5D; landing_page=main'.format(sessionid)

    payload1 = {
        'email': email,
        'extensionInstalled': 'false',
        'password': passw,
    }
    c_logging("Logging in this may take a while...", "yellow")
    a = s.post("https://privacy.com/auth/local", data=json.dumps(payload1), headers=headers)
    if a.status_code == 200:
        c_logging("Logged In to {}:{} !".format(email, passw), "green")
        c_logging("Removing Credentials From Variables", "magenta")
        email = ""
        passw = ""
        loggedin = True
        response = a.json()
        token = response["token"]
        headers["Authorization"] = 'Bearer ' + token
        headers["Cookie"] = 'sessionID={}; abtests=%5B%7B%22name%22%3A%22extension-install-test%22%2C%22value%22%3A%22signup-step%22%7D%5D; landing_page=main; ETag="ps26i5unssI="; token={}'.format(sessionid, token)
    else:
        c_logging("ERROR LOGGING IN {}".format(str(a.text)), "red")
        print(a.text)


    if loggedin == False:
        exit()

    for i in range(int(num)):
        time.sleep(3)
        url = "https://privacy.com/api/v1/card"
        cnum = randint(0, 30000)
        name = cname + str(cnum)

        payload2 = {
            "CVV": "XXX",
            "expMonth": "XX",
            "expYear": "XXXX",
            "hostname": "null",
            "memo": name,
            "panWithSpaces": "XXXX XXXX XXXX XXXX",
            "reloadable": "true",
            "spendLimit": int(limit),
            "spendLimitDuration": "MONTHLY",
            "style": "null"
        }

        r = s.post(url, data=json.dumps(payload2), headers=headers)

        if r.status_code == 200:
            n_logging("#########################")
            card = r.json()
            number = card["card"]["pan"]
            expdate = card["card"]["expMonth"] + "/" + card["card"]["expYear"]
            cvv = card["card"]["cvv"]
            f = open("cards.txt", "a+")
            f.write("{} | {} | {}\n".format(number, expdate, cvv))
            f.close()
            c_logging("Created Card", "green")
            print(number)
            print(expdate)
            print(cvv)
            n_logging("#########################")
            print("")
        else:
            n_logging("#########################")
            c_logging("ERROR CREATING CARD", "red")
            print(r.text)
            print(r.status_code)
            n_logging("#########################")
            print("")
    print("")
    c_logging("Finished Creating Cards!", "cyan")
    c_logging("Cards Made Were Saved To cards.txt", "magenta")
    c_logging("XO", "cyan")

if __name__ == '__main__':
    c_logging("Privacy Card Gen", "cyan")
    c_logging("By XO", "yellow")
    print("")
    c_logging("Starting...", "magenta")
    main()
