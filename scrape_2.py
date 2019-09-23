from bs4 import BeautifulSoup
import requests
import re
from collections import OrderedDict
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

def get_monster_data(df):

    # these are the attributes I want to get
    info = ["Armor Class", "Hit Points", "Saving Throws", "Speed",
    "Damage Immunities","Languages","Skills","Senses","Challenge"]

    # make the column names
    columns = ['name']
    for c in info:
        columns.append(c.lower())

    columns.append("strength")
    columns.append("dexterity")
    columns.append("constitution")
    columns.append("intelligence")
    columns.append("wisdom")
    columns.append("charisma")
    columns.append("actions")

    df2 = pd.DataFrame(columns=columns)

    # this will be done on each monster
    for index, row in df.iterrows():
        url = df.iloc[index].full_url
        # getting the page data
        request = requests.get(url) # send a request
        content = request.content # get the content
        soup = BeautifulSoup(content, "html.parser") # parse it

        # get the name
        name = str(soup.select("h2"))[8:-10]

        # get all the text
        text = soup.get_text()

        data = [name] # this will store all of the data for a monster
        for attribute in info: # iterate over each attribute to get
            start = text.find(attribute) # the beginning of where the data is
            if (start > 0): # if it exists
                end = text[start:].find("\n")+start # find the end of the line
                data.append(text[start+len(attribute)+1:end]) # pull the data
            else: # if the data cannot be found
                data.append("None") # just put None

        # now I will get the table with its base stats
        # stats in order are STR DEX CON INT WIS CHA
        base_data = soup.select("td") # get the stat table
        for b in base_data[6:]: # iterate over the numbers
            b = str(b) # convert to string
            i = b.find(">")+1 # find the start
            j = b[i:].find("<")+i # find where the data finishes
            stat = b[i:j] # extract it
            data.append(stat) # add it to the list

        # now I will get the attacks
        acts = soup.select("a", {"class":"attack"})
        acts_unique = [] # to remove duplicate
        for i in acts: # iterate through the list
            #print("Action!!!")
            j = i.text.splitlines() # split any multi line actions
            for k in j: # go through those
                #print("Line of butts")
                acts_unique.append(k) # add them to the unique list
        acts_unique = list(OrderedDict.fromkeys(acts_unique)) # remove duplicates

        # now remove the source
        actions = acts_unique[:-1] # this removes the line with the source
        data.append(actions) # add the actions to the list

        # add to dataframe and shift index
        try:
            df2.loc[-1] = data
            df2.index += 1
        except:
            print(data)
            print(len(data))
            print(len(columns))
            print(url)

    df3 = pd.merge(df, df2, on="name")
    df3.reset_index()

    return df3

def main():
    base_link = 'https://jsigvard.com/dnd/' # add the links to this to get data

    #monsters = get_df() # get the monster dataframe

    #links = create_links(base_link, list(monsters.url)) # get the full urls
    #monsters['full_url'] = links # add to dataframe
    #monsters.to_pickle('df.pkl')
    #monsters = pd.read_pickle("df.pkl")
    #url = monsters.iloc[0].full_url
    #monsters = get_monster_data(monsters)
    monsters.to_pickle("monsters.pkl")
    print(monsters.head(3))


if __name__=="__main__":main()
