"""
192 Kalender: Program av Jacob Sundqvist.

Är GUI programmet till min main.py.

Inspiration på struktur: https://youtu.be/X5yyKZpZ4vU?si=iWb-kC68NKVLwWcx
och https://drive.google.com/drive/folders/1BbHk5dr_jAozayhSqX1EQfxvGS0ZAQXB
"""

import tkinter as tk
from tkinter import *
from tkinter import messagebox, simpledialog
from tkcalendar import Calendar
from datetime import *
from GUI_main import Kalender, Aktivitet, läs_in_fil, spara_till_fil, validera_datum, validera_tid



class Kalender_GUI(tk.Tk):
    """
    Klass för att skapa stora fönstret.
    """

    def __init__(self):

        self.filnamn = simpledialog.askstring("Filnamn", "Skriv in filnamn som skall öppnas eller skapas:")                             #https://docs.python.org/3/library/dialog.html

        super().__init__()
        self.title("Kalender")
        self.geometry("550x500")



        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        try:

            self.frame = Inmatning(self, self.filnamn)
            self.frame.grid(row=1, column=0, sticky="nsew")

        except TclError:
            return #

class Inmatning(tk.Frame):
    """
    Hanterar all knappar, kalender och textrutan.
    """

    def __init__(self, parent, fil):
        super().__init__(parent)
        self.kalender = Kalender()
        self.master = parent

        self.listan = self.kalender.aktivitetslista
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)


        self.läs_in()


#Knappar:
        knapp_frame = tk.Frame(self)
        knapp_frame.grid(row=1, column=0, sticky="ew", padx=10)

        self.lägg_till_btn = tk.Button(knapp_frame, text="Lägg till", command=self.lägg_till)
        self.lägg_till_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.ta_bort_btn = tk.Button(knapp_frame, text="Ta bort", command=self.ta_bort)
        self.ta_bort_btn.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.ändra_btn = tk.Button(knapp_frame, text="Ändra", command=self.ändra)
        self.ändra_btn.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.visa_alla_btn = tk.Button(knapp_frame, text="Visa Alla Aktiviteter", command=self.visa_alla)
        self.visa_alla_btn.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        self.visa_månad_btn = tk.Button(knapp_frame, text="Visa Månad", command=self.visa_månad)
        self.visa_månad_btn.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

        self.spara_btn = tk.Button(knapp_frame, text="Spara och avsluta", command=self.spara_knapp)
        self.spara_btn.grid(row=5, column=0, padx=5, pady=5, sticky="ew")

#Testrutor: Hämtade mycket information hur man använder dessa här: https://www.tutorialspoint.com/python/tk_listbox.htm
        self.textruta = tk.Listbox(self, width=50, height=12, font=("Arial", "10"))
        self.textruta.grid(row=1, column=1, columnspan=8, rowspan=8)

