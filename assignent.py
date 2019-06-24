#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 13:03:54 2019

@author: manzar
"""

import pandas as pd
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

url = 'http://www.bifga.org.uk/trade-directory'
req = requests.get(url)
soup = BeautifulSoup(req.text, 'lxml')
table = soup.findAll('table', {'class': 'views-table cols-2'})
tds = table[0].findAll('td', {'class': 'views-field views-field-title'})
links = []
for td in tds:
    links.append(urljoin(url, td.a.attrs['href']))
    
contacts = []
web = []
email = []
name = []
for link in links:
    req = requests.get(link)
    soup = BeautifulSoup(req.text, 'lxml')
    name.append(soup.findAll('h1')[0].text)
    try:
        em = soup.findAll('div', {'class': 'field-name-field-trade-email'})
        email.append(em[0].a.attrs['href'].split('mailto:')[1])
    except:
        email.append('NaN')
    
    try:
        wb = soup.findAll('div', {'class': 'field-name-field-trade-website'})
        web.append(wb[0].a.attrs['href'])
    except:
        web.append('NaN')
    try:
        table = soup.findAll('table', {'id': 'group-contacts-values'})
        trs = table[0].findAll('tr', {'class': 'row-delta-0'})
        #print(tds)
    except:
        pass
    
    tds = trs[0].findAll('td')
    #print(td)
    

    contact = []
    for td in tds:
        if(len(td) == 0):
            pass
        else:
            contact.append(td.text)
    contacts.append(contact)
count = 0
contact_person = []
contact_email = []
numcount = []
for c in contacts:
    cemail = ''
    cname = ''
    num_count = 0
    for co in c:
        #print(co)
        if('@' in co):
            cemail = co
        if(any(x.isalpha() for x in co) and ('@' not in co)):
            cname = co
            #print(co)
        if(not any(x.isalpha() for x in co)):
            num_count += 1
    if(cname == ''):
        cname = 'NaN'
    if(cemail == ''):
        cemail = 'NaN'
    contact_person.append(cname)
    contact_email.append(cemail)
    numcount.append(num_count)
    print(cname, cemail, num_count)
    count += 1
    
contact_fax = []
contact_tel = []
    
ex = contacts
c = 0
for x in ex:
    count = 0
    for p in x:
        if(any(x.isalpha() for x in p)):
            print(ex[c].pop(count))
        count += 1
    c += 1

for x in ex:
    if(len(x) == 1):
        contact_tel.append(x[0])
        contact_fax.append('NaN')
    elif(len(x) == 2):
        contact_tel.append(x[0])
        contact_fax.append(x[1])
        
file = open('assignment.csv', 'w')
header = 'Company Name, Email, Website, ContactPerson name, ContactPerson email, ContactPerson telephone, ContactPerson Fax\n'
file.write(header)
for i in range(len(contacts)):
    file.write(name[i] + ', ' + email[i] + ', ' + web[i] + ', ' + contact_person[i] + ', ' + contact_email[i] + ', ' + contact_tel[i] + ', ' + contact_fax[i] + '\n')

file.close()
file = pd.read_csv('assignment.csv')   
'''     
    cname = True
    ctel = True
    cfax = True
    cemail = True
    num_count = 0
    for c in contacts:
        if('@' in c):
            cemail = False
        if(any(x.isalpha() for x in c) and ('@' not in c)):
            cname = False
        if(not any(x.isalpha() for x in c)):
            num_count += 1
    if(num_count == 1):
        ctel = False
    if(num_count == 0):
        ctel = False
        cfax = False
    print(cname, ctel, cfax, cemail)
'''
        
    