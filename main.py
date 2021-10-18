import databaze
print("""Vítejte v investničním dotazníku MaJa.
Pro registraci nového účtu, napište 1
Pro přihlášení k existujícímu účtu stisněte Enter.
""")
#Uživatel si zvolí zda-li se chce zaregistrovat, nebo přihlásit.
#Pokud se chce zaregistrovat, zadá jméno, a heslo, a pomocí funkce .registrace se zadaná data zapíšou do databáze. 
if input("Zvolte 1 pro registraci, a nebo zmačkněte Enter pro přihlášení: ") == "1":
    login_udaje = (input("Zadejte jméno kterým se budete přihlašovat: "),input("Zadejte heslo pod kterým se budete přihlašovat: "))
    databaze.registrace(login_udaje[0],login_udaje[1])
    print("Gratulujeme, nyní jste zaregistrováni v našem dotazníku. Pro pokračování se přihlašte vámi zadanými údaji.")

#Následně zadá své jméno, a heslo, a přihlásí se do systému. Funkce .login prověří, zda jsou zadané údaje v databázi, a zda jméno, a heslo souhlasí.
while True:
    login_jmeno = input("Zadejte vaše přihlašovací jméno: ")
    login_heslo = input("Zadejte vaše heslo: ")
    if databaze.login(login_jmeno,login_heslo) == False:
        print("Zadal jste špatné jméno nebo heslo.")
        if input("Chcete to zkusit znovu?: (a/n)") == "n":
            break
    else:
        print("Vítejte",login_jmeno,".")
        break