#Kalendern som syns
        kalendar_frame = tk.Frame(self)
        kalendar_frame.grid(row=0, column=2, sticky="n", padx=10, pady=10)

        self.visa_nästa_aktivitet_btn = tk.Button(kalendar_frame, text="Nästa", command=lambda:self.bläddra("F"))        #https://docs.google.com/presentation/d/1ux5O0RfUIJxJBXGCtnH4E8UJqIVFfdogSqEx-2NimDo/edit#slide=id.g2b9baf492fd_0_611
        self.visa_nästa_aktivitet_btn.grid(row=2, column=2, padx=5, sticky="news")

        self.visa_tidigare_aktivitet_btn = tk.Button(kalendar_frame, text="Tidigare", command=lambda:self.bläddra("B"))
        self.visa_tidigare_aktivitet_btn.grid(row=2, column=0, padx=5, sticky="news")

        datum = date.today()
        self.kalender_sida = Calendar(kalendar_frame, selectedmode="day", year=datum.year, month=datum.month, day=datum.day, date_pattern="YYYY-MM-DD")
        self.kalender_sida.grid(row=0, column=1, padx=10, pady=10, sticky="news")
        self.kalender_sida.bind("<<CalendarSelected>>", self.välj_datum_på_kalender)                                     #https://tkcalendar.readthedocs.io/en/stable/Calendar.html
                                                                                                                         #bind(), A <<CalendarSelected>> event is generated each time the user selects a day with the mouse.
        self.sök_på_datum = tk.Entry(kalendar_frame, width=10)
        self.sök_på_datum.grid(row=2, column=1, padx=10, sticky="news")
        self.sök_på_datum.insert(0, str(date.today().strftime("%Y-%m-%d")))
        self.sök_på_datum.bind("<Return>", self.uppdatera_kalender_sidan)                                               #Gör så att man kan trycka "enter" och att den hoppar till sökt datum. https://www.geeksforgeeks.org/how-to-bind-the-enter-key-to-a-tkinter-window/


        self.uppdatera_kalender_sidan()


    def läs_in(self):
        """
        bool som hämtar från kalender.läs_in_fil -> om True (felaktigt format) => Felmeddelande.
        Gömmer fönstret och förstör om True.

        :return: # or error message.
        """
        if läs_in_fil(self.master.filnamn, self.kalender) is True:
            self.master.withdraw()                                                                                  #https://www.geeksforgeeks.org/hide-and-unhide-the-window-in-tkinter-python/
            messagebox.showinfo("Filhantering", "Det finns något fel med denna fil")
            self.master.destroy()


    def välj_datum_på_kalender(self, event=None):
        """
        Rensar textrutan -> hämtar datum -> visar sökt datum

        :param event: None (måste ha event för att bind. skall fungera)
        :return: valt datum, datetime.date
        """
        self.textruta.delete(0, tk.END)
        valt_datum = self.visa_specifikt_datum()

        self.sök_på_datum.delete(0, END)
        self.sök_på_datum.insert(0, str(valt_datum))

    def uppdatera_kalender_sidan(self, event=None):
        """
        Rensar textrutan -> uppdaterar textrutan till datum som är inskrivet eller markerat.

        :param event: None (måste ha event för att bind. skall fungera)
        :return:#
        """
        self.textruta.delete(0, tk.END)

        try:

            inskrivet_datum = self.sök_på_datum.get()
            self.kalender_sida.selection_set(inskrivet_datum)
            self.visa_specifikt_datum(inskrivet_datum)

        except ValueError:
            messagebox.showwarning("Format","Inte ett giltigt värde")


    def lägg_till(self):
        """
        Hämtar valt datum (markerat eller sökt) -> öppnar popup fönster för att lägga till aktivitet.

        :return: #
        """
        valt_datum = self.kalender_sida.get_date()
        Popup_fönster(self, "Lägg till aktivitet", valt_datum)

    def ta_bort(self):
        """
        Hittar vald aktivitet som markeras -> tar bort aktivitet från listan och textrutan.

        Om ej vald aktivitet så kommer felmeddelande upp.

        :return: #
        """
        try:
            aktivitet, vald = self.hitta_vald_aktivitet()

            self.listan.index(aktivitet)
            self.listan.remove(aktivitet)
            self.textruta.delete(vald)

        except TclError:
            return messagebox.showerror("Fel", "Vänligen välj aktivitet som skall tas bort!")              #https://www.geeksforgeeks.org/validating-entry-widget-in-python-tkinter/ hämtade messagebox.showerror

    def ändra(self):
        """
        Hittar vald aktivitet som markeras -> öppnar popup fönster med ifyllda fält där aktiviteten ändras.

        Om ej vald aktivitet så kommer felmeddelande upp.

        :return:
        """
        try:
            aktivitet = self.hitta_vald_aktivitet()[0]

            popup = Popup_fönster(self, "Ändra", aktivitet.datum, aktivitet)
            popup.starttid.insert(tk.END, aktivitet.starttid)
            popup.sluttid.insert(tk.END, aktivitet.sluttid)
            popup.aktivitet.insert(tk.END, aktivitet.aktivitet)
            popup.anteckning.insert(tk.END, aktivitet.anteckning)

        except TclError:
            return messagebox.showerror("Fel", "Vänligen välj aktivitet som skall ändras!")

    def hitta_vald_aktivitet(self):
        """
        Får markerad aktivitet -> söker igenom listan och matchar aktiviteten.

        :return: Aktivitet och markerad aktivitet
        """
        vald = self.textruta.curselection()
        aktivitet_på_vald_dag = self.textruta.get(vald)

        for aktivitet in self.listan:
            if aktivitet_på_vald_dag == str(aktivitet):
                return aktivitet, vald


    def visa_alla(self):
        """
        Visar alla aktiviteter i textrutan.

        :return: #
        """
        self.textruta.delete(0, tk.END)
        self.textruta.insert(tk.END, *self.listan)

    def visa_månad(self):
        """
        Hämtar datum -> tillkallar kalender.hitta_månad som ger lista av alla aktiviteter den månaden.

        :return: #
        """
        self.textruta.delete(0, tk.END)
        valt_datum = self.kalender_sida.get_date()
        datumet = datetime.strptime(valt_datum , "%Y-%m-%d")

        self.textruta.insert(tk.END, *self.kalender.hitta_månad(datumet))

    def visa_specifikt_datum(self, valt_datum=None):
        """
        Rensar textrutan -> hämtar datum från kalender.hitta_datum i GUI_main.py

        :param valt_datum: datetime.date()
        :return: valt datum och aktivitet för valt datum
        """
        self.textruta.delete(0,tk.END)

        valt_datum = self.kalender_sida.get_date()
        valt_datum = datetime.strptime(valt_datum, "%Y-%m-%d").date()

        aktivitet_för_datum =  self.kalender.hitta_datum(valt_datum)
        self.textruta.insert(tk.END, *aktivitet_för_datum)

        return valt_datum

    def bläddra(self, framåt_eller_bakåt):
        """
        Hämtar markerat datum och return fån kalender.bläddra -> tittar om resultat är en set eller ej -> Om set
        så går den till nästa datum som hittas i omvandlade och sorterade listan.

        :param framåt_eller_bakåt: str från knapp
        :return: #
        """
        try:
            valt_datum = datetime.strptime(self.kalender_sida.get_date(), "%Y-%m-%d").date()
            resultat = self.kalender.bläddra(framåt_eller_bakåt, valt_datum)

            if isinstance(resultat, set):                                                                               #https://docs.python.org/3.12/library/functions.html#isinstance
                alla_datum = sorted(resultat)

                if framåt_eller_bakåt == "F":
                    nytt_datum = next((d for d in alla_datum if d > valt_datum), None)                                  #https://docs.python.org/3.12/library/functions.html#next, tog hjälp av GTP: https://chatgpt.com/c/67be2aac-5d90-8002-ac44-53c7252e8f5c
                else:
                    nytt_datum = next((d for d in reversed(alla_datum) if d < valt_datum), None)                        # reversed fick från dir(listan)
            else:
                nytt_datum = resultat

            self.textruta.delete(0, tk.END)
            self.kalender_sida.selection_set(nytt_datum.strftime("%Y-%m-%d"))
            self.visa_specifikt_datum(nytt_datum)
            self.välj_datum_på_kalender()

        except Exception as error:
            messagebox.showerror("Fel", "Ett fel har uppstått")
            print(error)

    def spara_knapp(self):
        """
        Kallar på kalender.spara_till_fil som hämtas från GUI_main.py -> avslutar program.

        :return: #
        """

        spara_till_fil(self.master.filnamn, self.kalender)
        self.quit()


