"""
192 Kalender: Program av Jacob Sundqvist.

Programmet skapar en kalender, antingen från att läsa in befintligt CSV fil eller från att välja att skapa en ny.
Därefter kan användaren lägga in, ändra eller ta bort aktiviteter och även kunna se dessa på specifika datum eller
få en överblick av alla.

Datum för redovisning: 2025-02-26

GUI finns ej med på denna fil.
"""


from calendar import*
from datetime import*                                                                                                   #https://www.geeksforgeeks.org/python-datetime-module/
import csv                                                                                                              #https://docs.python.org/3/library/csv.html

#Klasserna
class Aktivitet:
    """
    Klass hanterar format för aktivitetsinstanserna och även jämför mellan dessa instanser.
    Attributes: datum, tid, aktivitet, anteckning.
    """

    def __init__(self, datum, starttid, sluttid, aktivitet, anteckning = " "):
        """
        :param datum: YYYY-MM-DD
        :param tid: float av start och sluttider
        :param aktivitet: Sträng, title
        :param anteckning: Sträng, anteckning
        """
        self.datum = datum
        self.starttid = starttid
        self.sluttid = sluttid
        self.aktivitet = aktivitet
        self.anteckning = anteckning


    def __str__(self):
        """
        :return: datum, tid, aktivitet, anteckning
        """
        aktivitet_format = "Datum: " + self.datum + "\n" + \
                           "Starttid: " + self.starttid + "\n" + \
                           "Sluttid: " + self.sluttid + "\n" + \
                           "Händelse: " + self.aktivitet + "\n" + \
                           "Anteckning: " + self.anteckning + "\n" + \
                           "_" * 62
        return aktivitet_format

    def __lt__(self, other):                                                                                            #Används för att sortera listan i Kalender, detta då kalenderns lista består av Aktivitet instanser.
        """
        Jämför Aktivitetsinstanser som sedan sorteras i Kalender klassen.
        :param other:
        :return: True or False
        """
        if self.datum < other.datum:
            return True
        elif self.datum == other.datum:
            if self.starttid < other.starttid and self.sluttid < other.sluttid:
                return True
            else:
                return False
        else:
            return False

    def __eq__(self, other):
        """
        Typkontrollerar så att formatet är korrekt. Används senare för att identifiera Aktivitets-instans som skall
        tas bort eller ändras i Kalender-klassen.
        :param other:
        :return: False, eller True (att de är lika)
        """
        if isinstance(other, Aktivitet):                                                                                #https://www.geeksforgeeks.org/python-isinstance-method/

            return (self.datum == other.datum and self.starttid == other.starttid and self.sluttid == other.sluttid
                    and self.aktivitet == other.aktivitet)
        else:
            return False

