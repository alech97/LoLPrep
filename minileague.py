#!/usr/bin/env python

import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from collections import Counter
from tkinter import Tk, Button, Entry, Label, LEFT, RIGHT, font, Frame
from selenium.webdriver.chrome.service import Service as ChromeService
from subprocess import CREATE_NO_WINDOW

from driver import HiddenChromeWebDriver

LINK = 'https://www.metasrc.com/5v5/champion/{}/support?ranks=platinum,diamond,master,grandmaster,challenger'

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

with open(resource_path('champions.txt')) as f:
    champs = f.read().splitlines()

class ChoiceWindow(Tk):
    def __init__(self, width=300, height=100):
        super(ChoiceWindow, self).__init__()

        self.button_font = font.Font(family='calibri', size=15, weight="bold")
        
        self.title("LoL Prep")
        self.minsize(width, height)

        self.button1 = Button(
            self, text="Summoner's Rift", command=self.set_rift, height=4, width=15, 
            bg='#535bfa', fg='white', font=self.button_font, 
            activebackground='#676ae6'
        )
        self.button2 = Button(
            self, text='ARAM', command=self.set_aram, height=4, width=15, 
            bg='#24639f', fg='white', font=self.button_font, 
            activebackground='#2c5c54'
        )

        self.button1.pack(side=LEFT)
        self.button2.pack(side=RIGHT)
    
    def clear(self):
        self.button1.destroy()
        self.button2.destroy()
    
    def set_aram(self):
        self.state = 'aram'
        self.clear()
        self.ask_champion()
    
    def set_rift(self):
        self.state = 'rift'
        self.clear()
        self.ask_champion()
    
    def ask_champion(self):
        frame = Frame(self, bg='purple', height=300, width=100)
        frame.pack(side='top', fill='both', expand=True)
        Label(frame, text='What champion are you playing?', font=self.button_font, fg='black', bg='purple').pack()
        self.champ_entry = Entry(frame, text='champion')
        self.champ_entry.focus()
        self.bind('<Return>', self.swap_to_browser)
        self.champ_entry.pack()
    
    def swap_to_browser(self, *args):
        entry_text = self.champ_entry.get()
        self.destroy()
        open_champ(entry_text)

def open_browser(champ):
    """Opens a given link with a given clean champion stream"""
    mobile_emulation = {
        "deviceMetrics": {
            "width": 500, "height": 700, "pixelRatio": 3.0
        },
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 " +\
            "(KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
    }
    chrome_options = Options()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
    chrome_options.add_argument('log-level=2')
    chrome_options.add_argument("window-size=200,785")

    global browser

    browser = HiddenChromeWebDriver(resource_path('./driver/chromedriver.exe'), options=chrome_options)
    browser.get(LINK.format(champ))

    page_script = """
    document.getElementsByClassName('cc-window').forEach((e) => e.remove());
    document.getElementsByClassName('zaf-sticky-bottom-center').forEach((e) => e.remove());
    $('._yq1p7n').css('background-color', '#00a5bb80');
    $('.container').css('background-color', '#131313');
    $('body').css('background-color', '#131313');

    
    document.getElementById('navbar').remove();
    document.getElementById('leaderboard').remove();
    document.getElementById('metasrc_horizontal_adhesion').remove();

    var content = document.getElementById('content');
    var info = document.getElementById('relation-search').parentElement.parentElement;
    content.innerHTML = '';
    content.appendChild(info);

    var runes = document.evaluate("//h3[contains(., 'Best Runes Reforged')]", document, null, XPathResult.ANY_TYPE, null).iterateNext().parentElement,
        spells = document.evaluate("//h3[contains(., 'Best Summoner Spells')]", document, null, XPathResult.ANY_TYPE, null).iterateNext().parentElement,
        starting_items = document.evaluate("//h3[contains(., 'Starting Items')]", document, null, XPathResult.ANY_TYPE, null).iterateNext().parentElement,
        full_items = document.evaluate("//h3[contains(., 'Best Item Build Order')]", document, null, XPathResult.ANY_TYPE, null).iterateNext().parentElement,
        final_items = document.evaluate("//h3[contains(., 'Best Item Final Build')]", document, null, XPathResult.ANY_TYPE, null).iterateNext().parentElement,
        skills = document.evaluate("//h3[contains(., 'Best Skill Order')]", document, null, XPathResult.ANY_TYPE, null).iterateNext().parentElement;
    
    var div_order = [runes, spells, starting_items, skills, final_items, full_items];

    function removeAllChildNodes(parent) {
        while (parent.firstChild) {
            parent.removeChild(parent.firstChild);
        }
    }

    var container = document.getElementsByClassName('container')[0];
    removeAllChildNodes(container);
    container.append(...div_order);   
    """
    browser.execute_script(page_script)

def choose_champ(query: str):
    """Choose the champion closest to the given input"""
    #Clean query of special characters
    query = ''.join([c.lower() for c in query if c.isalnum()])
    input_ = Counter(query)
    min_diff, min_champ = float('inf'), None

    # For each champion, check which champion name is closest
    for champ in champs:
        counter = Counter(champ)

        #Minus 1 point for each letter within champ name found within the query
        champ_diff = sum((input_ - counter).values())
        #Minus 0.1 points * length of intersecting substrings (to break ties)
        #Ex: "fid" should mean "Fiddlesticks", not "Twisted Fate"
        for a, b in zip(query, champ):
            if a == b:
                champ_diff -= 0.1
            else:
                break

        if champ_diff < min_diff:
            min_diff = champ_diff
            min_champ = champ

    return min_champ

def open_champ(query: str):
    min_champ = choose_champ(query)
    open_browser(min_champ)

def main():
    choice_window = ChoiceWindow()
    choice_window.mainloop()
 
if __name__ == '__main__':
    main()