class Popup_fönster(tk.Toplevel):
    """
    Fönstret som kommer upp när hanteringen av aktiviteter välj.
    """

    def __init__(self, parent, namn_på_fönster=None, valt_datum=None, vald_aktivitet=None):
        super().__init__(parent)
        self.title(namn_på_fönster)
        self.geometry("300x200")
        self.master = parent

#Text
        self.namn_på_fönster = namn_på_fönster
        self.vald_aktivitet = vald_aktivitet

        self.datum_beskrivning = tk.Label(self, text="Datum: [YYY-MM-DD]")
        self.datum_beskrivning.grid(row=0, column=0, padx=20)

        self.starttid_beskrivning = tk.Label(self, text="Välj starttid [HH:MM]:")
        self.starttid_beskrivning.grid(row=1, column=0, padx=20)

        self.sluttid_beskrivning = tk.Label(self, text="Välj sluttid [HH:MM]:")
        self.sluttid_beskrivning.grid(row=2, column=0, padx=20)

        self.aktivitet_beskrivning = tk.Label(self, text="Aktivitet:")
        self.aktivitet_beskrivning.grid(row=3, column=0, padx=20)

        self.anteckning_beskrivning = tk.Label(self, text="Anteckning:")
        self.anteckning_beskrivning.grid(row=4, column=0, padx=20)

        self.felmeddelande_label = tk.Label(self, fg="red")
        self.felmeddelande_label.grid(row=5, column=0, columnspan=2)