class Kalender:
    """
    Klass som hanterar alla operationer relaterade till kalendern, som att lägga in, ta bort, ändra aktiviteter, samt söka
    och bläddra mellan dessa.
    Attributes: aktivitetslista: Lista med aktiviteter, eller tom.
    """

    def __init__(self, aktivitetslista=None):
        """
        Skapar en tom lista om de inte redan hämtas från fil.
        :param aktivitetslista: Lista av aktiviteter
        """
        if aktivitetslista is None:
            self.aktivitetslista = []
        else:
            self.aktivitetslista = aktivitetslista

    def __str__(self):
        """
        :return: aktivitetslista
        """
        for aktivitet in self.aktivitetslista:
            return aktivitet

    def lägg_till_aktivitet(self, aktivitet_lägg_till):
        """
        Kollar om överlappning sker -> (om nej) lägger till i aktivitetslistan

        :param aktivitet_lägg_till: str av aktivitet = Aktivitet(datum, starttid, sluttid, händelse, anteckning)
        :return: str meddelande
        """
        if self.överlappa_kontroll(aktivitet_lägg_till.datum, aktivitet_lägg_till.starttid, aktivitet_lägg_till.sluttid):
            return "\nDenna aktivitet överlappar med en befintlig. Försök igen.\n"
        self.aktivitetslista.append(aktivitet_lägg_till)
        return "\n" + "_" * 10 + "Tillagd" + "_" * 10 + "\n"

    def ta_bort_aktivitet(self, aktivitet_ta_bort):
        """
        Hittar aktivitet -> tar bort den ut listan

        :param aktivitet_ta_bort: str av aktivitet = Aktivitet(datum, starttid, sluttid, händelse, anteckning)
        :return: str meddelande
        """
        if aktivitet_ta_bort in self.aktivitetslista:
            self.aktivitetslista.remove(aktivitet_ta_bort)
            return "\n" + "_" * 10 + "Borttagen" + "_" * 10 + "\n"
        else:
            return "\nFinns ingen sådan i listan\n"

    def ändra_aktivitet(self, vald_aktivitet, ny_aktivitet):
        """
        Tittar om aktivitet finns i listan -> matchar aktivitet och tar bort -> om överlappa (lägg till gammal) ->
        lägg till ny

        :param vald_aktivitet: str av aktivitet = Aktivitet(datum, starttid, sluttid, händelse, anteckning)
        :param ny_aktivitet: str av aktivitet = Aktivitet(datum, starttid, sluttid, händelse, anteckning)
        :return: ValueError eller str meddelanden
        """
        try:
            index = self.aktivitetslista.index(vald_aktivitet)                                                          #Hittar vilket index aktiviteten befinner på och om den finns i listan.
            if index is None:
                return ValueError

            else:
                for alla_aktivitet in self.aktivitetslista:
                    if alla_aktivitet == vald_aktivitet:
                        self.aktivitetslista.remove(vald_aktivitet)
                        break

                if self.överlappa_kontroll(ny_aktivitet.datum, ny_aktivitet.starttid, ny_aktivitet.sluttid):
                    self.aktivitetslista.append(vald_aktivitet)
                    return "\nDenna aktivitet överlappar med en befintlig. Försök igen.\n"

            self.aktivitetslista.append(ny_aktivitet)
            return "\n" + "_" * 10 + "Uppdaterad" + "_" * 10 + "\n"

        except ValueError:
            return "\nFinns ingen sådan aktivitet i listan\n"

    def sortera(self):
        """
        Sorterar listan efter datum, och därefter tid. Använder sig av __lt__ och __eq__ under Aktivitet-klassen.
        :return: #
        """
        self.aktivitetslista.sort()

    def överlappa_kontroll(self, datum, starttid, sluttid):
        """
        Inför vilka aktiviteter som är befintliga -> kontrollerar om de finns reda aktivitet på datum sedan tid.

        :param datum:
        :param starttid:
        :param sluttid:
        :return: str
        """
        for aktivitet in self.aktivitetslista:
            befintlig_starttid = aktivitet.starttid
            befintlig_sluttid = aktivitet.sluttid
            befintlig_datum = aktivitet.datum

            if  befintlig_datum == datum:
                kontroll = (befintlig_starttid <= starttid <= befintlig_sluttid or befintlig_starttid <= sluttid <= befintlig_sluttid
                            or starttid <= befintlig_starttid and sluttid >= befintlig_sluttid)
                if kontroll:
                    return True

    def bläddra(self, byt_datum, valt_datum):
        """
       Skapar ett set av datetime(aktivitet) som sedan omvandlas till lista och sorteras -> indexerar valt datum ->
        ger alternativ för att minsta eller öka index nr.

        :param valt_datum: str av datum
        :param byt_datum: F eller B
        :return: str av datum på index nr.
        """
        try:
            set_av_datum = {datetime.strptime(aktivitet.datum, "%Y-%m-%d").date() for aktivitet in self.aktivitetslista}  #Skapar ett set av datum för att undvika upprepning av samma datum, denna är i en for-loop vilket matchar datetime mot instanser i aktivitetslistan
            nuvarande_datum = sorted(list(set_av_datum))                                                                         #Gör om set till lista som är sorterad då .index inte fungerar på set. Sorterad så att datum hamnar i rätt ordning.

            index = nuvarande_datum.index(valt_datum)                                                                   #Ger index nr på valt datum.

            if byt_datum == "F":
                if index < len(nuvarande_datum)-1:
                    index += 1
                    return nuvarande_datum[index]                                                                       #retunterar datumet på det index nr.
                else:
                    print("\nNotera att detta är den sista!\n")
                    return nuvarande_datum[-1]

            elif byt_datum == "B":
                if index > 0:
                    index -= 1
                    return nuvarande_datum[index]
                else:
                    print("\nNotera att detta är den första!\n")
                    return nuvarande_datum[0]

        except ValueError as error:
            return error

    def hitta_datum(self, valt_datum=None):
        """
        Visar alla aktiviteter som finns i listan enligt format. Används även för att visa specifika datum.

        :return: str, och aktivitet.
        """
        try:
            if valt_datum is None:
                print("_" * 20, "Alla händelser vissas", "_" * 20)
                return self.aktivitetslista

            else:
                valt_datum_str = str(valt_datum).split(",")[0]                                                              #Säkerställer att det är en sträng och säkerställer att datumet ges.
                print("_" * 20, valt_datum_str ,"_" * 20)
                aktivitet_på_specifikt_datum = [specifikt_aktivitet for specifikt_aktivitet in self.aktivitetslista if
                                                specifikt_aktivitet.datum == valt_datum_str]                                    #for-loop som hittar och lägger till sökt datum i en lista.

                return aktivitet_på_specifikt_datum
        except ValueError:
            return False

    def hitta_månad(self, vald_år_och_månad):
        """
        Skapar lista av aktiviteter som finns i aktivitetslistan och matchar de valda datetime.

        :param vald_år_och_månad: datetime
        :return: lista
        """
        print("_" * 20, "Månad vissas", "_" * 20)

        aktiviteter_på_månaden = [
            m_aktivitet for m_aktivitet in self.aktivitetslista
            if datetime.strptime(m_aktivitet.datum, "%Y-%m-%d").year == vald_år_och_månad.year
               and datetime.strptime(m_aktivitet.datum, "%Y-%m-%d").month == vald_år_och_månad.month]

        return aktiviteter_på_månaden


