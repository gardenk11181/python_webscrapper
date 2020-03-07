import xmlrpc

import requests
import json
import csv
from bs4 import BeautifulSoup
from xml.dom.minidom import parseString

PAGE = 3
URL = f"https://store.naver.com/hospitals/list?department=%ED%95%9C%EC%9D%98%EC%9B%90&page={PAGE}&query=%EA%B2%BD%EA%B8%B0%EB%8F%84%20%EC%9A%A9%EC%9D%B8%EC%8B%9C%20%ED%95%9C%EC%9D%98%EC%9B%90&queryType=hospital&sessionid=9ZFDcQfAJaZzIqnXZm%2FKAQ%3D%3D&sortingOrder=precision"

def bar(somejson, key):
    def val(node):
        # Searches for the next Element Node containing Value
        e = node.nextSibling
        while e and e.nodeType != e.ELEMENT_NODE:
            e = e.nextSibling
        return (e.getElementsByTagName('string')[0].firstChild.nodeValue if e
                else None)
    # parse the JSON as XML
    foo_dom = parseString(xmlrpc.client.dumps((json.loads(somejson),)))
    # and then search all the name tags which are P1's
    # and use the val user function to get the value
    return [val(node) for node in foo_dom.getElementsByTagName('name')
            if node.firstChild.nodeValue in key]

def extract_hospital():
    result = requests.get(URL)


    soup = BeautifulSoup(result.text, "html.parser")  # page의 모든 html을 가져온다.
    string = str(soup.find_all("script")[2])
    string = string[27:-9]
    str_json = json.loads(string)

    items = str_json['businesses']["[department:한의원][query:경기도 용인시 한의원][queryType:hospital][sessionid:9ZFDcQfAJaZzIqnXZm/KAQ==][sortingOrder:precision]"]['items']
    lists = []
    count=0
    for item in items:
        if item is None:
            break
        count = count+1
        lists.append({
               'Name': item['name'],
                'Address': item['roadAddr'],
                'Phone': item['phone']
                })

    return lists

def save_to_file(hospitals):
    file = open("jobs.csv",mode="w",encoding="utf-8",newline="")
    writer = csv.writer(file)
    writer.writerow(["Name","Address","Phone"])
    for hospital in hospitals:
        writer.writerow(list(hospital.values()))
    return

save_to_file(extract_hospital())