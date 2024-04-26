import babel.numbers
import os
import threading
import tkinter as tk
from alias import alias
from get_n_plot_prices import get_prices
from routes import routes
from datetime import date
from PIL import Image, ImageTk
from time import sleep
from tkcalendar import DateEntry
from tkinter import ttk, messagebox, Scrollbar, Listbox


def print_animation(label):
    try:
        while True:
            label.config(text=".")
            label.update()
            sleep(1)

            label.config(text="..")
            label.update()
            sleep(1)

            label.config(text="...")
            label.update()
            sleep(1)
    except tk.TclError:
        pass
    except RuntimeError:
        pass


def start_animation(label):
    threading.Thread(target=print_animation, args=(label,)).start()


def validate_input(new_text):
    if new_text.isdigit() or new_text == "":
        return True
    else:
        return False


def execute_get_prices(searching_window, selected_airport_from, selected_airport_to, selected_dates,
                       selected_n_of_persons):
    try:
        get_prices(alias[selected_airport_from], alias[selected_airport_to], selected_dates, selected_n_of_persons)
        searching_window.destroy()
    except Exception as e:
        print("Errore durante l'ottenimento dei prezzi:", e)
        try:
            searching_window.destroy()
        except RuntimeError:
            print("Runtime error")


def get_excel_files(folder_path):
    excel_files = [file for file in os.listdir(folder_path)] # if file.endswith('.xlsx')
    print(excel_files)
    return excel_files


