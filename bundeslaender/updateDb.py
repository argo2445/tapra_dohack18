#!/usr/bin/env python3
from lib.germanCities_ca import cities
import psycopg2
import csv

# Dieses Script ordnet jeder Tankstelle das entsprechende Bundesland zu.
# Die Bundesländer wurdem dem Städteverzeichnis unter https://gist.github.com/embayer/772c442419999fa52ca1
# entnommen  

def get_state_by_name(cityName):
  
  for city in cities:
    if city['stadt'].upper()==cityName.upper():
      return city['bundesland']
  

    mcity=city['stadt'].replace('ue','ü')
    mcity=mcity.replace('oe','ö')
    mcity=mcity.replace('ae','ä')
    #mcity=mcity.replace('ß','ss')
    if mcity.upper()==cityName.upper():
      return city['bundesland']
  #print("Die Stadt "+cityName+" wurde nicht gefunden")
  return None
def get_state_by_postcode(postcode):
  with open('./bundeslaender/lib/zuordnung_plz_ort.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
      if row[2]==postcode:
        return row[3]
  return None

conn=psycopg2.connect(dbname='tankerkoenig16', user='postgres', password='geheim', host='192.168.0.2', port='5432')
cur=conn.cursor()

#cur.execute('SELECT * FROM gas_station LIMIT 10')
#print(cur.fetchall())

states=[]
for city in cities:
  if city['bundesland'] not in states:
    states.append(city['bundesland'])
print(states)
# Add missing States
for state in states: 
  # Look up if State is already in DB
  cur.execute('SELECT name FROM state WHERE name=%s;',(state,))
  st=cur.fetchall()
  if len(st)==0:
    #Not in DB INSERT it
    cur.execute('INSERT INTO state (name) VALUES (%s);',(state,))
    conn.commit()
    print (state+' added to Database \n')


cur.execute('SELECT id, place, post_code, stateid FROM gas_station WHERE stateid IS NULL;')
rows=cur.fetchall()
while(len(rows)>0):
  row=rows.pop(0)
  # row[0]: id
  # row[1]: place
  
  state=get_state_by_name(row[1])
  if state==None: 
    state=get_state_by_postcode(row[2])
  if state != None:
    print(row[1]+": "+state)
    if state !=None:
      # find ID of Assigned State
      cur.execute('SELECT id FROM state WHERE name=%s;',(state,))
      id=cur.fetchone()
      # Write State to gas_station
      cur.execute('UPDATE gas_station SET stateid=%s WHERE id=%s ',(id,row[0]))
      conn.commit()
  else:
    print("Die Stadt "+row[1]+" wurde nicht gefunden")

conn.close()
    

