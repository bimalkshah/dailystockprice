from flask import Blueprint
import requests
from bs4 import BeautifulSoup
import pandas as pd

views=Blueprint('views',__name__)

@views.route('/')
def home():
    page=requests.get("https://www.sharesansar.com/today-share-price")
    src=page.content
    soup =BeautifulSoup(src,'html.parser')


    # Get the Date 
    date=soup.find('span',class_='text-org')


    # Get the table
    table= soup.find('table',{"id":'headFixed'})
    headers=[]
    for i in table.find_all('th'):
        title=i.text
        headers.append(title)

    df=pd.DataFrame(columns=headers)

    for row in table.find_all('tr')[1:]:
        data=row.find_all('td')
        row_data=[td.text.strip() for td in data]
        length=len(df)
        df.loc[length]=row_data

    df=df.reset_index(drop=True)
    df=df.drop(columns='S.No', axis=1)
    df=df.set_index('Symbol')

    json_data=df.to_json(orient='index')

    return (f"As on {date}<br><br>{json_data}")

