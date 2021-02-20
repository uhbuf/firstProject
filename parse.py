import sys
import requests
from bs4 import BeautifulSoup
Headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
def get_html(params=None):
    URL = 'https://learnersdictionary.com/definition/%s'%(params)
    r=requests.get(URL,headers=Headers)
    return r
def get_content(html,slovo):
    soup = BeautifulSoup(html, 'html.parser')
    var=1
    results = {}
    temp=[] # для добавления всех определений, этот список потом соеденю в словарь
    provekra=True
    while(provekra==True):
        temp.clear()
        if(var==1):
            items = soup.find('div', {'class': 'entry entry_v2 boxy', 'id': ''})
        elif soup.find('div', {'class':'entry entry_v2 boxy','id':'ld_entry_v2_jumplink_%s_%d'%(slovo,var)}):
            items = soup.find('div', {'class':'entry entry_v2 boxy','id':'ld_entry_v2_jumplink_%s_%d'%(slovo,var)})
        else:
            provekra=False
            break
        chast_rechi=items.find('span', class_='fl').get_text()
        items = items.find('div', class_='sblocks')
        items = items.find_all('span', class_='def_text')
        for item in items:
            temp.append(item.get_text())
        var+=1
        results[chast_rechi]=temp.copy()
    del temp,var,items
    return results
def parse(slovo):
    html=get_html(slovo)
    if html.status_code==200:
        return (get_content(html.text,slovo))
    else:
        return("Error")