import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkcalendar import DateEntry
from tkinter import messagebox
from datetime import date
from routes import routes
from alias import alias
from get_n_plot_prices import get_prices
from PIL import Image, ImageTk
from time import sleep
import babel.numbers


def validate_input(new_text):
    if new_text.isdigit() or new_text == "":
        return True
    else:
        return False


# noinspection PyUnusedLocal
def execute_get_prices(finestra_secondaria, selected_airport_from, selected_airport_to, selected_dates,
                       selected_n_of_persons):
    get_prices(alias[selected_airport_from], alias[selected_airport_to], selected_dates, selected_n_of_persons)
    finestra_secondaria.destroy()  # Distruggi la finestra secondaria dopo l'esecuzione di get_prices


class Home(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ryanair Flight Prices")
        self.iconbitmap("icon.ico")

        # window sizes and position
        window_width = 700
        window_height = 520
        x_position = (self.winfo_screenwidth() - window_width) // 2
        y_position = (self.winfo_screenheight() - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # frame
        self.frame_gui = tk.Frame(self, padx=40, pady=30, bg="#073693")
        self.resizable(False, False)
        self.frame_gui.pack()

        # header
        image = Image.open("header.png")
        photo = ImageTk.PhotoImage(image)
        header_label = tk.Label(self.frame_gui, image=photo, borderwidth=0)
        header_label.image = photo
        header_label.grid(row=0, column=0, columnspan=3, pady=30)

        # Airport from
        self.label_1 = tk.Label(self.frame_gui, text="Aeroporto di partenza:", font=("Arial", 12), bg="#073693",
                                fg="white")
        self.label_1.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        airport_from = list(routes)
        self.var_1 = tk.StringVar(value=airport_from[184])
        self.menu_airport_from = ttk.Combobox(self.frame_gui, values=airport_from, textvariable=self.var_1, state="readonly",
                                              font=("Arial", 12), width=30)
        self.menu_airport_from.grid(row=1, column=1, padx=10, pady=10)

        # Airport to
        self.label_2 = tk.Label(self.frame_gui, text="Aeroporto di arrivo:", font=("Arial", 12), bg="#073693", fg="white")
        self.label_2.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.airport_to = routes
        self.var_2 = tk.StringVar(value=self.airport_to[airport_from[24]])
        self.menu_airport_to = ttk.Combobox(self.frame_gui, state="readonly", font=("Arial", 12), width=30)
        self.menu_airport_to.grid(row=2, column=1, padx=10, pady=10)
        # callback to update airport to menu
        self.menu_airport_from.bind("<<ComboboxSelected>>", self.update_airport_to_menu)
        self.update_airport_to_menu(None)

        self.selected_dates = []
        # Calendar
        self.label_calendar = tk.Label(self.frame_gui, text="Date:", font=("Arial", 12), bg="#073693", fg="white")
        self.label_calendar.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.calendar = DateEntry(self.frame_gui, width=30, background="#cdab2a", foreground="#073693", borderwidth=2,
                                  date_pattern="yyyy-mm-dd", state="readonly", font=("Arial", 12))
        self.calendar.grid(row=3, column=1, padx=10, pady=10)

        # Add date button
        self.add_date_button = tk.Button(self.frame_gui, text="Aggiungi data", command=self.add_date, font=("Arial", 12),
                                         bg="#cdab2a", fg="#073693", relief=tk.FLAT)
        self.add_date_button.grid(row=3, column=2, padx=10, pady=10)

        # Selected dates list
        self.label_selected_dates = tk.Label(self.frame_gui, text="Date selezionate:", font=("Arial", 12), bg="#073693",
                                             fg="white")
        self.label_selected_dates.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.scrollbar = Scrollbar(self.frame_gui, orient=VERTICAL)
        self.dates_list = Listbox(self.frame_gui, width=30, height=5, font=("Arial", 12), borderwidth=2,
                                  yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.dates_list.yview)
        self.dates_list.grid(row=4, column=1, padx=10, pady=10, columnspan=1, sticky="nsw")
        self.scrollbar.grid(row=4, column=1, padx=10, pady=10, sticky="nse")

        # Delete date button
        self.delete_date_button = tk.Button(self.frame_gui, text="Cancella data", command=self.delete_date,
                                            font=("Arial", 12), state="disabled", bg="#8c061e", fg="white", relief=tk.FLAT)
        self.delete_date_button.grid(row=4, column=2, columnspan=3, padx=10, pady=10)
        self.bind("<Delete>", self.delete_date_wrapper)

        # Label number of persons
        self.label_number_of_persons = tk.Label(self.frame_gui, text="Numero di persone:", font=("Arial", 12),
                                                bg="#073693", fg="white")
        self.label_number_of_persons.grid(row=5, column=0, padx=10, pady=10, sticky="e")

        # Spinbox for number of persons
        self.number_of_persons_spinbox = tk.Spinbox(self.frame_gui, from_=1, to=25, font=("Arial", 12), width=31)
        self.number_of_persons_spinbox.grid(row=5, column=1, padx=10, pady=10, sticky="ns")
        self.number_of_persons_spinbox.delete(0, tk.END)
        self.number_of_persons_spinbox.insert(0, "1")
        self.number_of_persons_spinbox.bind("<KeyRelease>", self.validate_spinbox_input)

        # Aggiungi qui altre parti del codice...

        # Look for prices button
        self.look_for_prices = tk.Button(self.frame_gui, text="Cerca prezzi", command=self.look_for_prices,
                                         font=("Arial", 12), bg="#cdab2a", fg="#073693", relief=tk.FLAT)
        self.look_for_prices.grid(row=6, columnspan=3, padx=10, pady=30)

    def validate_spinbox_input(self, event):
        new_value = self.number_of_persons_spinbox.get()
        if new_value.isdigit():
            new_value = int(new_value)
            if new_value < 1:
                self.number_of_persons_spinbox.delete(0, tk.END)
                self.number_of_persons_spinbox.insert(0, "1")
            elif new_value > 25:
                self.number_of_persons_spinbox.delete(0, tk.END)
                self.number_of_persons_spinbox.insert(0, "25")
        else:
            self.number_of_persons_spinbox.delete(0, tk.END)

    def update_airport_to_menu(self, event):
        new_airport_from = self.var_1.get()
        self.menu_airport_to.config(values=self.airport_to[new_airport_from])

        self.var_2.set("")
        self.menu_airport_to.set("")

    def add_date(self):
        # Gain selected date
        selected_date = self.calendar.get_date()

        if selected_date < date.today():
            messagebox.showwarning("Data non valida", "Non puoi viaggiare indietro nel tempo!")
            return

        selected_date = selected_date.strftime("%Y-%m-%d")

        if selected_date not in self.selected_dates:
            self.selected_dates.append(selected_date)
            self.selected_dates.sort()
            # Abilitate delete date button
            self.delete_date_button.config(state="normal")
            self.update_date_list()
        else:
            messagebox.showwarning("Data già presente", "La data selezionata è già stata aggiunta.")

    def update_date_list(self):
        # Delete list
        self.dates_list.delete(0, tk.END)

        # Add updated dates
        for data in self.selected_dates:
            self.dates_list.insert(tk.END, data)

    def delete_date(self):
        selected_date_to_delete = self.dates_list.curselection()
        if selected_date_to_delete:
            selected_date_to_delete = selected_date_to_delete[0]
            date_to_remove = self.dates_list.get(selected_date_to_delete)

            if date_to_remove in self.selected_dates:
                self.selected_dates.remove(date_to_remove)
                self.update_date_list()

                # If date list empty -> disable delete date button
                if not self.selected_dates:
                    self.delete_date_button.config(state="disabled")
            else:
                messagebox.showwarning("Data non trovata", "La data selezionata non è presente nella lista.")

    def delete_date_wrapper(self, event):
        self.delete_date()

    def look_for_prices(self):
        selected_airport_from = self.menu_airport_from.get()
        selected_airport_to = self.menu_airport_to.get()
        selected_dates = self.selected_dates

        # Validating inputs
        if not selected_airport_to:
            messagebox.showerror("Errore", "Non hai selezionato un aeroporto di arrivo.")
            return

        if not selected_dates:
            messagebox.showerror("Errore", "Il campo delle date selezionate non può essere vuoto.")
            return

        selected_n_of_persons = self.number_of_persons_spinbox.get()
        if not selected_n_of_persons:
            messagebox.showerror("Errore", "Il campo del numero di persone non può essere vuoto.")
            return

        searching_window = tk.Toplevel(self)
        searching_window.title("Ricercando prezzi...")
        searching_window.iconbitmap("icon.ico")
        searching_window.resizable(False, False)

        # window sizes and position
        window_width = 350
        window_height = 260
        x_position = (searching_window.winfo_screenwidth() - window_width) // 2
        y_position = (searching_window.winfo_screenheight() - window_height) // 2
        searching_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        # Aggiungi altri widget o contenuti alla finestra secondaria
        label = tk.Label(searching_window, text="Questa è la finestra secondaria")
        label.pack(padx=10, pady=10)

        # Aggiorna la GUI prima di continuare con l'esecuzione
        self.update()

        # Esegui la funzione get_prices dopo 1 millisecondo
        searching_window.after(1, lambda: execute_get_prices(searching_window, selected_airport_from,
                                                                     selected_airport_to, selected_dates,
                                                                     selected_n_of_persons))