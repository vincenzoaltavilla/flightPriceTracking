import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkcalendar import DateEntry
from tkinter import messagebox
from datetime import date
from routes import *
from PIL import Image, ImageTk


def validate_input(new_text):
    if new_text.isdigit() or new_text == "":
        return True
    else:
        return False


class Home(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ryanair Flight Prices")
        self.iconbitmap("icon.ico")

        self.selected_dates = []

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
                                fg = "white")
        self.label_1.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        airport_from = list(routes)
        self.var_1 = tk.StringVar(value=airport_from[24])
        self.menu_airport_from = ttk.Combobox(self.frame_gui, values=airport_from, textvariable=self.var_1, state="readonly",
                                              font=("Arial", 12), width=30)
        self.menu_airport_from.grid(row=1, column=1, padx=10, pady=10)

        # Airport to
        self.label_2 = tk.Label(self.frame_gui, text="Aeroporto di arrivo:", font=("Arial", 12), bg="#073693", fg = "white")
        self.label_2.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.airport_to = routes
        self.var_2 = tk.StringVar(value=self.airport_to[airport_from[24]])
        self.menu_airport_to = ttk.Combobox(self.frame_gui, state="readonly", font=("Arial", 12), width=30)
        self.menu_airport_to.grid(row=2, column=1, padx=10, pady=10)
        # callback to update airport to menu
        self.menu_airport_from.bind("<<ComboboxSelected>>", self.update_airport_to_menu)
        self.update_airport_to_menu(None)

        # Calendar
        self.label_calendar = tk.Label(self.frame_gui, text="Date:", font=("Arial", 12), bg="#073693", fg = "white")
        self.label_calendar.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.calendar = DateEntry(self.frame_gui, width=30, background="#4080FF", foreground="white", borderwidth=2,
                                  date_pattern="yyyy-mm-dd", state="readonly", font=("Arial", 12))
        self.calendar.grid(row=3, column=1, padx=10, pady=10)

        # Add date button
        self.add_date_button = tk.Button(self.frame_gui, text="Aggiungi data", command=self.add_date, font=("Arial", 12),
                                         bg="#cdab2a", fg="#073693", relief=tk.FLAT)
        self.add_date_button.grid(row=3, column=2, padx=10, pady=10)

        # Selected dates list
        self.label_selected_dates = tk.Label(self.frame_gui, text="Date selezionate:", font=("Arial", 12), bg = "#073693",
                                             fg = "white")
        self.label_selected_dates.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.scrollbar = Scrollbar(self.frame_gui, orient=VERTICAL)
        self.dates_list = Listbox(self.frame_gui, width=30, height=5, font=("Arial", 12), borderwidth=2,
                                  yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.dates_list.yview)
        self.dates_list.grid(row=4, column=1, padx=10, pady=10, columnspan=1, sticky="nsw")
        self.scrollbar.grid(row=4, column=1, padx=10, pady=10,  sticky="nse")

        # Delete date button
        self.delete_date_button = tk.Button(self.frame_gui, text="Cancella data", command=self.delete_date,
                                            font=("Arial", 12), state="disabled", bg="#8c061e", fg="white", relief=tk.FLAT)
        self.delete_date_button.grid(row=4, column=2, columnspan=3, padx=10, pady=10)

        # Label number of persons
        self.label_number_of_persons = tk.Label(self.frame_gui, text="Numero di persone:", font=("Arial", 12),
                                                bg = "#073693", fg = "white")
        self.label_number_of_persons.grid(row=5, column=0, padx=10, pady=10, sticky="e")

        # Number of persons field
        self.number_of_persons_field = tk.Entry(self.frame_gui, width=32, font=("Arial", 12), borderwidth=2)
        self.number_of_persons_field.grid(row=5, column=1, padx=10, pady=10)
        self.number_of_persons_field.insert(0, "1")  # default
        self.number_of_persons_field.config(validate="key", validatecommand=(
            self.number_of_persons_field.register(validate_input), "%P"))

        # Look for prices button
        self.look_for_prices = tk.Button(self.frame_gui, text="Cerca prezzi", command=self.look_for_prices,
                                         font=("Arial", 12), bg="#cdab2a", fg="#073693", relief=tk.FLAT)
        self.look_for_prices.grid(row=6, columnspan=3, padx=10, pady=30)

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

        selected_n_of_persons = self.number_of_persons_field.get()
        if not selected_n_of_persons:
            messagebox.showerror("Errore", "Il campo del numero di persone non può essere vuoto.")
            return

        if int(selected_n_of_persons) > 25:
            messagebox.showerror("Errore", "Massimo 25 persone")
            return

        print("Aeroporto di partenza:", selected_airport_from)
        print("Aeroporto di arrivo:", selected_airport_to)
        print("Date Selezionate:", selected_dates)
        print("Numero di persone:", selected_n_of_persons)

    def update_airport_to_menu(self, event):
        new_airport_from = self.var_1.get()
        self.menu_airport_to.config(values=self.airport_to[new_airport_from])

        self.var_2.set("")
        self.menu_airport_to.set("")