import os
import re
import threading
import tkinter as tk
from ryanair_configs.alias import alias, inverted_alias
from business_logic.get_n_plot_prices import get_prices
from ryanair_configs.routes import routes
from datetime import date, datetime
from idlelib.tooltip import Hovertip
from PIL import Image, ImageTk
from time import sleep, ctime, strptime, strftime
from tkcalendar import DateEntry
from tkinter import ttk, messagebox, Scrollbar, Listbox


def start_animation(label):
    threading.Thread(target=print_animation, args=(label,)).start()


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
    excel_files = []
    for file in os.listdir(folder_path):
        excel_files.append(file[:-5] + strftime(".   Last update: %Y-%m-%d, ore %H:%M:%S",
                                                strptime(ctime(os.path.getmtime(f"{folder_path}/{file}")))))
    return excel_files


def get_history_flight_fields(string_flight):
    pattern = (r'^(\d+)-([A-Z]{3})-([A-Z]{3})-(\d{4}-\d{2}-\d{2}(?:,\d{4}-\d{2}-\d{2})*)\.   '
               r'Last update: (\d{4}-\d{2}-\d{2}), ore (\d{2}:\d{2}:\d{2})$')
    match = re.match(pattern, string_flight)

    if match:
        history_n_of_persons = int(match.group(1))
        history_airport_from = match.group(2)
        history_airport_to = match.group(3)
        history_dates_string = match.group(4)
        history_dates_list = history_dates_string.split(',')

        return history_n_of_persons, history_airport_from, history_airport_to, history_dates_list
    else:
        return None