class Home(tk.Tk):
    def __init__(self):
        super().__init__()
        self.excel_file = None
        self.title("Ryanair Flight Prices")
        try:
            self.iconphoto(False, tk.PhotoImage(file='icon.png'))
        except tk.TclError:
            print("Errore: icona non trovata")

        self.configure(background='#073693')
        self.resizable(False, False)

        # window sizes and position
        window_width = 700
        window_height = 680
        x_position = (self.winfo_screenwidth() - window_width) // 2
        y_position = ((self.winfo_screenheight() - window_height) // 2)-40
        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # frame
        self.frame_gui = tk.Frame(self, padx=40, pady=30, bg="#073693")
        self.frame_gui.pack()

        # header
        try:
            image = Image.open("header.png")
            photo = ImageTk.PhotoImage(image)
            header_label = tk.Label(self.frame_gui, image=photo, borderwidth=0)
            header_label.image = photo
        except FileNotFoundError:
            header_label = tk.Label(self.frame_gui, text="RYANAIR FLIGHT PRICES", font=("Arial", 15, "bold"), bg="#073693",
                                    fg="#cdab2a")
        finally:
            header_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Airport from
        self.label_airport_from = tk.Label(self.frame_gui, text="Aeroporto di partenza:", font=("Arial", 12), bg="#073693",
                                           fg="white")
        self.label_airport_from.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.airport_from = list(routes)
        self.var_airport_from = tk.StringVar(value=self.airport_from[184])
        self.menu_airport_from = ttk.Combobox(self.frame_gui, values=self.airport_from, textvariable=self.var_airport_from,
                                              state="readonly",
                                              font=("Arial", 12), width=30)
        self.menu_airport_from.grid(row=1, column=1, padx=10, pady=10)

        # Airport to
        self.label_airport_to = tk.Label(self.frame_gui, text="Aeroporto di arrivo:", font=("Arial", 12), bg="#073693",
                                         fg="white")
        self.label_airport_to.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.airport_to = routes
        self.var_airport_to = tk.StringVar(value=self.airport_to[self.airport_from[24]])
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
        self.scrollbar = Scrollbar(self.frame_gui, orient=tk.VERTICAL)
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

        # Look for prices button
        self.look_for_prices = tk.Button(self.frame_gui, text="CERCA PREZZI", command=self.look_for_prices,
                                         font=("Arial", 14), bg="#cdab2a", fg="#073693", relief=tk.FLAT)
        self.look_for_prices.grid(row=6, columnspan=3, padx=10, pady=30)

        # History section
        self.label_history = tk.Label(self.frame_gui, text="Ricerche aperte", font=("Arial", 12), bg="#073693", fg="white")
        self.label_history.grid(row=7, columnspan=3, padx=10, pady=1, sticky="ns")
        self.history = Listbox(self.frame_gui, selectmode=tk.SINGLE, width=55, height=5, font=("Arial", 12), borderwidth=2)
        self.history_scrollbar = Scrollbar(self.frame_gui, orient=tk.VERTICAL, command=self.history.yview)
        self.history.config(yscrollcommand=self.history_scrollbar.set)
        self.history.grid(row=8, column=0, padx=10, pady=10, columnspan=3)
        self.history_scrollbar.grid(row=8, column=2, padx=10, pady=10, sticky="ns")
        self.populate_excel_files_listbox()

        self.reload_button = tk.Button(self.frame_gui, text="Aggiorna ricerche aperte", command=self.populate_excel_files_listbox,
                                       font=("Arial", 12), bg="#cdab2a", fg="#073693", relief=tk.FLAT)
        self.reload_button.grid(row=9, columnspan=3, padx=10, pady=10)

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
        new_airport_from = self.var_airport_from.get()
        self.menu_airport_to.config(values=self.airport_to[new_airport_from])

        self.var_airport_to.set("")
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
        try:
            searching_window.iconphoto(False, tk.PhotoImage(file='icon.png'))
        except tk.TclError:
            print("Errore: icona non trovata")
        searching_window.configure(background='#073693')
        searching_window.resizable(False, False)

        # window sizes and position
        window_width = 350
        window_height = 260
        x_position = (searching_window.winfo_screenwidth() - window_width) // 2
        y_position = (searching_window.winfo_screenheight() - window_height) // 2
        searching_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # frame
        searching_window.frame_gui = tk.Frame(searching_window, bg="#073693")
        searching_window.frame_gui.pack()

        searching_window.sw_label_n_of_persons = tk.Label(searching_window.frame_gui,
                                                          text=f"Numero di persone: {selected_n_of_persons}",
                                                          font=("Arial", 12), bg="#073693", fg="white", padx=5, pady=5)
        searching_window.sw_label_n_of_persons.grid(row=0, column=0, padx=100, pady=5)

        searching_window.sw_route = tk.Label(searching_window.frame_gui,
                                             text=f"{selected_airport_from} ➜ {selected_airport_to}",
                                             font=("Arial", 12), bg="#073693", fg="white", padx=5, pady=2)
        searching_window.sw_route.grid(row=1, column=0, padx=5, pady=2)

        text_selected_date = ""
        for selected_date in selected_dates:
            text_selected_date = text_selected_date + selected_date + "\n"

        searching_window.sw_dates = tk.Label(searching_window.frame_gui,
                                             text=text_selected_date, font=("Arial", 12),
                                             bg="#073693", fg="white", padx=5)
        searching_window.sw_dates.grid(row=2, column=0, padx=5)

        searching_window.sw_loading = tk.Label(searching_window.frame_gui,
                                               font=("Arial", 22), bg="#073693", fg="white", padx=5)
        searching_window.sw_loading.grid(row=3, column=0, padx=5)
        start_animation(searching_window.sw_loading)

        thread = threading.Thread(target=execute_get_prices,
                                  args=(searching_window, selected_airport_from, selected_airport_to, selected_dates,
                                        selected_n_of_persons))
        thread.start()

        sheet_name = alias[selected_airport_from] + '-' + alias[selected_airport_to]
        self.excel_file = "tabella_prezzi/" + selected_n_of_persons + '-' + sheet_name + "-" + ",".join(
            selected_dates) + ".xlsx"

        # wait for the end of the thread
        self.after(100, self.wait_for_thread, thread, searching_window)

    def wait_for_thread(self, thread, searching_window):
        if thread.is_alive():
            self.after(100, self.wait_for_thread, thread, searching_window)
        else:
            if os.path.exists(self.excel_file):
                messagebox.showinfo("Fatto!", "Controlla file Excel e grafico.")

            else:
                messagebox.showerror("Volo inesistente",
                                     "Assicurati che un volo esista tuttora prima di cercarne i prezzi.")

            searching_window.destroy()
            self.populate_excel_files_listbox()

    def populate_excel_files_listbox(self):
        excel_folder = "tabella_prezzi"
        try:
            self.history.delete(0, tk.END)
            excel_files = get_excel_files(excel_folder)
            if not excel_files:
                self.history.insert(tk.END, "Nessuna ricerca aperta al momento")
            else:
                for file in excel_files:
                    self.history.insert(tk.END, file)
        except FileNotFoundError:
            print("Cartella prezzi non trovata")