import sqlite3
#Tímto příkazem jsem vytvořil TABLE uzivatele
# c.execute("""CREATE TABLE uzivatele(
#     login_uzivatele text,
#     heslo_uzivatele text
# )""")

# c.execute("""CREATE TABLE fondy(
#     nazev_fondu text,
#     vlastnici_fondu text,
#     min_cena real,
#     max_cena real
# )""")
# c.execute ("INSERT INTO fondy VALUES('Bohatství','admin','2.0310','2.6017')")
# c.execute("""CREATE TABLE nakupy(
# # nazev_fondu text,
# # kupec text,
# # cena_nakupu real,
# # mnozstvi real
# # )""")
# conn.commit()
# conn.close()
# c.execute ("INSERT INTO nakupy VALUES('Bohatství','admin','2.0310','2.5')")
conn = sqlite3.connect("C:\\Users\\hovor\\Desktop\\kody\\Investicni_appka\\databaze.db")
c = conn.cursor()
#Testovací výpis
# print(c.execute("SELECT * FROM fondy").fetchall())


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

def vypis_portfolia(jmeno):
    conn = sqlite3.connect("C:\\Users\\hovor\\Desktop\\kody\\Investicni_appka\\databaze.db")
    c = conn.cursor()
    if c.execute('SELECT EXISTS(SELECT * FROM fondy WHERE vlastnici_fondu =?)',(jmeno,)).fetchone() == (1,):
        print(c.execute('SELECT * FROM nakupy WHERE kupec =?',(jmeno,)).fetchall())
    else:
        print("Momentálně nevlastníte podíl v žádném fondu.")
    conn.commit()
    conn.close()

conn.commit()
conn.close()