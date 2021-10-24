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
    c.execute("INSERT INTO uzivatele VALUES(?,?,?)",(jmeno,heslo,100))
    for i in c.execute("SELECT nazev_fondu FROM fondy").fetchall():
        c.execute("INSERT INTO portfolio VALUES(?,?,?,?,?,?)",(jmeno,i[0],0,0,0,0))
        conn.commit()
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

#Funkce pro výpis portfolia + v ní funkce na nákup
def vypis_portfolia(jmeno):

    conn = sqlite3.connect("C:\\Users\\hovor\\Desktop\\kody\\Investicni_appka\\databaze.db")
    c = conn.cursor()

    if c.execute("SELECT EXISTS(SELECT * FROM portfolio WHERE majitel_portfolia = ? AND celkove_mnozstvi_akcii = ?)",(jmeno, 1.0)).fetchall()[0] == (1,):
        for i in c.execute('SELECT * FROM portfolio WHERE majitel_portfolia = ?',(jmeno,)).fetchall():
            print("Název Fondu: ",i[1])
            print("Množství akcií: ",i[2])
            print("Průměrná cena nákupu: ", round(i[3],4))
            print("Zisk: ", round(i[4],4),"\n")
    else:
        print("V tuto chvíli je vaše portfolio prázdné.")

def nakup_akcii(jmeno):
    conn = sqlite3.connect("C:\\Users\\hovor\\Desktop\\kody\\Investicni_appka\\databaze.db")
    c = conn.cursor()

    # VÝPIS FONDŮ A JEJICH AKTUÁLNÍCH CEN
    for i in c.execute("SELECT rowid, * FROM fondy").fetchall():
        nazev_fondu = i[1]
        print("Číslo fondu: ",i[0])
        print(nazev_fondu)
        hodnota = round(random.uniform(i[2],i[3]),4)
        print("Předchozí cena fondu: ", i[5])
        print("Aktuální cena fondu je: ",hodnota,"Kč")
        if hodnota > i[5]:
            rozdil = hodnota - i[5]
            print("Cena vzrostla o", round(rozdil,3),"Kč za akcii.\n")
        elif hodnota < i[5]:
            rozdil = i[5] - hodnota
            print("Cena klesla o", round(rozdil,3),"Kč za akcii.\n")
        else:
            print("Cena se nezměnila.")
        c.execute ('UPDATE fondy SET aktualni_hodnota = ?,posledni_hodnota = ? WHERE nazev_fondu = ?',(hodnota, hodnota, nazev_fondu))
        conn.commit()

    stav_uctu = c.execute("SELECT stav_uctu FROM uzivatele WHERE login_uzivatele = ?",(jmeno,)).fetchone()[0]
    print("Stav vašich finančích prostředku: ",stav_uctu,"Kč")
    if input("Chcete provést nákup akcii?(a/n)") == "a":
        fond = input("Vlož číslo fondu do kterého chceš investovat: ")
        mnozstvi = int(input("Zadej množství akcii které chceš koupit: "))
        nazev_kupovaneho_fondu = c.execute("SELECT * FROM fondy WHERE rowid = ?",(fond,)).fetchall()[0][0]
        akt_cena_kup_akc = c.execute("SELECT aktualni_hodnota FROM fondy WHERE nazev_fondu = ?",(nazev_kupovaneho_fondu,)).fetchall()[0][0]
        if (akt_cena_kup_akc * mnozstvi) < stav_uctu:
            stav_uctu -= (c.execute("SELECT * FROM fondy WHERE rowid = ?",(fond,)).fetchall()[0][3] * mnozstvi)
            celkova_cena = c.execute("SELECT * FROM fondy WHERE rowid = ?",(fond,)).fetchall()[0][3] * mnozstvi
            vypis_portfolio = c.execute("SELECT * FROM portfolio WHERE majitel_portfolia =? AND nazev_fondu =?",(jmeno,nazev_kupovaneho_fondu)).fetchall()
            mnozstvi_nakup = mnozstvi + vypis_portfolio[0][2]
            prumerna_cena = ((vypis_portfolio[0][3] * vypis_portfolio[0][2])+celkova_cena) / (vypis_portfolio[0][2]+mnozstvi)
            zisk = akt_cena_kup_akc - vypis_portfolio[0][3]
            c.execute ('UPDATE uzivatele SET stav_uctu = ? WHERE login_uzivatele = ?',(stav_uctu, jmeno))
            #INSERT INTO NAKUPY
            c.execute("INSERT INTO nakupy VALUES(?,?,?,?)",(nazev_kupovaneho_fondu, jmeno, celkova_cena, mnozstvi))
            #UPDATE HODNOTY V PORTFOLIO
            c.execute ('UPDATE portfolio SET mnozstvi_akcii = ?, prumerna_cena_nakupu = ?, zisk = ?, celkove_mnozstvi_akcii = ? WHERE majitel_portfolia = ? AND nazev_fondu = ?',(mnozstvi_nakup, prumerna_cena, zisk, 1, jmeno, nazev_kupovaneho_fondu))
            print(f"Potvrzujeme vaši koupi {mnozstvi}ks cenných papírů fondu {nazev_kupovaneho_fondu}, ve výši {akt_cena_kup_akc}Kč za kus, v celkové hodnotě {celkova_cena}Kč.")
        else:
            print("Na tuto transakci nemáte dostatečné finanční prostředky.")
        conn.commit()
    conn.commit()
    conn.close()

def prodej_akcii(jmeno):
    if input("Chcete provést nákup akcii?(a/n)") == "a":
        pass

def historie_transakci(jmeno):
    conn = sqlite3.connect("C:\\Users\\hovor\\Desktop\\kody\\Investicni_appka\\databaze.db")
    c = conn.cursor()
    if c.execute('SELECT EXISTS(SELECT * FROM nakupy WHERE kupec =?)',(jmeno,)).fetchone() == (1,):
        print("Toto je seznam všech vašich transakcí: ")
        for i in c.execute('SELECT rowid,* FROM nakupy WHERE kupec =?',(jmeno,)).fetchall():
            print(f"{i[0]}. Nakoupil jste {round(i[4],3)}ks akcií fondu {i[1]}. Cena 1ks akcie byla {round(i[3],3)}Kč. Celková cena transakce byla {round(i[4]*i[3],3)}Kč.")
    else:
        print("Zatím jste neprovedl žádné transakce.\n")   
    conn.commit()
    conn.close()

conn.commit()
conn.close()