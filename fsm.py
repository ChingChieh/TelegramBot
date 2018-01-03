from transitions.extensions import GraphMachine
import types
import requests
import re
from bs4 import BeautifulSoup

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    def is_going_to_state1(self, update):
        text = update.message.text
        return text.lower() == 'nba news'

    def is_going_to_state2(self, update):
        text = update.message.text
        return text.isdigit()
        #return text.lower() == 'go to state2'
    
    def is_going_to_move(self, update):
        text = update.message.text
        return text == '助攻' or text == '運球' or text == '動作' or text == '抄截' or text == '火鍋' or text == '灌籃'

    def is_going_to_leader(self, update):
        text = update.message.text
        return text == '最佳數據'
    
    def is_going_to_help(self, update):
        text = update.message.text
        return text.lower() == 'help'

    def on_enter_state1(self, update):
        #update.message.reply_text("I'm entering state1")
        response = requests.get("https://nba.udn.com/nba/index?gr=www#/")
        soup = BeautifulSoup(response.text,"lxml")
        nba_news = [tag.text for tag in soup.find_all("div",{"class":"only_mobile focus_mobile"})]
        string = ""
        i = 1
        for line in nba_news:
            if(line != " "):
                line = str(i)+' '+line
                string = string + line + "\n"                
            i+=1
        update.message.reply_text(string)    
        self.go_back(update)

    def on_exit_state1(self, update):
        print('Leaving state1')

    def on_enter_state2(self, update):
        text = update.message.text
        number = int(text)
        #update.message.reply_text("I'm entering state2")
        if(number > 10 or number < 1):
            update.message.reply_text("wrong input")
            self.go_back(update)
            return
        
        response = requests.get("https://nba.udn.com/nba/index?gr=www#/")
        soup = BeautifulSoup(response.text,"lxml")
        nba_news = [tag.text for tag in soup.find_all("div",{"class":"only_mobile focus_mobile"})]
        array = []
        i = 1
        for line in nba_news:
            if(line == " "):
                array.append(i)
            i+=1
        print(array)
        check = 1;
        
        for num in array:
            if(number == num):
                update.message.reply_text("wrong input")
                self.go_back(update)
                return

        for k in range(0,10):
            if(k == (number - 1)):
                update.message.reply_text(soup.find_all("div",{"class":"only_mobile focus_mobile"})[k].find("a")["href"])   
        self.go_back(update)

    def on_exit_state2(self, update):
        print('Leaving state2')

    def on_enter_move(self, update):
        text = update.message.text
        if(text == '火鍋'):
            text = '阻攻'
        #update.message.reply_text("I'm entering state1")
        response = requests.get("https://nba.udn.com/nba/index?gr=www#/")
        soup = BeautifulSoup(response.text,"lxml")
        nba_move = [tag.text for tag in soup.find_all("a",{"class":"youtube"})]
        j = -1
        for line in nba_move:
            n = line.find(text)
            j += 1
            if(n == 4 and line[0] == '今'):
                string = line + "\n" + soup.find_all("a",{"class":"youtube"})[j]["href"]
                update.message.reply_text(string)
                self.go_back(update)
                return
            
        update.message.reply_text("can't find")  
        self.go_back(update)
    
    def on_exit_move(self, update):
        print('Leaving move')

    def on_enter_leader(self, update):
        #update.message.reply_text("I'm entering state1")
        r = requests.get("https://www.cbssports.com/nba/stats/leaders/live")
        s = BeautifulSoup(r.text,"lxml")
        
        #print(s.find_all("td")[13].text)
        
        name1 = s.find_all("td",{"align":"left"})[0].text
        name2 = s.find_all("td",{"align":"left"})[10].text
        name3 = s.find_all("td",{"align":"left"})[20].text
        n1 = name1.find(",")
        n2 = name2.find(",")
        n3 = name3.find(",")
        name1 = '得分王' + '\n' + name1[3:n1] + ' ' + s.find_all("td")[13].text + '分'
        name2 = '籃板癡漢' + '\n' + name2[3:n2] + ' ' + s.find_all("td")[113].text + '籃板'
        name3 = '最無私' + '\n' + name3[3:n3] + ' ' + s.find_all("td")[213].text + '助攻'

        name = name1 + '\n' + name2 + '\n' + name3
        update.message.reply_text(name)    
        self.go_back(update)

    def on_exit_leader(self, update):
        print('Leaving leader')

    def on_enter_help(self, update):
        string = '關鍵字:' + '\n' 
        string = string + '1. nba news(不分大小寫) 可查詢NBA及時新聞' + '\n' + '\n' 
        string = string + '2. 可輸入NBA新聞的號碼得到該新聞網址' + '\n' + '\n'
        string = string + '3. 灌籃、助攻、火鍋、動作、運球、抄截可看當日最佳指定動作' + '\n' + '\n'
        string = string + '4. 最佳數據可看當日得分王、籃板王、助攻王' 
        update.message.reply_text(string)        
        self.go_back(update)

    def on_exit_help(self, update):
        print('Leaving help')


    
