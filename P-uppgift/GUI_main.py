"""
192 Kalender: Program av Jacob Sundqvist.

Samma som main.py men tagit bort onödig kod för att enklare kunna se och använda.

Fungerar som backend för GUI specifikt. Ändrade vissa format för att passa GUI bättre, så som returns i
lägg_till_aktivitet, ändra_aktivitet (från str -> bool) och __Str__ (bara format på str) under Aktivitet klassen.
Även tagit bort vissa print() från Kalender klassens metoder.
"""

from datetime import*                                                                                                   #https://www.geeksforgeeks.org/python-datetime-module/
import csv                                                                                                              #https://docs.python.org/3/library/csv.html


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
        return self.datum + " | " + " " + self.starttid + " till "+ self.sluttid +  " | " + self.aktivitet + " | " + self.anteckning


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
            return True

        self.aktivitetslista.append(aktivitet_lägg_till)
        return False

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
                    return True

            self.aktivitetslista.append(ny_aktivitet)
            return False

        except ValueError as error:
            return "\nFinns ingen sådan aktivitet i listan\n", error

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
        set_av_datum = {datetime.strptime(aktivitet.datum, "%Y-%m-%d").date() for aktivitet in self.aktivitetslista}  # Skapar ett set av datum för att undvika upprepning av samma datum, denna är i en for-loop vilket matchar datetime mot instanser i aktivitetslistan. Tittade igenom: https://www.geeksforgeeks.org/python-data-structures/
        nuvarande_datum = sorted(list(set_av_datum))                                                                         #Gör om set till lista som är sorterad då .index inte fungerar på set. Sorterad så att datum hamnar i rätt ordning.

        try:

            index = nuvarande_datum.index(valt_datum)                                                                            #Ger index nr på valt datum.

            if byt_datum == "F":
                if index < len(nuvarande_datum)-1:
                    index += 1
                    return nuvarande_datum[index]                                                                                  #retunterar datumet på det index nr.
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

        except ValueError:
            return set_av_datum

    def hitta_datum(self, valt_datum=None):
        """
        Visar alla aktiviteter som finns i listan enligt format. Används även för att visa specifika datum.
        :return: str, och aktivitet.
        """
        try:
            if valt_datum is None:
                return self.aktivitetslista

            else:
                valt_datum_str = str(valt_datum).split(",")[0]                                                              #Säkerställer att det är en sträng och säkerställer att datumet ges.

                aktivitet_på_specifikt_datum = [specifikt_aktivitet for specifikt_aktivitet in self.aktivitetslista if
                                                specifikt_aktivitet.datum == valt_datum_str]                                    #for-loop som hittar och lägger till sökt datum i en lista.

                return aktivitet_på_specifikt_datum

        except ValueError:
            return False

    def hitta_månad(self, vald_år_och_månad):
        """
        Skapar lista av aktiviteter som finns i aktivitetslistan och matchar de valda datetime.

        :param vald_år_och_månad:
        :return:
        """

        aktiviteter_på_månaden = [
            m_aktivitet for m_aktivitet in self.aktivitetslista
            if datetime.strptime(m_aktivitet.datum, "%Y-%m-%d").year == vald_år_och_månad.year
               and datetime.strptime(m_aktivitet.datum, "%Y-%m-%d").month == vald_år_och_månad.month]

        return aktiviteter_på_månaden


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
                    objekt = Aktivitet(rad_delar[0], rad_delar[1], rad_delar[2], rad_delar[3], rad_delar[4] if len(rad_delar) > 4 else "")
                    fillista.lägg_till_aktivitet(objekt)

                    if not validera_datum(objekt.datum, fil) or not validera_tid(objekt.starttid, objekt.sluttid):
                        return True

                return kalender

        else:
            return True

    except Exception as error:
        return error

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


def validera_datum(inmatning, fil=None):
    """
    Undersöker om rätt format enligt datetime -> kontrollerar att den inte hamnar efter dagens datum.
    (Tittar även om den skall validera på fil därmed bortser från datum < date.today())
    :return: str av datum
    """
    try:
        datum = datetime.strptime(inmatning, "%Y-%m-%d").date()
        if fil:
            return True

        elif datum < date.today():
            return False
        else:
            return datum.strftime("%Y-%m-%d")
    except ValueError:
        return False

def validera_tid(starttid, sluttid):
    """
    kontrollerar att rätt format enligt datetime -> kontrollerar att användare kan endast lägga in rimliga tider.

    :return: str av tider.
    """
    try:
        starttid = datetime.strptime(starttid, "%H:%M").time()
        sluttid = datetime.strptime(sluttid, "%H:%M").time()

        if starttid < time(0, 0) or starttid > time(23, 59):
            return False
        elif sluttid < time(0, 0) or sluttid > time(23, 59):
            return False
        elif sluttid < starttid:
            return False
        else:
            return starttid.strftime("%H:%M"), sluttid.strftime("%H:%M")

    except ValueError:
        return False


