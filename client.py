import random
import MySQLdb

DB_HOST = 'localhost'
DB_USER = 'userRoot'
DB_PASS = 'root'
DB_NAME = 'Firmas'

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