#Filhanteringen
def läs_in_fil(filnamn, kalender):                                                                                       #https://docs.python.org/3/library/csv.html#csv.reader Hämtade struktur för csv filhantering här
    """
    Läser in fil. Om ingen fil hittas så skapas en tom lista i Kalender-klassen.
    :param filnamn: fil
    :param kalender: Kalender-klass
    :return:
    """
    try:
        if filnamn and filnamn.strip():

            with open(filnamn, newline="", encoding="utf-8") as fil:
                läsare = csv.reader(fil, delimiter=",", quotechar="|")
                fillista = kalender
                for rad_delar in läsare:
                    objekt = Aktivitet(rad_delar[0], rad_delar[1], rad_delar[2], rad_delar[3], rad_delar[4] if len(rad_delar) > 4 else "")     #Hantera om kan skriver in "," eller ":" osv.
                    fillista.lägg_till_aktivitet(objekt)

                    if not validera_datum(objekt.datum, fil) or not validera_tid(objekt.starttid, objekt.sluttid):
                        return True

                return kalender

        else:
            print("Du försökte öppna eller skapa en fil utan namn. Detta går ej. Gör om gör rätt")
            return True

    except Exception:
        return "Filen kunde ej hittas, titta igenom format och eller skapa en ny fil"

def spara_till_fil(filnamn, kalender):
    """
    Sparar ändringar till fil. Sker i slutet av programmet när de aktivt avslutas.
    :param filnamn: Fil
    :param kalender: Kalender-klass (lista)
    :return:
    """
    try:
        with open(filnamn, "w", newline="", encoding="utf-8") as fil:
            writer = csv.writer(fil, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
            for aktivitet in kalender.aktivitetslista:
                rad = [aktivitet.datum, aktivitet.starttid, aktivitet.sluttid, aktivitet.aktivitet, aktivitet.anteckning]
                writer.writerow(rad)
        return "="*26+ "Detta program har avslutats"+"="*26

    except Exception as error:
        return "\nDet uppstod ett fel, vänligen kika igenom och försök igen", error


#Funktionerna
def validera_datum(inmatning, fil=None):
    """
    Undersöker om rätt format enligt datetime -> kontrollerar att den inte hamnar efter dagens datum.
    (Tittar även om den skall validera på fil därmed bortser från datum < date.today())

    :return: str av datum eller False om ogiltigt.
    """
    try:
        datum = datetime.strptime(inmatning, "%Y-%m-%d").date()
        if fil:
            return True

        elif datum < date.today():
            print("\nFel: Datumet kan inte vara i det förflutna. Försök igen.\n")
            return False
        else:
            return datum.strftime("%Y-%m-%d")
    except ValueError:
        print("\nFelaktig datum, försök igen enligt format\n")
        return False

def validera_tid(starttid, sluttid):
    """
    kontrollerar att rätt format enligt datetime -> kontrollerar att användare kan endast lägga in rimliga tider.

    :return: Tuple med start- och sluttid i strängformat eller False vid fel.
    """
    try:
        starttid = datetime.strptime(starttid, "%H:%M").time()
        sluttid = datetime.strptime(sluttid, "%H:%M").time()

        if starttid < time(0, 0) or starttid > time(23, 59):
            print("Felaktig starttid\n")
            return False

        elif sluttid < time(0, 0) or sluttid > time(23, 59):
            print("Felaktig sluttid\n")
            return False

        elif sluttid < starttid:
            print("\nSluttid måste vara senare än starttid, vänligen försök igen\n")
            return False

        else:
            return starttid.strftime("%H:%M"), sluttid.strftime("%H:%M")

    except ValueError:
        print("\nFelaktiga tider, försök igen enligt format\n")
        return False

def input_data():
    """
    Ber om input för datum / tider -> kallar på validering

    :return: datum, starttid, sluttid, händelse, anteckning
    """
    print("Vänligen skriv in följande information\n")

    while True:
        datum = input("Välj datum [YYYY-MM-DD]: ")
        datum_validering = validera_datum(datum)
        if datum_validering:
            break

    while True:
        starttid = input("Välj starttid [HH:MM]: ")
        sluttid = input("Välj sluttid [HH:MM]: ")
        tider_validering = validera_tid(starttid, sluttid)
        if tider_validering:
            starttid, sluttid = tider_validering
            break

    händelse = input("Välj aktivitet: ")
    anteckning = input("Anteckning: ")


    return datum, starttid, sluttid, händelse, anteckning

def hantera_undermeny_val(kalender, undermeny_val):
    """
    Kallar på input() och skapar aktivitet -> ger alternativ och kallar på respektive. 
    
    :param kalender: listan
    :param undermeny_val: int 
    :return: None
    """""
    datum, starttid, sluttid, händelse, anteckning = input_data()
    aktivitet = Aktivitet(datum, starttid, sluttid, händelse, anteckning)

    if undermeny_val == "1":
        lägger_till_aktivitet = kalender.lägg_till_aktivitet(aktivitet)
        print(lägger_till_aktivitet)

    elif undermeny_val == "2":
        tar_bort_aktivitet = kalender.ta_bort_aktivitet(aktivitet)
        print(tar_bort_aktivitet)

    elif undermeny_val == "3":
        print("\nUppge de nya uppgifterna")

        ny_datum, ny_starttid, ny_sluttid, ny_händelse, ny_anteckning = input_data()
        ny_aktivitet = Aktivitet(ny_datum, ny_starttid, ny_sluttid, ny_händelse, ny_anteckning)

        uppdaterar_aktivitet = kalender.ändra_aktivitet(aktivitet, ny_aktivitet)
        print(uppdaterar_aktivitet)

def bläddra_i_kalender(kalender, valt_datum):
    """
    Ber om användare input -> kallar på bläddra och visar aktivitet.

    :param valt_datum: hämtar det inmatande datum.
    :param kalender: kalender-klass
    :return:None
    """

    while True:
        byt_datum = input("\nByt datum [F (fram i tiden), B (bakåt i tiden), T (Tillbaka)]: \n").upper()

        if not byt_datum in ["F" , "B" , "T"]:                                                                          #Felhanterar så att man inte kan lägga in något annat än de i listan.
            print("Fel, vänligen välj de möjligheter som finns")
            continue

        elif byt_datum == "T":
            print()
            break

        valt_datum = kalender.bläddra(byt_datum, valt_datum)
        aktivitets_listan = kalender.hitta_datum(valt_datum)
        print(*aktivitets_listan, sep="\n")

def hantera_visa_händelser(kalender, val=None):
    """
    Hanterar input / val av användaren -> validerar att inmatning är korrekt format -> kallar på respektive metod.

    :param val:
    :param kalender: klassen
    :return: None
    """
    try:
        if val =="1":
            aktivitets_listan = kalender.hitta_datum()
            print(*aktivitets_listan, sep="\n")                                                                         #Fick detta format från GTP: https://chatgpt.com/c/67ba778f-1d3c-8002-898a-2dcbfb9de730

        elif val == "2":
            välj_år_och_månad = input("Välj år och månad [YYYY-MM]: \n")
            välj_år_och_månad = datetime.strptime(välj_år_och_månad , "%Y-%m").date()
            aktivitets_listan = kalender.hitta_månad(välj_år_och_månad)
            print(*aktivitets_listan, sep="\n")

        else:
            välj_datum = input("Välj ett datum [YYYY-MM-DD]: ")
            välj_datum = datetime.strptime(välj_datum, "%Y-%m-%d").date()
            aktivitets_listan = kalender.hitta_datum(välj_datum)

            if not aktivitets_listan:
                print(" Inga sådan händelser hittades för", välj_datum, "\n")

            else:
                print(*aktivitets_listan, sep="\n")
                bläddra_i_kalender(kalender, välj_datum)

    except ValueError as error:
        print("\nVänligen fyll i efterfrågan information i korrekt format!", "\nFelmeddelande: ", error, "\n")


#Menyerna
def hantera_händelser_undermeny(kalender):
    """
    Undermeny till "hantera kalender"
    :param kalender: lista
    :return: sträng av text.
    """
    undermeny_alternativ = """\n1: Lägg till ny aktivitet\n2: Ta bort aktivitet\n3: Ändra befintlig aktivitet\n Tillbaka till huvudmenyn tryck T\n"""
    while True:
        try:
            print(undermeny_alternativ)

            undermeny_val = input("Vad vill du göra? ").upper()

            if undermeny_val == "1":
                hantera_undermeny_val(kalender, undermeny_val)

            elif undermeny_val == "2":
                hantera_undermeny_val(kalender, undermeny_val)

            elif undermeny_val == "3":
                hantera_undermeny_val(kalender, undermeny_val)

            elif undermeny_val == "T":
                print()
                return None

        except ValueError as error:
            print("Vänligen fyll i allt enligt format", "\nFelmeddelande: ", error)

def visa_händelser_menyn(kalender):
    """
    Undermeny för att visa händelser.
    :param kalender:
    :return:
    """
    visa_händelser_meny = """\n1: Vissa Alla. \n2: Visa Månad\n3: Visa Specifikt Datum\nTryck T för att går tillbaka\n"""
    while True:
        try:
            print(visa_händelser_meny)

            visa_händelser_val = input("Vad vill du göra? ").upper()

            if visa_händelser_val == "1":
                kalender.sortera()
                hantera_visa_händelser(kalender, visa_händelser_val)
                print()

            elif visa_händelser_val == "2":
                hantera_visa_händelser(kalender, visa_händelser_val)

            elif visa_händelser_val == "3":
                hantera_visa_händelser(kalender)

            elif visa_händelser_val == "T":
                print()
                return None

        except ValueError as error:
            return error

def huvudmeny():
    """
    1. Visa alla aktiviteter
    2. Hantera kalender
        a. Lägg till ny aktivitet
        b. Ta bort aktivitet
        c. Ändra befintlig aktivitet
    3. Visa datum
    4. Avsluta

    :return:
    """
    kalender_i_terminalen()
    kalender = Kalender()

    filnamn = input("Ge namn på fil som skall läsas in elle på den som skall skapas: ")
    if läs_in_fil(filnamn, kalender) is True:
        return



    while True:
        print("_" * 20, "Huvudmenyn", "_" * 20)

        if not kalender.aktivitetslista:
            print("Ingen nuvarande händelse finns. Skapa en eller läs in fil med format "
                  "[YYYY-MM-DD, HH:MM, HH:MM, Aktivitet, Anteckning]. Lägg till en händelse\n")

            hantera_undermeny_val(kalender, undermeny_val="1") #Tvingar användaren att skapa en aktivitet innan de andra alternativen kommer fram.

        elif kalender.aktivitetslista:
            meny = """1: Vissa händelser. \n2: Hantera kalender\n3: Spara och Avsluta\n"""
            print(meny)

            huvudmeny_val = input("Vad vill du göra? ")

            if huvudmeny_val == "1":
                visa_händelser_menyn(kalender)

            elif huvudmeny_val == "2":
                hantera_händelser_undermeny(kalender)

            elif huvudmeny_val == "3":
                print(spara_till_fil(filnamn, kalender))
                break

        else:
            print("\nFörsök igen\n")



def kalender_i_terminalen():
    """
    Redovisar kalendern och dagens datum i terminal, inget större funktion utan att det ser bra ut. .
    :return: None
    """
    print("="*26, "Kalender","="*26)
    datum_nu = date.today()
    cal = month(datum_nu.year, datum_nu.month)
    print(cal)
    print("_" * 62)
    print("Dagens datum: ", datum_nu)
    print("Dagens tid: ", datetime.now().strftime("%H:%M"))
    print("_"*62, "\n")
    return None

huvudmeny()

