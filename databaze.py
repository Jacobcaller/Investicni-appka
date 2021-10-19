import sqlite3
#Tímto příkazem jsem vytvořil TABLE uzivatele
# c.execute("""CREATE TABLE uzivatele(
#     login_uzivatele text,
#     heslo_uzivatele text
# )""")

conn = sqlite3.connect("C:\\Users\\hovor\\Desktop\\kody\\Investicni_appka\\databaze.db")
c = conn.cursor()

#Tato funkce ověřuje, zda se jméno zadané uživatelem náhodou již nenachází v databázi. Pokud se v ní nachází, funkce vrátí False. 
def overeni_jmena(jmeno):
    conn = sqlite3.connect("C:\\Users\\hovor\\Desktop\\kody\\Investicni_appka\\databaze.db")
    c = conn.cursor()
    if c.execute('SELECT EXISTS(SELECT * FROM uzivatele WHERE login_uzivatele =?)',(jmeno,)).fetchone() == (1,):
        conn.commit()
        conn.close()
        return False

#Tato funkce zajišťuje registraci, a zapsání přihlašovacích údajů nového uživatele do systému.
def registrace(jmeno,heslo):
    conn = sqlite3.connect("C:\\Users\\hovor\\Desktop\\kody\\Investicni_appka\\databaze.db")
    c = conn.cursor()
    c.execute("INSERT INTO uzivatele VALUES(?,?)",(jmeno,heslo))
    conn.commit()
    conn.close()

#Tato funkce ověří, zda-li jsou zadané údaje v databázi, a zda jméno, a heslo souhlasí.
def login(jmeno,heslo):
    conn = sqlite3.connect("C:\\Users\\hovor\\Desktop\\kody\\Investicni_appka\\databaze.db")
    c = conn.cursor()
    #Funkce SELECT EXISTS zjistí, jestli vybraná věc existuje, a funkce .fetchone() vrátí výsledek funkce SELECT EXISTS(vrátí (1,) pokud vybraná věc existuje , a (0,) pokud ne.)
    if c.execute('SELECT EXISTS(SELECT * FROM uzivatele WHERE heslo_uzivatele =? AND login_uzivatele =?)',(heslo,jmeno)).fetchone() == (1,):
        conn.commit()
        conn.close()
        return True
    else:
        conn.commit()
        conn.close()
        return False


conn.commit()
conn.close()



