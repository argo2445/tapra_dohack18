#!/usr/bin/env python3
import psycopg2

# SELECT date_trunc('day', date) AS "Day" ,stid,  AVG(e5), AVG(e10), AVG(diesel)
# FROM gas_station_information_history
# GROUP BY 1, stid
# ORDER BY 1 

conn=psycopg2.connect(dbname='tankerkoenig16', user='postgres', password='geheim', host='192.168.0.2', port='5432')
reader=conn.cursor()
writer=conn.cursor()

reader.execute('SELECT date_trunc(\'day\', date) AS "Day" ,stid,  AVG(e5), AVG(e10), AVG(diesel) FROM gas_station_information_history GROUP BY 1, stid ORDER BY 1 ')

while(True):
  row=reader.fetchone()
  if row==None:
    break
  # Check for invalid values
  row[2:] = [val if val>0 else None for val in row[2:]]
  writer.execute('INSERT INTO gas_station_min_history (stid, e5, e10, diesel, date) VALUES (%s, %s, %s, %s, %s);',(row[1], row[2], row[3], row[4], row[0]))
  conn.commit()
