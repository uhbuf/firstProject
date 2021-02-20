import sys
import requests
from bs4 import BeautifulSoup
Headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
def get_html(params=None):
    URL = 'https://wooordhunt.ru/word/%s'%(params)
    r=requests.get(URL,headers=Headers)
    return r
def get_content(html,slovo):
    results={}
    kolvoPrimerov=0
    schet=0
    temp=[]
    soup = BeautifulSoup(html, 'html.parser')
    items=soup.find('div',id='wd')
    if(items.find('div',id='word_forms')):
        prosto_nushno=items.find_all('div',id='word_forms')
        for i in prosto_nushno:
            temp.append(i.get_text())
        results['dopolnenie']=temp.copy()
    temp.clear()
    perevod=items.find('div',class_='t_inline_en')
    if(perevod):
        results['perevod'] = perevod.get_text()
        trans=items.find('span',class_='transcription')
        results['transcription']=trans.get_text()
        example_en=items.find_all('p',class_='ex_o')
        example_ru=items.find_all('p',class_='ex_t human')
        temp=[]
        for i in example_ru:
            kolvoPrimerov+=1
            temp.append(i.get_text())
        results['kolvo']=kolvoPrimerov
        results['example_ru']=temp.copy()
        temp.clear()
        for i in example_en:
            if(schet!=kolvoPrimerov):
                temp.append(i.get_text())
            else: break
        results['example_en']=temp.copy()
        temp.clear()
        return results
    else: return 0
def parseSlovar(slovo):
    html=get_html(slovo)
    if html.status_code==200:
        return (get_content(html.text,slovo))
    else:
        return("Error")