class Home(tk.Tk):
    def __init__(self):
        super().__init__()
        self.excel_file = None
        self.title("Ryanair Flight Prices")
        try:
            self.iconphoto(False, tk.PhotoImage(file='img/icon.png'))
        except tk.TclError:
            print("Errore: icona non trovata")

        self.configure(background='#073693')
        self.resizable(False, False)

        # window sizes and position
        window_width = 700
        window_height = 680
        x_position = (self.winfo_screenwidth() - window_width) // 2
        y_position = ((self.winfo_screenheight() - window_height) // 2) - 40
        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # frame
        self.frame_gui = tk.Frame(self, padx=40, pady=30, bg="#073693")
        self.frame_gui.pack()

        # header
        try:
            image = Image.open("img/header.png")
            photo = ImageTk.PhotoImage(image)
            header_label = tk.Label(self.frame_gui, image=photo, borderwidth=0)
            header_label.image = photo
        except FileNotFoundError:
            header_label = tk.Label(self.frame_gui, text="RYANAIR FLIGHT PRICES", font=("Arial", 15, "bold"),
                                    bg="#073693",
                                    fg="#cdab2a")
        finally:
            header_label.grid(row=0, column=0, columnspan=3, pady=10)

        help_button = tk.Button(self.frame_gui, text='HELP', font=("Arial", 10), bg="#073693", fg="#cdab2a",
                                relief=tk.FLAT, activebackground="#073693", activeforeground="#9c7f13", borderwidth=0,
                                highlightthickness=0)
        help_button.grid(row=0, column=0, padx=(1, 130), pady=(0, 30))
        help_tip = Hovertip(help_button, 'Non spostare il programma dalla cartella in cui si trova. Se lo vuoi nel \n'
                                         'tuo desktop, clicca cn il tasto destro sull\'icona del programma e vai su \n'
                                         '\'Invia a -> Desktop (crea collegamento)\'. Fai lo stesso anche per la'
                                         ' cartella\n\'risultati\' e se vuoi anche per \'tabelle_excel\'.\n\n'
                                         'Inserisci nel pannello le date del volo che stai cercando cliccando su \n'
                                         '\'Aggiungi data\'. Se inserisci una data per errore, selezionala nel pannello'
                                         '\ne clicca su \'Cancella data\', o premi direttamente CANC.\n'
                                         'Più date inserirai (max 7), più sarà lento il programma a cercare i prezzi.\n'
                                         '\nCliccando su una ricerca nella cronologia, ti verranno automaticamente\n'
                                         'riempiti i campi di ricerca del volo, così da velocizzare un\'eventuale nuova'
                                         '\nricerca sullo stesso volo. Per cancellare la cronologia, svuota la cartella'
                                         '\n\'tabelle_excel\'.\n\n'
                                         'Qualora non si aprisse in automatico il file pdf con i risultati della tua\n'
                                         'ricerca, lo troverai nella cartella \'risultati\' con lo stesso nome presente'
                                         '\nin cronologia. Buone ricerche!', hover_delay=0)

        credits_button = tk.Button(self.frame_gui, text='CREDITS', font=("Arial", 10), bg="#073693", fg="#cdab2a",
                                   relief=tk.FLAT, activebackground="#073693", activeforeground="#9c7f13",
                                   borderwidth=0, highlightthickness=0)
        credits_button.grid(row=0, column=2, padx=(45, 1), pady=(0, 30))
        credits_tip = Hovertip(credits_button, f'Ryanair Flight Prices, v1.0.\nFor personal use only.\n'
                                               f'Powered by Vincenzo Altavilla.\nCopyright © {date.today().year}.',
                               hover_delay=0)

        # Airport from
        self.label_airport_from = tk.Label(self.frame_gui, text="Aeroporto di partenza:", font=("Arial", 12),
                                           bg="#073693",
                                           fg="white")
        self.label_airport_from.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.airport_from = list(routes)
        self.var_airport_from = tk.StringVar(value=self.airport_from[184])
        self.menu_airport_from = ttk.Combobox(self.frame_gui, values=self.airport_from,
                                              textvariable=self.var_airport_from,
                                              state="readonly",
                                              font=("Arial", 12), width=30)
        self.menu_airport_from.grid(row=1, column=1, padx=10, pady=10)

        # Airport to
        self.label_airport_to = tk.Label(self.frame_gui, text="Aeroporto di arrivo:", font=("Arial", 12), bg="#073693",
                                         fg="white")
        self.label_airport_to.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.airport_to = routes
        self.var_airport_to = tk.StringVar()
        self.menu_airport_to = ttk.Combobox(self.frame_gui, state="readonly", font=("Arial", 12), width=30)
        self.menu_airport_to.grid(row=2, column=1, padx=10, pady=10)
        # callback to update airport to menu
        self.menu_airport_from.bind("<<ComboboxSelected>>", self.update_airport_to_menu)
        self.menu_airport_to.bind("<<ComboboxSelected>>", self.update_switch_airports)

        # Switch airports
        self.switch_airports_button = tk.Button(self.frame_gui, text="🔃", font=("Arial", 40), bg="#073693",
                                                fg="#cdab2a",
                                                relief=tk.FLAT, activebackground="#073693", activeforeground="#9c7f13",
                                                borderwidth=0, state="disabled", command=self.switch_airports)
        self.switch_airports_button.grid(row=1, column=2, rowspan=2)
        self.update_airport_to_menu(None)

        self.selected_dates = []
        # Calendar
        self.label_calendar = tk.Label(self.frame_gui, text="Date:", font=("Arial", 12), bg="#073693", fg="white")
        self.label_calendar.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.calendar = DateEntry(self.frame_gui, width=30, background="#cdab2a", foreground="#073693", borderwidth=2,
                                  date_pattern="yyyy-mm-dd", state="readonly", font=("Arial", 12))
        self.calendar.grid(row=3, column=1, padx=10, pady=(10, 0))

        # Add date button
        self.add_date_button = tk.Button(self.frame_gui, text="Aggiungi data", command=self.add_date,
                                         font=("Arial", 12),
                                         bg="#cdab2a", fg="#073693", activebackground="#9c7f13",
                                         activeforeground="#073693",
                                         relief=tk.FLAT)
        self.add_date_button.grid(row=3, column=2, padx=10, pady=(10, 0), sticky="s")

        # Selected dates list
        self.label_selected_dates = tk.Label(self.frame_gui, text="Date selezionate:", font=("Arial", 12), bg="#073693",
                                             fg="white")
        self.label_selected_dates.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="e")
        self.scrollbar = Scrollbar(self.frame_gui, orient=tk.VERTICAL)
        self.dates_list = Listbox(self.frame_gui, width=30, height=5, font=("Arial", 12), borderwidth=2,
                                  yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.dates_list.yview)
        self.dates_list.grid(row=4, column=1, padx=10, pady=(0, 10), sticky="nsw")
        self.scrollbar.grid(row=4, column=1, padx=13, pady=(0, 10), sticky="nse")

        # Delete date button
        self.delete_date_button = tk.Button(self.frame_gui, text="Cancella data", command=self.delete_date,
                                            font=("Arial", 12), state="disabled", bg="#8c061e", fg="white",
                                            activebackground="#540413", activeforeground="white", relief=tk.FLAT)
        self.delete_date_button.grid(row=4, column=2, columnspan=3, padx=10, pady=(0, 10))
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
                                         font=("Arial", 14, "bold"), bg="#cdab2a", fg="#073693",
                                         activebackground="#9c7f13",
                                         activeforeground="#073693", relief=tk.FLAT)
        self.look_for_prices.grid(row=6, columnspan=3, padx=10, pady=(10, 40))

        # History section
        self.label_history = tk.Label(self.frame_gui, text="Cronologia ricerche:", font=("Arial", 12), bg="#073693",
                                      fg="white")
        self.label_history.grid(row=7, columnspan=3, padx=52, pady=(10, 0), sticky="nsw")
        self.history = Listbox(self.frame_gui, selectmode=tk.SINGLE, width=71, height=5, font=("Arial", 10),
                               borderwidth=2)
        self.history_scrollbar_vert = Scrollbar(self.frame_gui, orient=tk.VERTICAL, command=self.history.yview)
        self.history_scrollbar_horiz = Scrollbar(self.frame_gui, orient=tk.HORIZONTAL, command=self.history.xview)
        self.history.config(yscrollcommand=self.history_scrollbar_vert.set,
                            xscrollcommand=self.history_scrollbar_horiz.set)
        self.history.grid(row=8, column=0, padx=55, columnspan=3, sticky="nsw")
        self.history_scrollbar_vert.grid(row=8, column=2, padx=55, sticky="nse")
        self.history_scrollbar_horiz.grid(row=9, column=0, padx=55, columnspan=3, sticky="new")
        self.populate_excel_files_listbox()

        self.history.bind("<<ListboxSelect>>", self.set_history_flight)

        self.reload_button = tk.Button(self.frame_gui, text="Aggiorna cronologia",
                                       command=self.populate_excel_files_listbox,
                                       font=("Arial", 12), bg="#cdab2a", fg="#073693", activebackground="#9c7f13",
                                       activeforeground="#073693", relief=tk.FLAT)
        self.reload_button.grid(row=9, columnspan=3, padx=10, pady=25)

    def update_airport_to_menu(self, event):
        new_airport_from = self.var_airport_from.get()
        self.menu_airport_to.config(values=self.airport_to[new_airport_from])
        self.var_airport_to.set("")
        self.menu_airport_to.set("")
        self.switch_airports_button.config(state="disabled")

    def update_switch_airports(self, event):
        self.switch_airports_button.config(state="normal")

    def switch_airports(self):
        hold = self.menu_airport_from.get()
        self.menu_airport_from.set(str(self.menu_airport_to.get()))
        self.var_airport_from.set(str(self.menu_airport_to.get()))
        self.update_airport_to_menu(None)

        if hold in self.airport_to[str(self.menu_airport_from.get())]:
            self.menu_airport_to.set(hold)
            self.var_airport_to.set(hold)
            self.switch_airports_button.config(state="normal")

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

        if len(selected_dates) > 7:
            messagebox.showerror("Errore", "Puoi selezionare al massimo 7 date.")
            return

        selected_n_of_persons = self.number_of_persons_spinbox.get()
        if not selected_n_of_persons:
            messagebox.showerror("Errore", "Il campo del numero di persone non può essere vuoto.")
            return

        for data in selected_dates:
            if datetime.strptime(data, "%Y-%m-%d").date() < datetime.now().date():
                messagebox.showerror("Errore", "Nel campo 'Date Selezionate' è presente una data"
                                               " antecedente ad oggi.")
                return

        searching_window = tk.Toplevel(self)
        searching_window.title("Ricercando prezzi...")
        try:
            searching_window.iconphoto(False, tk.PhotoImage(file='img/icon.png'))
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
        self.excel_file = "tabelle_excel/" + selected_n_of_persons + '-' + sheet_name + "-" + ",".join(
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
        excel_folder = "tabelle_excel"
        try:
            self.history.delete(0, tk.END)
            excel_files = get_excel_files(excel_folder)
            # print(excel_files)
            if not excel_files:
                self.history.insert(tk.END, "                                                  Cronologia vuota")
            else:
                for file in excel_files:
                    self.history.insert(tk.END, file)
        except FileNotFoundError:
            self.history.insert(tk.END, "                                          Cartella prezzi non trovata")

    def set_history_flight(self, event):
        selected_item = None
        try:
            selected_item = self.history.get(self.history.curselection())
        except tk.TclError:
            pass

        if selected_item:
            flight_fields = get_history_flight_fields(selected_item)
            if flight_fields:
                history_n_of_persons, history_airport_from, history_airport_to, history_dates = flight_fields
                try:
                    self.number_of_persons_spinbox.delete(0, tk.END)
                    self.number_of_persons_spinbox.insert(0, history_n_of_persons)

                    self.menu_airport_from.set(value=inverted_alias[history_airport_from])
                    self.menu_airport_from.bind("<<ComboboxSelected>>", self.update_airport_to_menu)
                    self.update_airport_to_menu(None)
                    self.menu_airport_to.set(value=inverted_alias[history_airport_to])

                    self.dates_list.delete(0, tk.END)

                    # Add history dates
                    for data in history_dates:
                        self.dates_list.insert(tk.END, data)

                    self.selected_dates = history_dates
                    self.update_date_list()
                    self.delete_date_button.config(state="normal")
                    self.switch_airports_button.config(state="normal")

                except IndexError:
                    # Gestione dell'errore nel caso in cui il formato dell'elemento selezionato non sia corretto
                    print("Errore: formato cronologia non valido")
            else:
                print("Stringa non valida.")


if __name__ == "__main__":
    app = Home()
    app.mainloop()
