# -*- coding: utf-8 -*-
"""
Created on Sun Feb 27 13:26:24 2022

@author: ASpan
"""

import pandas as pd
from sqlalchemy import create_engine
import psycopg2 
import io
import getpass

# connecting to local db
pswd = getpass.getpass('Password:')
engine = create_engine('postgresql+psycopg2://postgres:' + pswd + '@localhost:5432/pklm')
conn = engine.raw_connection()
cur = conn.cursor()


# writing to an existing table
cur = conn.cursor()
output = io.StringIO()

df.to_csv(output, sep='\t', header=False, index=False)
output.seek(0)
contents = output.getvalue()
cur.copy_from(output, 'table_name', null="") # null values become
conn.commit()