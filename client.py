#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import MySQLdb
from datetime import datetime,timedelta

DB_HOST = 'localhost'
DB_USER = 'userRoot'
DB_PASS = 'root'
DB_NAME = 'Firmas'

def run_query(query=''):
    datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME]

    conn = MySQLdb.connect(*datos) # Conectar a la base de datos
    cursor = conn.cursor()         # Crear un cursor
    cursor.execute(query)          # Ejecutar una consulta

    if query.upper().startswith('SELECT'):
        data = cursor.fetchall()   # Traer los resultados de un select
    else:
        conn.commit()              # Hacer efectiva la escritura de datos
        data = None

    cursor.close()                 # Cerrar el cursor
    conn.close()                   # Cerrar la conexión

    return data

def esPrimo(num):
    for i in range(2,num):
        if(num%i) == 0:
            return False
    return True

def genPrimoRandom(n):
    P = random.randrange(n,2*n)
    while not(esPrimo(P)):
        P = P + 1
        if(P == 2*n):
            P = n
    return P

def MCD(a,b):
    resto = 0
    while(b > 0):
        resto = b;
        b = a % b
        a = resto
    return a

def esCoprimo(e, phi):
    if(MCD(e,phi) == 1):
        return True
    else:
        return False

def eucExt(a,b):
    r = [a,b]
    s = [1,0]
    t = [0,1]
    i = 1
    q = [[]]
    while (r[i] != 0):
        q = q + [r[i-1] // r[i]]
        r = r + [r[i-1] % r[i]]
        s = s + [s[i-1] - q[i]*s[i]]
        t = t + [t[i-1] - q[i]*t[i]]
        i = i+1
    return (r[i-1], s[i-1], t[i-1])

def genRSAKeys():
    p = genPrimoRandom(100000)
    q = genPrimoRandom(100000)
    while q == p:
        q = genPrimoRandom(100000)
    n = p * q
    phi = (p-1)*(q-1)
    e = random.randrange(phi)
    while not(esCoprimo(e,phi)):
        e = random.randrange(phi)
    d = eucExt(e, phi)[1]
    if d < 0:
        d = d + phi
    return (e,d,n)

def registrarUsuario(correo):
    nombre = raw_input("Escriba su nombre>>")
    fecha = datetime.now().date() + timedelta(days=7)
    keys = genRSAKeys()
    query = "INSERT INTO usuarios (nombre, correo, e, expirationDate, n) VALUES ('%s', '%s', '%i', '%s', '%i')" % (nombre, correo, keys[0], fecha, keys[2])
    run_query(query)
    with open('keys/' + nombre + '.key', 'w') as writePrivateFile:
        writePrivateFile.write('d:' + str(keys[1]) + '\nn:' + str(keys[2]))
    print('Listo!')

def updateKeys(correo,nombre):
    keys = genRSAKeys()
    fecha = datetime.now().date() + timedelta(days=7)
    query = "UPDATE usuarios SET e='%i', expirationDate='%s', n='%i' WHERE correo='%s'" % (keys[0], fecha, keys[2], correo)
    run_query(query)
    with open('keys/' + nombre + '.key', 'w') as writePrivateFile:
        writePrivateFile.write('d:' + str(keys[1]) + '\nn:' + str(keys[2]))
    print('Listo!')

correo = raw_input("Escribe tu correo>>  ").lower()
query = "SELECT nombre,expirationDate FROM usuarios WHERE correo='%s'" % correo
result = run_query(query)
if len(result) == 0:
    print('Se ha detectado un nuevo usuario, favor de registrarse...')
    registrarUsuario(correo)
elif(result[0][1] < datetime.now().date()):
    print('Llaves caducadas. Se actualizaran las llaves')
    updateKeys(correo,result[0][0])
else:
    print('Bienvenido')
