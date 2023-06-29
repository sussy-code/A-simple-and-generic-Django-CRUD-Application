import petl as etl
import sqlite3
from API.datapipeline.PipelineHub import ApiResponse, ReferenceData
import re
import sqlite3
import json

class DBTable:
  def __init__(self, tableName, databaseUrl, dn=None, password=None):
    self.tableName = tableName
    # URL Completed with the authentification informations protocol://url:server@user:password
    self.databaseUrl = databaseUrl
    self.dn = dn
    self.password = password

''' We could imagine defining here the db tables that we will be used '''
student_table = DBTable('students_app_student', 'studentsDB.sqlite3')  # URL Complete with the authentification informations protocol://url:server@user:password

def fetch_all(reference):
  if (reference.reference.role == "all"):
    conn = sqlite3.connect(student_table.databaseUrl)
    fetched_data = etl.fromdb(conn, 'SELECT * FROM students_app_student')
    fetched_data = etl.dicts(etl.sort(fetched_data))
    conn.commit()
    return [ReferenceData.from_flat_dicts(element) for element in fetched_data]
  elif (reference.reference.role != ""):
    conn = sqlite3.connect(student_table.databaseUrl)
    fetched_data = etl.fromdb(conn, 'SELECT * FROM students_app_student WHERE role = ?', (reference.reference.role, ))
    fetched_data = etl.dicts(etl.sort(fetched_data))
    conn.commit()
    return [ReferenceData.from_flat_dicts(element) for element in fetched_data]

def fetchByID(id: int):
  conn = sqlite3.connect(student_table.databaseUrl)
  fetched_data = etl.fromdb(conn, 'SELECT * FROM students_app_student WHERE id = ?', (id,))
  fetched_data = etl.dicts(etl.sort(fetched_data))
  conn.commit()
  return ReferenceData.from_flat_dicts(fetched_data[0])

def fetchByUsername(username: str):
  conn = sqlite3.connect(student_table.databaseUrl)
  fetched_data = etl.fromdb(conn, 'SELECT * FROM students_app_student WHERE username = ?', (username,))
  fetched_data = etl.dicts(etl.sort(fetched_data))
  conn.commit()
  return ReferenceData.from_flat_dicts(fetched_data[0])

def delete(id: int):
  conn = sqlite3.connect(student_table.databaseUrl)
  cursor = conn.cursor()
  cursor.execute('DELETE FROM students_app_student WHERE id = ?', (id,))
  cursor.fetchall()
  conn.commit()
  return True

def update(id: int, updated_reference: ReferenceData):
  conn = sqlite3.connect(student_table.databaseUrl)
  cursor = conn.cursor()
  output = cursor.execute('UPDATE students_app_student SET first_name = ?, last_name = ?, role = ?, age = ?, grade = ?, homeaddress = ?WHERE id = ?', (updated_reference.reference.first_name, updated_reference.reference.last_name, updated_reference.reference.role, updated_reference.reference.age, updated_reference.reference.grade, updated_reference.reference.homeaddress, id))
  conn.commit()
  return True

def insert(new_reference: ReferenceData):
  conn = sqlite3.connect(student_table.databaseUrl)
  cursor = conn.cursor()
  output = cursor.execute('INSERT INTO students_app_student (first_name, last_name, role, age, grade, homeaddress) VALUES (?, ?, ?, ?, ?, ?)', (new_reference.reference.first_name, new_reference.reference.last_name, new_reference.reference.role, new_reference.reference.age, new_reference.reference.grade, new_reference.reference.homeaddress))
  conn.commit()
  return True