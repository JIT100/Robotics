from RPA.Browser.Selenium import Selenium
from selenium.webdriver.common.by import By
import time
import re
from termcolor import colored, cprint
import random

br = Selenium()

class Robot:
    def __init__(self, name):
        self.name = name

    def say_hello(self):
        # Randomm greetings msgs
        greetings = [
            f"Hello there! I'm {self.name}, your friendly software robot.",
            f"Hi! It's {self.name}, your trusty companion on the quest for knowledge.",
            f"Welcome! I'm {self.name}, ready to help you explore the world of science."
        ]
        greeting = random.choice(greetings)
        print(colored(greeting, 'blue'))
        print()

    def say_goodbye(self):
        # Randomm goodbye msgs
        goodbye_messages = [
            f"Farewell, my friend! It was a pleasure assisting you as {self.name}.",
            f"Until we meet again! Remember, {self.name} is always here to help.",
            f"Goodbye for now! Stay curious and keep exploring with {self.name}.",
            f"Take care! {self.name} wishes you continued success in your endeavors."
        ]
        goodbye_message = random.choice(goodbye_messages)
        print()
        print(colored(goodbye_message, 'magenta'))
    
    def display_description(self,data):
        description = f"I am an intelligent software robot."
        print(colored(description, 'cyan'))
        self.display_instructions(data)

    def display_instructions(self,data):
        instructions = [
            "I am here to assist you in finding key information about important scientists.",
            f"Today, I will show case {len(data)} scientists.",
            "First, I will navigate to their Wikipedia pages and retrieve birth and death dates,",
            "as well as the first paragraph of their Wikipedia biography.",
            "Let's get started, Shall We !! "
        ]

        for instruction in instructions:
            print()
            print(colored(f"{instruction}", 'white'))
            time.sleep(1)
        print()

    # Opens & maximize the browser
    def open_webpage(self, webpage):
        br.open_available_browser(webpage)
        br.maximize_browser_window()

    def calculate_age(self,born,died): 
        age=int(died[:4])-int(born[:4])-((int(died[5:7]),int(died[-2:]))<(int(born[5:7]),int(born[-2:])))
        return age


    # Fetch the data from website
    def fetch_data(self,item,data):
        table_rows = br.find_elements("xpath://div[@id='mw-content-text']//table//tr")

        # Iterate through the table rows and search for the "died" text
        for index, row in enumerate(table_rows):
            if "Died" in row.text:
                died_index= index + 1
        died=br.driver.find_element(By.XPATH,f'//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[{died_index}]/td/span').get_attribute("innerText")
        died=re.sub("[()]","",died)
        # Fetching Born date 
        born=br.driver.find_element(By.XPATH,"//span[@class='bday']").get_attribute("innerText")
        
        # Iterate through Paragraph
        br.wait_until_page_contains_element('//*[@id="mw-content-text"]/div[1]/p[2]')
        paragraph=br.get_text('//*[@id="mw-content-text"]/div[1]/p[2]')
        for i in range (3,6):
            if len(paragraph) > 10:
                first_paragraph=paragraph
                break
            elif len(paragraph) < 10:
                paragraph= br.get_text(f'//*[@id="mw-content-text"]/div[1]/p[{i}]')
        first_paragraph=re.sub("([\(\[]).*?([\)\]])", "", first_paragraph)

        # Calculating Age
        age = self.calculate_age(born,died)
        
        data[item]=[item,born,died,age,first_paragraph]
        
        return data
              
    def search(self,item,count,data):
        try:
            if count == 1:
                br.input_text('xpath://*[@id="searchInput"]',item,clear=True)
                br.click_button('//*[@id="search-form"]/fieldset/button')
                self.fetch_data(item,data)
            elif count >1:
                br.input_text('name:search',item,clear=True)
                br.wait_until_page_contains_element("class:cdx-button")
                br.click_button('class:cdx-button')
                self.fetch_data(item,data)
        except Exception as e:
             print(f"An error occurred: {str(e)}")


    def show_data(self,dict):
        for item in dict:
            print('\nScientist Name:',colored(dict[item][0],'cyan',attrs=['bold']))
            print(colored('------------------------------------------', 'light_cyan'))
            print('\nBorn Date:',colored(dict[item][1],'light_blue'))
            print('\nDeath Date:',colored(dict[item][2],'light_blue'))
            print('\nAge :',colored(dict[item][3],'magenta'))
            print('\nFirst Paragraph:')
            cprint(dict[item][4],'yellow')
            time.sleep(1)

    def run(self,website,items):
        data={}
        count=0
        print(colored('\nFetching the details of all the scietists, Hang Tight ......... ', 'red',attrs=['dark','blink']))
        self.open_webpage(website)
        print()
        print(colored('----□----□----□----□----□----□----□----□----□----□---□----□----□----□----□----□----□----□----□----□----□----□----□----□----□----□----□----□----□---□----□----□----□----□----', 'light_cyan'))
        for item in items:
            count+=1
            self.search(item,count,data)
        br.close_all_browsers()
        self.show_data(data)
        time.sleep(1)
        print()
        print(colored('----□----□----□----□----□----□----□----□----□----□---□----□----□----□----□----□----□----□----□----□----□----□----□----□----□----□----□----□----□---□----□----□----□----□----', 'light_cyan'))
        time.sleep(1)