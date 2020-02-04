# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 12:27:11 2020

@author: n7iqb
"""

import sqlite3,pandas as pd

conn = sqlite3.connect("final_db.db") #Connects to the database file in memory

c = conn.cursor() #cursor object that connects to the database

SQL_Query = pd.read_sql_query("SELECT Substrate.Kinase, Substrate.Sub_Gene, Substrate.Sub_Mod_Rsd FROM Substrate",conn)


df_home = pd.DataFrame(SQL_Query, columns=['Kinase','Sub_Gene','Sub_Mod_Rsd'])

print (df_home)