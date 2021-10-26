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

#Funkce pro výpis portfolia
def vypis_portfolia(jmeno):

    conn = sqlite3.connect("C:\\Users\\hovor\\Desktop\\kody\\Investicni_appka\\databaze.db")
    c = conn.cursor()

    if c.execute("SELECT EXISTS(SELECT * FROM portfolio WHERE majitel_portfolia = ? AND celkove_mnozstvi_akcii > 0)",(jmeno,)).fetchall()[0] == (1,):
        for i in c.execute('SELECT * FROM portfolio WHERE majitel_portfolia = ? AND mnozstvi_akcii > 0',(jmeno,)).fetchall():
            print("Název Fondu: ",i[1])
            print("Množství akcií: ",i[2])
            print("Průměrná cena nákupu: ", round(i[3],4))
            print("Aktuální cena za akcii: ", c.execute("SELECT aktualni_hodnota FROM fondy WHERE nazev_fondu = ?",(i[1],)).fetchall()[0][0])
            zisk_ztrata = (i[2] * i[3]) - (i[2] * c.execute('SELECT aktualni_hodnota FROM fondy WHERE nazev_fondu = ?',(i[1],)).fetchall()[0][0])
            if zisk_ztrata > 0:
               print("Zisk: ", round(zisk_ztrata,4),"Kč\n")
            elif zisk_ztrata < 0:
                print("Ztráta: ", round(zisk_ztrata,4),"Kč\n")
            else:
                print("Zisk/ztráta: ",zisk_ztrata,"Kč\n")

    else:
        print("V tuto chvíli je vaše portfolio prázdné.")

#Funkce pro nákup akcií
def nakup_akcii(jmeno):
    conn = sqlite3.connect("C:\\Users\\hovor\\Desktop\\kody\\Investicni_appka\\databaze.db")
    c = conn.cursor()

    # VÝPIS FONDŮ A JEJICH AKTUÁLNÍCH CEN
    for i in c.execute("SELECT rowid, * FROM fondy").fetchall():
        nazev_fondu = i[1]
        print("\nČíslo fondu: ",i[0])
        print(nazev_fondu)
        hodnota = round(random.uniform(i[2],i[3]),4)
        print("Předchozí cena fondu: ", i[5])
        print("Aktuální cena fondu je: ",hodnota,"Kč")
        prumerna_cena_v_ptf = c.execute("SELECT prumerna_cena_nakupu FROM portfolio WHERE majitel_portfolia = ? AND nazev_fondu = ?",(jmeno,nazev_fondu)).fetchall()[0][0]
        stav_uctu = c.execute("SELECT stav_uctu FROM uzivatele WHERE login_uzivatele = ?",(jmeno,)).fetchone()[0]
        if hodnota > i[5]:
            rozdil = hodnota - i[5]
            print("Cena vzrostla o", round(rozdil,3),"Kč za akcii.")
        elif hodnota < i[5]:
            rozdil = i[5] - hodnota
            print("Cena klesla o", round(rozdil,3),"Kč za akcii.")
        elif hodnota == i[5]:
            print("Cena se nezměnila.")
        print("Se stavem vašeho účtu si můžete koupit",round((stav_uctu / hodnota),4), "ks akcií tohoto fondu.")
        if c.execute("SELECT mnozstvi_akcii FROM portfolio WHERE majitel_portfolia = ? AND nazev_fondu = ?",(jmeno,nazev_fondu)).fetchall()[0][0] > 0:
            if (prumerna_cena_v_ptf - hodnota) > 0:
                print("Aktuální cena za akcii je nižší o ",round((prumerna_cena_v_ptf - hodnota),4),"Kč za kus, než je vaše průměrná nákupní cena akcie v tomto fondu.")
            elif (prumerna_cena_v_ptf - hodnota) < 0:
                print("Aktuální cena za akcii je vyšší o ",round((hodnota - prumerna_cena_v_ptf),4),"Kč za kus, než je vaše průměrná nákupní cena akcie v tomto fondu.")
            else:
                print("Aktuální cena za kus této akcie je stejná jako vaše průměrná nákupní cena v tomto fondu.")

        
        c.execute ('UPDATE fondy SET aktualni_hodnota = ?,posledni_hodnota = ? WHERE nazev_fondu = ?',(hodnota, hodnota, nazev_fondu))
        conn.commit()

    stav_uctu = c.execute("SELECT stav_uctu FROM uzivatele WHERE login_uzivatele = ?",(jmeno,)).fetchone()[0]
    print("\nStav vašich finančích prostředku: ",round(stav_uctu,4),"Kč")
    if input("Chcete provést nákup akcii?(a/n)") == "a":
        fond = input("Vlož číslo fondu do kterého chceš investovat: ")
        mnozstvi = float(input("Zadej množství akcii které chceš koupit: "))
        nazev_kupovaneho_fondu = c.execute("SELECT * FROM fondy WHERE rowid = ?",(fond,)).fetchall()[0][0]
        akt_cena_kup_akc = c.execute("SELECT aktualni_hodnota FROM fondy WHERE nazev_fondu = ?",(nazev_kupovaneho_fondu,)).fetchall()[0][0]
        if (akt_cena_kup_akc * mnozstvi) < stav_uctu:
            stav_uctu -= (c.execute("SELECT * FROM fondy WHERE rowid = ?",(fond,)).fetchall()[0][3] * mnozstvi)
            celkova_cena = c.execute("SELECT * FROM fondy WHERE rowid = ?",(fond,)).fetchall()[0][3] * mnozstvi
            vypis_portfolio = c.execute("SELECT * FROM portfolio WHERE majitel_portfolia =? AND nazev_fondu =?",(jmeno,nazev_kupovaneho_fondu)).fetchall()
            mnozstvi_nakup = mnozstvi + vypis_portfolio[0][2]
            prumerna_cena = ((vypis_portfolio[0][3] * vypis_portfolio[0][2])+celkova_cena) / (vypis_portfolio[0][2]+mnozstvi)
            c.execute ('UPDATE uzivatele SET stav_uctu = ? WHERE login_uzivatele = ?',(stav_uctu, jmeno))
            #INSERT INTO NAKUPY
            c.execute("INSERT INTO nakupy VALUES(?,?,?,?)",(nazev_kupovaneho_fondu, jmeno, celkova_cena, mnozstvi))
            #UPDATE HODNOTY V PORTFOLIO
            c.execute ('UPDATE portfolio SET mnozstvi_akcii = ?, prumerna_cena_nakupu = ?, celkove_mnozstvi_akcii = ? WHERE majitel_portfolia = ? AND nazev_fondu = ?',(mnozstvi_nakup, prumerna_cena, (vypis_portfolio[0][2]+mnozstvi_nakup), jmeno, nazev_kupovaneho_fondu))
            print(f"Potvrzujeme vaši koupi {mnozstvi}ks cenných papírů fondu {nazev_kupovaneho_fondu}, ve výši {akt_cena_kup_akc}Kč za kus, v celkové hodnotě {round(celkova_cena,4)}Kč.")
        else:
            print("Na tuto transakci nemáte dostatečné finanční prostředky.")
        conn.commit()
    conn.commit()
    conn.close()

