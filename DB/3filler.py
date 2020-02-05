import mysql.connector
import pandas as pd
import glob

conn = mysql.connector.connect(
    host='localhost',
    user='eval',
    password='password',
    database='podemos_eval'
)
curs = conn.cursor()

all_csv = glob.glob('../ejercicio_modeloapiinterfaz/data_*.csv')
lst_df = []

print(all_csv)

for file in all_csv:
    lst_df.append(pd.read_csv(file, index_col=0, header=0))

for entry in lst_df[3].itertuples():
    curs.execute("""
        INSERT INTO Grupos
        VALUES {}
    """.format(tuple(entry)))
    conn.commit()
print('Data en "{}" cargada en "Grupos"'.format(all_csv[3]))

for entry in lst_df[2].itertuples():
    curs.execute("""
        INSERT INTO Cuentas
        VALUES {}
    """.format(tuple(entry)))
    conn.commit()
print('Data en "{}" cargada en "Cuentas"'.format(all_csv[2]))

for entry in lst_df[0].itertuples():
    curs.execute("""
        INSERT INTO CalendarioPagos
        VALUES {}
    """.format(tuple(entry)))
    conn.commit()
print('Data en "{}" cargada en "CalendarioPagos"'.format(all_csv[0]))

for entry in lst_df[1].itertuples():
    curs.execute("""
        INSERT INTO Clientes
        VALUES {}
    """.format(tuple(entry)))
    conn.commit()
print('Data en "{}" cargada en "Clientes"'.format(all_csv[1]))

for entry in lst_df[4].itertuples():
    curs.execute("""
        INSERT INTO Miembros
        VALUES {}
    """.format(tuple(entry)))
    conn.commit()
print('Data en "{}" cargada en "Miembros"'.format(all_csv[4]))

for entry in lst_df[5].itertuples():
    curs.execute("""
        INSERT INTO Transacciones
        VALUES {}
    """.format(tuple(entry)))
    conn.commit()
print('Data en "{}" cargada en "Transacciones"'.format(all_csv[5]))

conn.close()
