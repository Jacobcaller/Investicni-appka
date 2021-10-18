import sqlite3
#TABLE uzivatele
# #     login_uzivatele text,
# #     heslo_uzivatele text

conn = sqlite3.connect("C:\\Users\\hovor\\Desktop\\kody\\Investicni_appka\\databaze.db")
c = conn.cursor()

#Zajišťuje registraci, a zapsání přihlašovacích údajů nového uživatele do systému.
def registrace(jmeno,heslo):
    conn = sqlite3.connect("C:\\Users\\hovor\\Desktop\\kody\\Investicni_appka\\databaze.db")
    c = conn.cursor()
    c.execute("INSERT INTO uzivatele VALUES(?,?)",(jmeno,heslo))
    conn.commit()
    conn.close()

#Ověří, zda-li jsou zadané údaje v databázi, a zda jméno, a heslo souhlasí.
def login(jmeno,heslo):
    conn = sqlite3.connect("C:\\Users\\hovor\\Desktop\\kody\\Investicni_appka\\databaze.db")
    c = conn.cursor()
    #SELECT EXISTS zjistí jestli vybraná věc existuje, a .fetchone() a vrátí výsledek SELECT EXISTS - vrátí (1,) pokud vybraná věc existuje , a (0,) pokud ne.
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



