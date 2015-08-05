import sqlite3
import sys



# print "Welcome, what do you want to do?"
# print "1) Create a new DB?"
# print "2) Delete existing DB and create new one?"
# print "3) Exit"


print "Used to create Mushroom DB, default filename is 'db.mushroom.sqlite3'"
print "Else add argument to create DB with different name"

s = raw_input('This WILL DELETE EXISTING DB, type "YES" to continue: ')

if s != "YES":
  print "Exiting"
  sys.exit(0)

try:
  filename = sys.argv[1]
except:
  filename = 'db.mushroom.sqlite3'

conn = sqlite3.connect(filename)


curs = conn.cursor()

print "Creating Time, Temp1, temp2, hum1, hum2, C02  table"
# Create table
curs.execute('''CREATE TABLE readings
             (date text, temp1 real, temp2 real, hum1 real, hum2 real, c02 integer)''')

curs.execute('''CREATE TABLE triggers
             (temp real, hum real, c02 integer)''')
         
curs.execute('''CREATE TABLE states
             (date text, temp real, trelay real,  hum real, hrelay real, c02 integer, c02relay real)''')             
             
##### creat inital trigger values
curs.execute('''INSERT INTO triggers VALUES ('20', '80', '4000')''')

             
conn.commit()             
             
print "\n\nDatabase created, and contains:\n\n"
import pdb; pdb.set_trace()

for line in conn.iterdump():
  print line



conn.close()