import sqlite3
import random

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
print(c.execute("SELECT * FROM fondy").fetchall())


#Funkce pro výpis portfolia + v ní funkce na nákup
def vypis_portfolia(jmeno):
    # doc_db = sqlite3.connect(':memory:') 
    # c_doc = doc_db.cursor()
    conn = sqlite3.connect("C:\\Users\\hovor\\Desktop\\kody\\Investicni_appka\\databaze.db")
    c = conn.cursor()
    for i in c.execute("SELECT * FROM fondy").fetchall():
        nazev_fondu = i[0]
        print(nazev_fondu)
        hodnota = round(random.uniform(i[1],i[2]),3)
        print("Předchozí cena fondu: ", i[4])
        print("Aktuální cena fondu je: ",hodnota)
        c.execute ('UPDATE fondy SET aktualni_hodnota = ?,posledni_hodnota = ? WHERE nazev_fondu = ?',(hodnota, hodnota, nazev_fondu))


    if c.execute("SELECT EXISTS(SELECT * FROM portfolio WHERE majitel_portfolia = ?)",(jmeno,)).fetchall() == (1,):
        print(c.execute('SELECT * FROM portfolio WHERE majitel_portfolia = ?)',(jmeno,)).fetchall())
    else:
        print("V tuto chvíli je vaše portfolio prázdné.")


    if input("Chcete provést nákup akcii?(a/n)") == "a":
        pass


    if input("Chcete provést nákup akcii?(a/n)") == "a":
        pass


    if input("Chcete zobrazit historii transakcí?(a/n):") == "a":
        if c.execute('SELECT EXISTS(SELECT * FROM nakupy WHERE kupec =?)',(jmeno,)).fetchone() == (1,):
            print("Toto je seznam všech vašich transakcí: ")
            for i in c.execute('SELECT rowid,* FROM nakupy WHERE kupec =?',(jmeno,)).fetchall():
                print(f"{i[0]}. Nakoupil jste {round(i[4],3)}ks akcií fondu {i[1]}. Cena 1ks akcie byla {round(i[3],3)}Kč. Celková cena transakce byla {round(i[4]*i[3],3)}Kč.")
        else:
            print("Zatím jste neprovedl žádné transakce.\n")

        
    conn.commit()
    conn.close()
    # c_doc.close()
    
    

conn.commit()
conn.close()