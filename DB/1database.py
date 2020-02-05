import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='eval',
    password='password',
)

curs = conn.cursor()

curs.execute("""
    CREATE SCHEMA IF NOT EXISTS `podemos_eval`
    DEFAULT CHARACTER SET utf8 ;
    USE `podemos_eval`;
      """)

print('Base de datos "podemos_eval" creada')