#Entry
        self.datum = tk.Entry(self)
        self.datum.grid(row=0, column=1)
        if valt_datum:
            self.datum.insert(0, valt_datum)

        self.starttid = tk.Entry(self)
        self.starttid.grid(row=1, column=1)

        self.sluttid = tk.Entry(self)
        self.sluttid.grid(row=2, column=1)

        self.aktivitet = tk.Entry(self)
        self.aktivitet.grid(row=3, column=1)

        self.anteckning = tk.Entry(self)
        self.anteckning.grid(row=4, column=1)

#Knappar
        self.spara = tk.Button(self, text=namn_på_fönster, command=self.spara_till_textruta)
        self.spara.grid(row=5, column=1)

#Metoder
    def validera(self, datum_sparas, starttid_sparas, sluttid_sparas):
        """
        Tar in inlagd data -> kallar på kalender.validera_datum och kalender.validera_tid och hanterar resultat.

        :param datum_sparas: datum
        :param starttid_sparas: tid
        :param sluttid_sparas: tid
        :return: True eller False, baserat på validering från GUI_main.py.
        """

        datum = validera_datum(datum_sparas)
        if datum is False:
            messagebox.showerror("Fel", "Ogiltigt datumformat eller datum i det förflutna!")
            return True

        tider = validera_tid(starttid_sparas, sluttid_sparas)
        if tider is False:
            messagebox.showerror("Fel", "Ogiltigt tidsformat")
            return True

        return False

    def lägg_till_popup(self, aktivitet_att_läggas_till):
        """
        Hämtar skapad aktivitet -> kallar på kalender.lägg_till_aktivitet -> Hanterar om den fastnar på överlappa.

        :param aktivitet_att_läggas_till: Aktivitet
        :return: True, dvs om den överlappar.
        """

        if self.master.kalender.lägg_till_aktivitet(aktivitet_att_läggas_till):
            messagebox.showerror("Fel", "Denna överlappar")

            return True

    def ändra_popup(self, vald_aktivitet, ny_aktivitet):
        """
        Hämtar vald aktivitet och ny aktivitet -> kallar på kalender.ändra_aktivitet -> Hanterar om den fastnar på överlappa.

        :param vald_aktivitet: vald aktivitet från listan
        :param ny_aktivitet:  ny aktivitet från inmatning
        :return: True, dvs om den överlappar.
        """

        if self.master.kalender.ändra_aktivitet(vald_aktivitet, ny_aktivitet):
            messagebox.showerror("Fel", "Denna överlappar")

            return True

    def spara_till_textruta(self):
        """
        Hämtar all inmatning -> kallar på validering (stoppar om får True) -> skapar aktivitet ->
        lägger till eller ändrar (stoppar om får True) -> sorterar listan

        :return: #
        """

        datum_sparas = self.datum.get()
        starttid_sparas = self.starttid.get()
        sluttid_sparas = self.sluttid.get()
        aktiviteter_sparas = self.aktivitet.get()
        anteckningar_sparas = self.anteckning.get()

        if self.validera(datum_sparas, starttid_sparas, sluttid_sparas):
            return

        aktivitet = Aktivitet(datum_sparas, starttid_sparas, sluttid_sparas, aktiviteter_sparas, anteckningar_sparas)

        if self.namn_på_fönster == "Lägg till aktivitet":
            if self.lägg_till_popup(aktivitet):
                return

        elif self.namn_på_fönster == "Ändra":
            if self.ändra_popup(self.vald_aktivitet, aktivitet):
                return

        self.master.kalender.sortera()
        self.master.uppdatera_kalender_sidan()

        self.destroy()                                                                                                  #https://discuss.python.org/t/close-main-tkinter-window-with-destroy-error/31097



if __name__ == "__main__":
    app = Kalender_GUI()
    app.mainloop()
