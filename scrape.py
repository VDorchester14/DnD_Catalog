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
    aci2 = text[aci:].find(')')
    ac = text[aci+12:aci+aci2+1]

    # this gets the hit points
    hpi = text.find("Hit Points") # find hit points
    hpi2 = text[hpi:].find(')') # find where the line ends
    hp = text[hpi+11:(hpi2+hpi+1)] # get the text

    # this gets the saving throws
    sti = text.find("Saving Throws") # find the saving throws
    sti2 = text[sti:].find("\n")
    st = text[sti+14:sti+sti2+1]

    #this gets speed
    spi = text.find("Speed")
    spi2 = text[spi:].find("\n")
    sp = text[spi+6:spi+spi2]
    print(sp)
 
    # damage immunities
    dmgi = text.find("Damage Immunities")
    dmgi2 = text[dmgi:].find("\n")+dmgi
    dmg = text[dmgi+18:dmgi2]
    print(dmg)

    # Condition immunities
    coni = text.find("Condition Immunities")
    coni2 = text[coni:].find("\n")+coni
    con = text[coni+21:coni2]
    print(con)

    # Senses
    sensei = text.find("Senses")
    sensei2 = text[sensei:].find("\n")+sensei
    senses = text[sensei+len("senses "):sensei2]
    print(senses)
    
    # Challenge
    cri = text.find("Challenge")
    cri2 = text[cri:].find("\n")+cri
    cr = text[cri+len("Challenge "):cri2]
    print(cr)

    # Skills 
    ski = text.find("Skills")
    ski2 = text[ski:].find("\n")+ski
    if(ski > 0):
        skills = text[ski+len("skills "):ski2]
        print(skills)

    # Languages 
    lai = text.find("Languages")
    lai2 = text[lai:].find("\n")+lai
    if lai>0:
        languages = text[lai+len("languages "):lai2]
        print(languages)


    # now get the attacks
    att = soup.select("a", {"class":"attack"})
    attacks = [a.text for a in att]
    # currently there are some duplicate attacks  add a line
    # here to fix it.
    for a in attacks:
        print(a)

    # stats
    stats = soup.select("td")
    print(stats)

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
