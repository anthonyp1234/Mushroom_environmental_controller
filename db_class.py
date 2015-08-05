#!/usr/bin/env python2.7  
####Define Database being used
import datetime
import sqlite3


class database:
  def __init__(self, name, size):
    self.filename = name
    self.size = size  # How many lines for the table to store data.
    self.conn = sqlite3.connect(self.filename) ##open file when starting instance
  
  def addreadings(self, time, temp1, temp2, hum1, hum2,c02):    
    self.conn.cursor.execute("INSERT INTO readings VALUES ({0},{1},{2}, {3}, {4})".format(time, temp1, temp2, hum1, hum2,c02))
    conn.commit() 
    
    triggers = self.conn.cursor.execute('SELECT * FROM readings')
    tablesize = len(triggers.fethall())
    
    if tablesize >= 2* self.size: #remove when twice the size of max, so as to not do too many table deletes.
      self.conn.cursor.execute('DELETE FROM readings WHERE NOT EXISTS in (SELECT id FROM readings ORDER BY id LIMIT self.size );') ###Remove first line of table.
      conn.commit()

  def addstates(self, time, tempavg, trelay, humavg, humrelay, c02avg,c02relay):    
    self.conn.cursor.execute("INSERT INTO states VALUES ({0},{1},{2}, {3}, {4})".format(time, tempavg, trelay, humavg, humrelay, c02avg,c02relay))
    conn.commit()  
    
    triggers = self.conn.cursor.execute('SELECT * FROM states')
    tablesize = len(triggers.fethall())
    
    if tablesize >= 2* self.size: #remove when twice the size of max, so as to not do too many table deletes.
      self.conn.cursor.execute('DELETE FROM states WHERE NOT EXISTS in (SELECT id FROM states ORDER BY id LIMIT self.size );') ###Remove first line of table.
      conn.commit()
    
    
    
  def read_triggers(self):
    triggers = self.conn.cursor.execute('SELECT * FROM triggers')    
    return triggers.fetchone()  ###returns tuple. just index the value. [temp,humidity,c02]
       
  def connection_close(self):
    self.conn.close()    
    