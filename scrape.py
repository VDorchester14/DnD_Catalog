from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

# this function will get the links to every monster
# returns dataframe with name and url and key
def get_df():
    # set the url
    url = "https://jsigvard.com/dnd/Monsters.html"
    request = requests.get(url) # send a request
    content = request.content # get the content
    soup = BeautifulSoup(content, "html.parser") # parse it

    # gets the links associated with each entry
    monsters = soup.select("a:link")
    links = {}
    for link in monsters:
        sub_link = re.findall(r'"(.*?)"', str(link))[0]
        name = re.findall(r'>(.*?)<', str(link))[0]
        sub_link = sub_link.replace(" ", "%20")
        links[name] = sub_link

    # now put it in a dataframe
    names = links.keys()
    urls = links.values()
    df = pd.DataFrame(list(zip(names, urls)), columns = ['name','url'])
    return df

# creates the full links
def create_links(base, extensions):
    links = []
    for li in extensions:
        links.append(base+li)
    return links

def get_monster_data(url):
    request = requests.get(url) # send a request
    content = request.content # get the content
    soup = BeautifulSoup(content, "html.parser") # parse it

    # get the name
    name = str(soup.select("h2"))[8:-10]

    # get all the text
    text = soup.get_text()

    # this gets the armor class
    aci = text.find("Armor Class")
    aci2 = text[aci:].find('\n')+aci
    armor_class = text[aci+len("Armor Class "):aci2]

    # this gets the hit points
    hpi = text.find("Hit Points") # find hit points
    hpi2 = text[hpi:].find('\n')+hpi # find where the line ends
    hit_points = text[hpi+len("Hit Points "):hpi2] # get the text

    # this gets the saving throws
    sti = text.find("Saving Throws") # find the saving throws
    sti2 = text[sti:].find("\n")+sti
    saving_throws = text[sti+len("Saving Throws "):sti2]

    #this gets speed
    spi = text.find("Speed")
    spi2 = text[spi:].find("\n")+spi
    speed = text[spi:spi2]

    # damage immunities
    dmgi = text.find("Damage Immunities")
    dmgi2 = text[dmgi:].find("\n")+dmgi
    dmg_immunities = text[dmgi+len("Damage Immunities "):dmgi2]

    # languages
    lai = text.find("Languages")
    if(lai>0):
        lai2 = text[lai:].find("\n")+lai
        languages = text[lai+len("Languages "):lai2]
    else:
        languages = "None"

    # skills
    ski = text.find("Skills")
    ski2 = text[ski:].find("\n")+ski
    skills = text[ski+len("Skills "):ski2]

    # senses
    sei = text.find("Senses")
    sei2 = text[sei:].find("\n")+sei
    senses = text[sei+len("senses "):sei2]

    # challenge
    chi = text.find("Challenge")
    chi2 = text[chi:].find("\n")+chi
    challenge = text[chi+len("challenge "):chi2]

    print(armor_class, hit_points, saving_throws, speed, dmg_immunities, languages, skills, senses, challenge)

    return

def main():
    base_link = 'https://jsigvard.com/dnd/' # add the links to this to get data

    #monsters = get_df() # get the monster dataframe

    #links = create_links(base_link, list(monsters.url)) # get the full urls
    #monsters['full_url'] = links # add to dataframe
    #monsters.to_pickle('df.pkl')
    monsters = pd.read_pickle("df.pkl")
    url = monsters.iloc[0].full_url
    get_monster_data(url)


if __name__=="__main__":main()