#Funkce pro prodej akcií
def prodej_akcii(jmeno):
    conn = sqlite3.connect("C:\\Users\\hovor\\Desktop\\kody\\Investicni_appka\\databaze.db")
    c = conn.cursor()
    if c.execute("SELECT EXISTS(SELECT * FROM portfolio WHERE majitel_portfolia = ? AND celkove_mnozstvi_akcii > 0)",(jmeno,)).fetchall()[0] == (1,):
        prazdne = 0
        stav_uctu = c.execute("SELECT stav_uctu FROM uzivatele WHERE login_uzivatele = ?",(jmeno,)).fetchone()[0]
        pocitadlo = 0
        fond_list = []
        for i in c.execute('SELECT * FROM portfolio WHERE majitel_portfolia = ? AND mnozstvi_akcii > 0',(jmeno,)).fetchall():
            fond_list.append(i[1])
            pocitadlo += 1
            print("Číslo fondu: ",pocitadlo)
            print("Název Fondu: ",i[1])
            print("Množství akcií: ",i[2])
            print("Průměrná cena nákupu: ", round(i[3],4))
            print("Aktuální cena za akcii: ", c.execute("SELECT aktualni_hodnota FROM fondy WHERE nazev_fondu = ?",(i[1],)).fetchall()[0][0])
            zisk = (i[2] * i[3]) - (i[2] * c.execute('SELECT aktualni_hodnota FROM fondy WHERE nazev_fondu = ?',(i[1],)).fetchall()[0][0])
            if zisk > 0:
               print("Zisk: ", round(zisk,4),"Kč\n")
            elif zisk < 0:
                print("Ztráta: ", round(zisk,4),"Kč\n")
            else:
                print("Zisk/ztráta: ",zisk,"Kč\n")
    else:
        print("V tuto chvíli je vaše portfolio prázdné.")
        prazdne = 1
        return

    if prazdne == 0:
        fond = int(input("Vlož číslo fondu kterého akcie chceš odprodat: "))
        mnozstvi = float(input("Zadej množství akcii které chceš odprodat: "))
        nazev_prodavaneho_fondu = fond_list[fond-1]
        akt_cena_kup_akc = c.execute("SELECT aktualni_hodnota FROM fondy WHERE nazev_fondu = ?",(nazev_prodavaneho_fondu,)).fetchall()[0][0]
        vypis_portfolia = c.execute('SELECT * FROM portfolio WHERE majitel_portfolia = ? AND nazev_fondu = ?',(jmeno,nazev_prodavaneho_fondu)).fetchall()
        if c.execute('SELECT * FROM portfolio WHERE majitel_portfolia = ? AND nazev_fondu = ? AND celkove_mnozstvi_akcii > 0',(jmeno,nazev_prodavaneho_fondu)).fetchall()[0][2] >= mnozstvi:
            cena_prodeje = mnozstvi * akt_cena_kup_akc
            stav_uctu += cena_prodeje
            c.execute ('UPDATE uzivatele SET stav_uctu = ? WHERE login_uzivatele = ?',(stav_uctu, jmeno))
            c.execute ('UPDATE portfolio SET mnozstvi_akcii = ?, celkove_mnozstvi_akcii = ? WHERE majitel_portfolia = ? AND nazev_fondu = ?',((vypis_portfolia[0][2] - mnozstvi), (vypis_portfolia[0][5] - mnozstvi), jmeno, nazev_prodavaneho_fondu))
            if (vypis_portfolia[0][2] - mnozstvi) == 0:
                c.execute ('UPDATE portfolio SET prumerna_cena_nakupu = ? WHERE majitel_portfolia = ? AND nazev_fondu = ?',(0, jmeno, nazev_prodavaneho_fondu))
                conn.commit()
            conn.commit()
            print(f"Prodal jste {round(mnozstvi,3)}ks akcií fondu {nazev_prodavaneho_fondu} za {round(cena_prodeje,3)}Kč.")
            conn.close()
        else:
            print("Zadal jste k prodeji větší množství akcií než vlastníte. Operace byla zrušena.")
        
#Funkce zaznamenávající transakce
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

#OPRAVIT ZISK/ZTRÁTU KDYŽ SE NAKUPUJE OD NULY
#PŘIDAT PRODEJE TO HISTORIE TRANSAKCÍ