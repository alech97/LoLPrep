#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from collections import Counter

link = 'https://www.metasrc.com/5v5/champion/{}/support?ranks=platinum,diamond,master,grandmaster,challenger'

mobile_emulation = {
    "deviceMetrics": {"width": 500, "height": 700, "pixelRatio": 3.0},
    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"}
chrome_options = Options()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
chrome_options.add_argument("window-size=200,850")

champs = [
    "aatrox",
    "ahri",
    "akali",
    "alistar",
    "amumu",
    "anivia",
    "annie",
    "aphelios",
    "ashe",
    "aurelionsol",
    "azir",
    "bard",
    "blitzcrank",
    "brand",
    "braum",
    "caitlyn",
    "camille",
    "cassiopeia",
    "chogath",
    "corki",
    "darius",
    "diana",
    "drmundo",
    "draven",
    "ekko",
    "elise",
    "evelynn",
    "ezreal",
    "fiddlesticks",
    "fiora",
    "fizz",
    "galio",
    "gangplank",
    "garen",
    "gnar",
    "gragas",
    "graves",
    "hecarim",
    "heimerdinger",
    "illaoi",
    "irelia",
    "ivern",
    "janna",
    "jarvaniv",
    "jax",
    "jayce",
    "jhin",
    "jinx",
    "kaisa",
    "kalista",
    "karma",
    "karthus",
    "kassadin",
    "katarina",
    "kayle",
    "kayn",
    "kennen",
    "khazix",
    "kindred",
    "kled",
    "kogmaw",
    "leblanc",
    "leesin",
    "leona",
    "lillia",
    "lissandra",
    "lucian",
    "lulu",
    "lux",
    "malphite",
    "malzahar",
    "maokai",
    "masteryi",
    "missfortune",
    "mordekaiser",
    "morgana",
    "nami",
    "nasus",
    "nautilus",
    "neeko",
    "nidalee",
    "nocturne",
    "nunuwillump",
    "olaf",
    "orianna",
    "ornn",
    "pantheon",
    "poppy",
    "pyke",
    "qiyana",
    "quinn",
    "rakan",
    "rammus",
    "reksai",
    "renekton",
    "rengar",
    "riven",
    "rumble",
    "ryze",
    "samira",
    "sejuani",
    "senna",
    "seraphine",
    "sett",
    "shaco",
    "shen",
    "shyvana",
    "singed",
    "sion",
    "sivir",
    "skarner",
    "sona",
    "soraka",
    "swain",
    "sylas",
    "syndra",
    "tahmkench",
    "talon",
    "taric",
    "teemo",
    "thresh",
    "tristana",
    "trundle",
    "tryndamere",
    "twistedfate",
    "twitch",
    "udyr",
    "urgot",
    "varus",
    "vayne",
    "veigar",
    "velkoz",
    "vi",
    "viktor",
    "vladimir",
    "volibear",
    "warwick",
    "wukong",
    "xayah",
    "xerath",
    "xinzhao",
    "yasuo",
    "yone",
    "yorick",
    "yuumi",
    "zac",
    "zed",
    "ziggs",
    "zilean",
    "zoe",
    "zyra"
]

def open_browser(champ):
    """Opens a given link with a given clean champion stream"""
    global browser
    browser = webdriver.Chrome('./chromedriver', options=chrome_options)
    # browser.set_window_size(200, 850)
    browser.get(link.format(champ))

    page_script = """
    document.getElementsByClassName('cc-window').forEach((e) => e.remove());
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


def clean_str(s: str):
    """Clean a given string to be lowercase and without special characters"""
    return ''.join([c.lower() for c in s if c.isalnum()])


def choose_champ(query: str):
    """Choose the champion closest to the given input"""
    input_ = Counter(query)
    min_diff, min_champ = float('inf'), None

    # For each champion, check which champion name is closest
    for champ in champs:
        counter = Counter(champ)

        champ_diff = sum((input_ - counter).values())

        if champ_diff < min_diff:
            min_diff = champ_diff
            min_champ = champ
        elif champ_diff == min_diff and query in champ:
            min_diff = champ_diff
            min_champ = champ

    return min_champ


def main():
    input_ = clean_str(input("What champion are you playing? <3\n"))

    min_champ = choose_champ(input_)

    open_browser(min_champ)


if __name__ == '__main__':
    main()
