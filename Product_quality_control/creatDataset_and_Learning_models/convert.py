import json
import csv

with open('forData.json', 'r') as data, open('dataGaki.cvs', 'w', newline='', encoding='utf-8') as table:
    dt = json.load(data)
    tableHeader = [['area1', 'area', 'per1', 'per', 'cont', 'apr', 'target']]
    for i in dt:
        tableHeader.append(i)
    print(tableHeader)
    writer = csv.writer(table)
    writer.writerows(tableHeader)