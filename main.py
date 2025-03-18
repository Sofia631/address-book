import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
from db import register_user, save_contact, get_contacts, login_user, update_contact, \
    delete_contact_from_db,  search_contacts
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os


font_path = os.path.join(os.getcwd(), "font", "DejaVuSans.ttf")

pdfmetrics.registerFont(TTFont("DejaVuSans", font_path))

root = ctk.CTk()
root.title("Address Book")
root.geometry("800x500")
root.configure(fg_color="#668598")

custom_font = ("Pixelify Sans", 40, "bold")
custom_font1 = ("Pixelify Sans", 25)
custom_font2 = ("Pixelify Sans", 20)

def open_register():
    root.withdraw()
    reg_window = ctk.CTkToplevel(root)
    reg_window.title("Регистрация")
    reg_window.geometry("500x400")
    reg_window.configure(fg_color="#668598")

    label_username = ctk.CTkLabel(reg_window, text="Логин:", font=custom_font1, text_color="black")
    label_username.pack(pady=5)
    entry_username = ctk.CTkEntry(reg_window, font=custom_font1, width=300)
    entry_username.pack(pady=5)

    label_password = ctk.CTkLabel(reg_window, text="Пароль:", font=custom_font1, text_color="black")
    label_password.pack(pady=5)
    entry_password = ctk.CTkEntry(reg_window, font=custom_font1, width=300, show="*")
    entry_password.pack(pady=5)

    def register():
        username = entry_username.get()
        password = entry_password.get()

        if len(username) > 15:
            messagebox.showerror("Ошибка", "Имя не должно превышать 15 символов.")
            return
        if len(password) > 30 or not any(char.isdigit() for char in password) or not any(
                char.isalpha() for char in password):
            messagebox.showerror("Ошибка", "Пароль должен содержать буквы и цифры и быть не длиннее 30 символов.")
            return

        if register_user(username, password):
            messagebox.showinfo("Успех", f"Пользователь {username} зарегистрирован!")
            reg_window.destroy()  # Закрытие окна регистрации
            open_dashboard(username)  # Открытие окна личного кабинета
        else:
            messagebox.showerror("Ошибка", "Пользователь с таким логином уже существует.")

    btn_register = ctk.CTkButton(reg_window, text="Зарегистрироваться", font=custom_font1, corner_radius=20, hover_color="#555",
                                 fg_color="black",  width= 200, height= 50, border_width= 3, border_color="gray", command=register)
    btn_register.pack(pady=10)

    back_login = ctk.CTkLabel(reg_window, text="Уже есть аккаунт?", font=custom_font1, text_color="black")
    back_login.pack(pady=5)

    btn_back_to_login = ctk.CTkButton(reg_window, text="Войти", font=custom_font1, corner_radius=20,
                                      fg_color="black", hover_color="#555", width= 200, height= 50, border_width= 3,
                                      border_color="gray", command=lambda: (reg_window.destroy(), open_login()))
    btn_back_to_login.pack(pady=5)

    btn_back = ctk.CTkButton(reg_window, text="Назад", font=custom_font1, corner_radius=20, fg_color="green",
                             hover_color="#555",  width= 200, height= 50, border_width= 3, border_color="gray",
                             command=lambda: (reg_window.destroy(), root.deiconify()))
    btn_back.pack(pady=5)

    reg_window.wait_window()

def open_login():
    root.withdraw()
    login_window = ctk.CTkToplevel(root)
    login_window.title("Вход")
    login_window.geometry("500x400")
    login_window.configure(fg_color="#668598")

    label_username = ctk.CTkLabel(login_window, text="Логин:", font=custom_font1, text_color="black")
    label_username.pack(pady=5)
    entry_username = ctk.CTkEntry(login_window, font=custom_font1, width=300)
    entry_username.pack(pady=5)

    label_password = ctk.CTkLabel(login_window, text="Пароль:", font=custom_font1, text_color="black")
    label_password.pack(pady=5)
    entry_password = ctk.CTkEntry(login_window, font=custom_font1, width=300, show="*")
    entry_password.pack(pady=5)

    def login():
        username = entry_username.get()
        password = entry_password.get()

        if login_user(username, password):
            messagebox.showinfo("Успех", f"Добро пожаловать, {username}!")
            login_window.destroy()
            open_dashboard(username)  # Открытие окна личного кабинета
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль.")

    title_reg = ctk.CTkButton(login_window, text="Войти", font=custom_font1, corner_radius=20, fg_color="black", hover_color="#555",
                              width= 200, height= 50, border_width= 3, border_color="gray",
                              command=login)
    title_reg.pack(pady=10)

    back_login = ctk.CTkLabel(login_window, text="Уже есть аккаунт?", font=custom_font1, text_color="black")
    back_login.pack(pady=5)

    btn_back_to_register = ctk.CTkButton(login_window, text="Зарегистрироваться", font=custom_font1,
                                         corner_radius=20, fg_color="black", hover_color="#555",  width= 200,
                                         height= 50, border_width= 3, border_color="gray",
                                         command=lambda: (login_window.destroy(), open_register()))
    btn_back_to_register.pack(pady=5)

    btn_back = ctk.CTkButton(login_window, text="Назад", font=custom_font1, corner_radius=20, fg_color="green",
                             hover_color="#555", width= 200, height= 50, border_width= 3, border_color="gray",
                             command=lambda: (login_window.destroy(), root.deiconify()))
    btn_back.pack(pady=5)

    login_window.wait_window()

def open_dashboard(username):
    dashboard_window = ctk.CTkToplevel(root)
    dashboard_window.title(f"Личный кабинет - {username}")
    dashboard_window.geometry("600x400")
    dashboard_window.configure(fg_color="#668598")

    welcome_label = ctk.CTkLabel(dashboard_window, text=f"Добро пожаловать, {username}!", font=custom_font2,
                                     text_color="black")
    welcome_label.pack(pady=10)


    def perform_search(query):
        query = query.strip()
        if not query:
            messagebox.showerror("Ошибка", "Введите хотя бы один критерий для поиска!")
            return

        results = search_contacts(query)
        if results:
            result_str = "\n".join([f"{fname} {lname} - {phone}" for fname, lname, phone, _, _, _ in results])
            result_label.configure(text=f"Результаты поиска:\n{result_str}")
        else:
            result_label.configure(text="По запросу ничего не найдено.")

    search_frame = ctk.CTkFrame(dashboard_window, fg_color="#668598")
    search_frame.pack(pady=10)

    search_entry = ctk.CTkEntry(search_frame, font=custom_font2, width=250)
    search_entry.pack(side="left", padx=5)

    search_button = ctk.CTkButton(search_frame, text="Найти", font=custom_font2,
                                  command=lambda: perform_search(search_entry.get()), fg_color="blue")
    search_button.pack(side="left")

    result_label = ctk.CTkLabel(dashboard_window, text="Результаты поиска будут отображены здесь.",
                                font=custom_font2, text_color="black")
    result_label.pack(pady=10)

    def contacts(user_id):  # Принимаем user_id, чтобы привязывать контакты к пользователю
        contacts_window = ctk.CTkToplevel(dashboard_window)
        contacts_window.title("Контакты")
        contacts_window.geometry("400x250")
        contacts_window.configure(fg_color="#668598")

        ctk.CTkLabel(contacts_window, text="Добавление контакта", font=("Pixelify Sans", 18), text_color="black").pack(
            pady=10)

        ctk.CTkLabel(contacts_window, text="Выберите тип контакта:", font=("Pixelify Sans", 14),
                     text_color="black").pack(pady=10)

        # Функции вызова окон
        ctk.CTkButton(contacts_window, text="Физическое лицо", font=("Pixelify Sans", 15),
                      corner_radius=20, fg_color="black", text_color="white",
                      command=lambda: add_physical_person(user_id, contacts_window)).pack(pady=5)

        ctk.CTkButton(contacts_window, text="Юридическое лицо", font=("Pixelify Sans", 15),
                      corner_radius=20, fg_color="black", text_color="white",
                      command=lambda: add_organization(user_id, contacts_window)).pack(pady=5)

        def add_physical_person(user_id, parent_window):
            parent_window.destroy()
            add_window = ctk.CTkToplevel()
            add_window.title("Добавление физического лица")
            add_window.geometry("500x500")
            add_window.configure(fg_color="#668598")

            ctk.CTkLabel(add_window, text="Добавление физического лица", font=("Pixelify Sans", 18), text_color="black").pack(pady=10)

            # Фамилия
            entry_lname = ctk.CTkLabel(add_window, text="Фамилия:", font=("Pixelify Sans", 14), text_color="black")
            entry_lname.pack(pady=5)
            entry_lname = ctk.CTkEntry(add_window, font=("Pixelify Sans", 14), width=300)
            entry_lname.pack(pady=5)


            # Имя
            entry_fname = ctk.CTkLabel(add_window, text="Имя:", font=("Pixelify Sans", 14), text_color="black")
            entry_fname.pack(pady=5)
            entry_fname = ctk.CTkEntry(add_window, font=("Pixelify Sans", 14), width=300)
            entry_fname.pack(pady=5)

            # Отчество
            entry_patronymic = ctk.CTkLabel(add_window, text="Отчество:", font=("Pixelify Sans", 14), text_color="black")
            entry_patronymic.pack(pady=5)
            entry_patronymic = ctk.CTkEntry(add_window, font=("Pixelify Sans", 14),  width=300)
            entry_patronymic.pack(pady=5)

            # Телефон
            entry_phone = ctk.CTkLabel(add_window, text="Телефон:", font=("Pixelify Sans", 14), text_color="black")
            entry_phone.pack(pady=5)
            entry_phone = ctk.CTkEntry(add_window, font=("Pixelify Sans", 14), width=300)
            entry_phone.pack(pady=5)

            # Адрес
            entry_address = ctk.CTkLabel(add_window, text="Адрес:", font=("Pixelify Sans", 14), text_color="black")
            entry_address.pack(pady=5)
            entry_address = ctk.CTkEntry(add_window, font=("Pixelify Sans", 14), width=300)
            entry_address.pack(pady=5)

            entry_photo = create_photo_entry(add_window)

            def save():

                lname = entry_lname.get()
                fname = entry_fname.get()
                phone = entry_phone.get()
                address = entry_address.get()
                photo = entry_photo.get()

                save_contact(user_id, entry_fname.get(), entry_lname.get(), entry_patronymic.get(),
                             entry_phone.get(), entry_address.get(), entry_photo.get())

                if not fname or not lname or not phone:
                    # Если фамилия, имя или телефон не введены, показываем сообщение
                    messagebox.showerror("Ошибка", "Фамилия, имя и телефон обязательны для заполнения!")
                    return
                success = save_contact(user_id, fname, lname, "", phone, address, photo)

                if success:
                    messagebox.showinfo("Успех", "Контакт успешно добавлен!")
                else:
                    messagebox.showerror("Ошибка", "Произошла ошибка при добавлении контакта.")

            button_save = ctk.CTkButton(add_window, text="Сохранить", font=custom_font2, command=save, fg_color="green")
            button_save.pack(pady=10)

        def add_organization(user_id, parent_window):
            parent_window.destroy()
            add_window = ctk.CTkToplevel()
            add_window.title("Добавление юридического лица")
            add_window.geometry("500x500")
            add_window.configure(fg_color="#668598")

            label_title = ctk.CTkLabel(add_window, text="Добавление юридического лица", font=("Pixelify Sans", 18),
                                       text_color="black")
            label_title.pack(pady=10)

            label_company = ctk.CTkLabel(add_window, text="Название компании:", font=("Pixelify Sans", 14),
                                         text_color="black")
            label_company.pack(pady=5)
            entry_company_name = ctk.CTkEntry(add_window, width=300)
            entry_company_name.pack(pady=5)


            label_lname = ctk.CTkLabel(add_window, text="Фамилия представителя:", font=("Pixelify Sans", 14),
                                       text_color="black")
            label_lname.pack(pady=5)
            entry_lname = ctk.CTkEntry(add_window, width=300)
            entry_lname.pack(pady=5)

            label_fname = ctk.CTkLabel(add_window, text="Имя представителя:", font=("Pixelify Sans", 14),
                                       text_color="black")
            label_fname.pack(pady=5)
            entry_fname = ctk.CTkEntry(add_window, width=300)
            entry_fname.pack(pady=5)

            label_phone = ctk.CTkLabel(add_window, text="Телефон:", font=("Pixelify Sans", 14), text_color="black")
            label_phone.pack(pady=5)
            entry_phone = ctk.CTkEntry(add_window, width=300)
            entry_phone.pack(pady=5)

            label_address = ctk.CTkLabel(add_window, text="Юридический адрес:", font=("Pixelify Sans", 14),
                                         text_color="black")
            label_address.pack(pady=5)
            entry_address = ctk.CTkEntry(add_window, width=300)
            entry_address.pack(pady=5)

            entry_photo = create_photo_entry(add_window)

            def save():
                company_name = entry_company_name.get().strip()
                lname = entry_lname.get().strip()
                fname = entry_fname.get().strip()
                phone = entry_phone.get().strip()
                address = entry_address.get().strip()
                photo = entry_photo.get().strip()

                if not company_name or not lname or not fname or not phone:
                    messagebox.showerror("Ошибка", "Все поля, кроме адреса и фото, обязательны для заполнения!")
                    return

                success = save_contact(user_id, fname, lname, "", phone, address, photo, company_name)

                if success:
                    messagebox.showinfo("Успех", "Юридическое лицо успешно добавлено!")
                    add_window.destroy()
                else:
                    messagebox.showerror("Ошибка", "Произошла ошибка при добавлении юридического лица.")

            button_save = ctk.CTkButton(add_window, text="Сохранить", font=custom_font2, command=save, fg_color="green")
            button_save.pack(pady=10)

        def create_photo_entry(parent_window):
            def open_file_dialog():
                file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
                if file_path:  # Если путь к файлу был выбран
                    entry_photo.delete(0, ctk.END)  # Очистить текущее значение
                    entry_photo.insert(0, file_path)  # Вставить выбранный путь в поле

            label_photo = ctk.CTkLabel(parent_window, text="Фото:", font=("Pixelify Sans", 14),
                                       text_color="black")
            label_photo.pack(pady=5)

            entry_photo = ctk.CTkEntry(parent_window, width=300)
            entry_photo.pack(pady=5)

            button_photo = ctk.CTkButton(parent_window, text="Выбрать фото", font=("Pixelify Sans", 12),
                                         command=open_file_dialog)
            button_photo.pack(pady=5)

            return entry_photo

    def show_sorted_contacts(contacts, sort_by):
        sorted_contacts = sort_contacts(contacts, sort_by)

        contacts_window = ctk.CTkToplevel()
        contacts_window.title(f"Список контактов ({sort_by})")
        contacts_window.geometry("500x500")
        contacts_window.configure(fg_color="#668598")

        label_title = ctk.CTkLabel(contacts_window, text=f"Сортировка по {sort_by}",
                                   font=("Pixelify Sans", 18), text_color="black")
        label_title.pack(pady=10)

        contact_list_box = tk.Listbox(contacts_window, height=15, width=50, bg="#668598", fg="black",
                                      font=("Pixelify Sans", 14), highlightbackground="black", highlightcolor="black")
        contact_list_box.pack(pady=10)

        for contact in sorted_contacts:
            contact_list_box.insert(tk.END, f"{contact[2]} {contact[3]} - {contact[4]}")  # Формат: ФИО - телефон

        button_close = ctk.CTkButton(contacts_window, text="Закрыть", font=("Pixelify Sans", 14),
                                     command=contacts_window.destroy, fg_color="blue")
        button_close.pack(pady=10)

    def sort_contacts(contacts, sort_by):
        if sort_by == "lname":
            return sorted(contacts, key=lambda x: x[3].lower())
        elif sort_by == "fname":
            return sorted(contacts, key=lambda x: x[2].lower())
        elif sort_by == "phone":
            return sorted(contacts, key=lambda x: x[4].lower())
        return contacts

    def view_contact(user_id):
        view_window = ctk.CTkToplevel()
        view_window.title("Просмотр контакта")
        view_window.geometry("500x500")
        view_window.configure(fg_color="#668598")

        label_title = ctk.CTkLabel(view_window, text="Выберите контакт для просмотра",
                                   font=("Pixelify Sans", 18), text_color="black")
        label_title.pack(pady=10)

        contacts = get_contacts(user_id)
        if not contacts:
            messagebox.showerror("Ошибка", "У вас нет сохраненных контактов.")
            view_window.destroy()
            return

        contact_var = tk.StringVar()
        contact_list = ctk.CTkComboBox(view_window, variable=contact_var,
                                       values=[f"{c[2]} {c[3]} - {c[4]}" for c in contacts])  # Формат: ФИО - телефон
        contact_list.pack(pady=10)

        def load_contact():
            selected_contact = contact_list.get()
            if not selected_contact:
                messagebox.showerror("Ошибка", "Выберите контакт для просмотра.")
                return

            selected_index = [f"{c[2]} {c[3]} - {c[4]}" for c in contacts].index(selected_contact)
            contact = contacts[selected_index]

            for widget in view_window.winfo_children():
                widget.destroy()

            label_title = ctk.CTkLabel(view_window, text="Просмотр контакта", font=("Pixelify Sans", 18),
                                       text_color="black")
            label_title.pack(pady=10)

            labels_entries = [
                ("Фамилия:", contact[3]),
                ("Имя:", contact[2]),
                ("Телефон:", contact[4]),
                ("Отчество:", contact[5] if contact[5] else "Не указано"),
                ("Адрес:", contact[6] if contact[6] else "Не указано"),
                ("Фото:", contact[7] if contact[7] else "Не указано"),
                ("Название компании:", contact[8] if contact[8] else "Не указано"),
            ]

            for label_text, value in labels_entries:
                label = ctk.CTkLabel(view_window, text=label_text, font=("Pixelify Sans", 14), text_color="black")
                label.pack(pady=5)
                entry = ctk.CTkEntry(view_window, width=300)
                entry.insert(0, value)
                entry.pack(pady=5)
                entry.configure(state="disabled")

            if contact[7]:
                try:
                    img = Image.open(contact[7])
                    img = img.resize((150, 150))
                    img = ImageTk.PhotoImage(img)

                    label_img = ctk.CTkLabel(view_window, image=img)
                    label_img.image = img
                    label_img.pack(pady=10)
                except Exception as e:
                    print(f"Ошибка при загрузке изображения: {e}")

            def print_contact():
                file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                         filetypes=[("PDF Files", "*.pdf")])
                if not file_path:
                    return

                c = canvas.Canvas(file_path, pagesize=letter)
                c.setFont("DejaVuSans", 12)
                y = 750

                for label_text, value in labels_entries:
                    c.drawString(100, y, f"{label_text} {value}")
                    y -= 30

                c.save()
                messagebox.showinfo("Успех", "Контакт сохранен в PDF")

            button_print = ctk.CTkButton(view_window, text="Печать", font=("Pixelify Sans", 14), command=print_contact,
                                         fg_color="green")
            button_print.pack(pady=10)

        button_load = ctk.CTkButton(view_window, text="Выбрать", font=("Pixelify Sans", 14), command=load_contact,
                                    fg_color="blue")
        button_load.pack(pady=10)

        button_sort_lname = ctk.CTkButton(view_window, text="Сортировать по фамилии", font=("Pixelify Sans", 14),
                                          command=lambda: show_sorted_contacts(contacts, "lname"))
        button_sort_lname.pack(pady=5)

        button_sort_fname = ctk.CTkButton(view_window, text="Сортировать по имени", font=("Pixelify Sans", 14),
                                          command=lambda: show_sorted_contacts(contacts, "fname"))
        button_sort_fname.pack(pady=5)

        button_sort_phone = ctk.CTkButton(view_window, text="Сортировать по телефону", font=("Pixelify Sans", 14),
                                          command=lambda: show_sorted_contacts(contacts, "phone"))
        button_sort_phone.pack(pady=5)

    def edit_contact(user_id):
        edit_window = ctk.CTkToplevel()
        edit_window.title("Редактирование контакта")
        edit_window.geometry("500x500")
        edit_window.configure(fg_color="#668598")

        label_title = ctk.CTkLabel(edit_window, text="Выберите контакт для редактирования",
                                   font=("Pixelify Sans", 18), text_color="black")
        label_title.pack(pady=10)

        contacts = get_contacts(user_id)
        if not contacts:
            messagebox.showerror("Ошибка", "У вас нет сохраненных контактов.")
            edit_window.destroy()
            return

        contact_var = tk.StringVar()
        contact_list = ctk.CTkComboBox(edit_window, variable=contact_var,
                                       values=[f"{c[2]} {c[3]} - {c[4]}" for c in contacts])
        contact_list.pack(pady=10)

        def load_contact():
            selected_contact = contact_list.get()
            if not selected_contact:
                messagebox.showerror("Ошибка", "Выберите контакт для редактирования.")
                return

            selected_index = [f"{c[2]} {c[3]} - {c[4]}" for c in contacts].index(selected_contact)

            contact = contacts[selected_index]

            for widget in edit_window.winfo_children():
                widget.destroy()

            button_edit = ctk.CTkButton(edit_window, text="Редактировать контакт", font=("Pixelify Sans", 14),
                                        command=lambda: edit_contact(user_id), fg_color="orange")
            button_edit.pack(pady=10)

            labels_entries = [
                ("Фамилия:", contact[3]),
                ("Имя:", contact[2]),
                ("Телефон:", contact[4]),
                ("Отчество:", contact[5] if contact[5] else ""),
                ("Адрес:", contact[6] if contact[6] else ""),
                ("Название компании:", contact[8] if contact[8] else ""),
            ]

            entry_fields = {}
            for label_text, default_value in labels_entries:
                label = ctk.CTkLabel(edit_window, text=label_text, font=("Pixelify Sans", 14), text_color="black")
                label.pack(pady=5)
                entry = ctk.CTkEntry(edit_window, width=300)
                entry.insert(0, default_value)
                entry.pack(pady=5)
                entry_fields[label_text] = entry

            def open_file_dialog():
                file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
                if file_path:
                    entry_photo.delete(0, ctk.END)
                    entry_photo.insert(0, file_path)

            label_photo = ctk.CTkLabel(edit_window, text="Фото:", font=("Pixelify Sans", 14), text_color="black")
            label_photo.pack(pady=5)

            entry_photo = ctk.CTkEntry(edit_window, width=300)
            entry_photo.insert(0, contact[7] if contact[7] else "")
            entry_photo.pack(pady=5)

            button_photo = ctk.CTkButton(edit_window, text="Выбрать фото", font=("Pixelify Sans", 12),
                                         command=open_file_dialog)
            button_photo.pack(pady=5)

            def save_changes():
                new_values = {label: entry.get().strip() for label, entry in entry_fields.items()}
                if not new_values["Фамилия:"] or not new_values["Имя:"] or not new_values["Телефон:"]:
                    messagebox.showerror("Ошибка", "Фамилия, имя и телефон обязательны!")
                    return

                new_photo_path = entry_photo.get().strip()

                update_success = update_contact(
                    contact[0],  # ID контакта
                    new_values["Имя:"], new_values["Фамилия:"], new_values["Отчество:"],
                    new_values["Телефон:"], new_values["Адрес:"], new_photo_path,
                    new_values["Название компании:"]
                )

                if update_success:
                    messagebox.showinfo("Успех", "Контакт успешно обновлен!")
                    edit_window.destroy()
                else:
                    messagebox.showerror("Ошибка", "Не удалось обновить контакт.")

            button_save = ctk.CTkButton(edit_window, text="Сохранить изменения", font=("Pixelify Sans", 14),
                                        command=save_changes, fg_color="green")
            button_save.pack(pady=10)

        button_load = ctk.CTkButton(edit_window, text="Выбрать", font=("Pixelify Sans", 14), command=load_contact,
                                    fg_color="blue")
        button_load.pack(pady=10)

    def delete_contact(user_id):
        delete_window = ctk.CTkToplevel()
        delete_window.title("Удалить контакт")
        delete_window.geometry("500x400")
        delete_window.configure(fg_color="#668598")

        label_title = ctk.CTkLabel(delete_window, text="Выберите контакт для удаления",
                                   font=("Pixelify Sans", 18), text_color="black")
        label_title.pack(pady=10)

        contacts = get_contacts(user_id)
        if not contacts:
            messagebox.showerror("Ошибка", "У вас нет сохраненных контактов.")
            delete_window.destroy()
            return

        contact_var = tk.StringVar()
        contact_list = ctk.CTkComboBox(delete_window, variable=contact_var,
                                       values=[f"{c[2]} {c[3]} - {c[4]}" for c in contacts])
        contact_list.pack(pady=10)

        def delete_selected_contact():
            selected_contact = contact_list.get()
            if not selected_contact:
                messagebox.showerror("Ошибка", "Выберите контакт для удаления.")
                return

            selected_index = [f"{c[2]} {c[3]} - {c[4]}" for c in contacts].index(selected_contact)

            contact = contacts[selected_index]

            confirm = messagebox.askyesno("Подтверждение",
                                          f"Вы уверены, что хотите удалить контакт: {selected_contact}?")
            if confirm:
                success = delete_contact_from_db(contact[0])
                if success:
                    messagebox.showinfo("Успех", "Контакт успешно удален!")
                    delete_window.destroy()
                else:
                    messagebox.showerror("Ошибка", "Не удалось удалить контакт.")

        button_delete = ctk.CTkButton(delete_window, text="Удалить", font=("Pixelify Sans", 14),
                                      command=delete_selected_contact, fg_color="red")
        button_delete.pack(pady=20)

        button_cancel = ctk.CTkButton(delete_window, text="Отмена", font=("Pixelify Sans", 14),
                                      command=delete_window.destroy, fg_color="gray")
        button_cancel.pack(pady=10)

    def open_menu():
        menu_window = ctk.CTkToplevel(dashboard_window)
        menu_window.title("Меню")
        menu_window.geometry("300x400")

        ctk.CTkLabel(menu_window, text="Меню", font=("Pixelify Sans", 20, "bold"), text_color="white").pack(pady=20)

        ctk.CTkButton(menu_window, text="Изменить контакт", font=("Pixelify Sans", 15), corner_radius=20,
                      fg_color="#555", text_color="white", command=lambda: edit_contact(username)).pack(pady=10)

        ctk.CTkButton(menu_window, text="Добавить контакт", font=("Pixelify Sans", 15), corner_radius=20,
                      fg_color="#555", text_color="white", command=lambda: contacts(username)).pack(pady=10)

        ctk.CTkButton(menu_window, text="Просмотр контактов", font=("Pixelify Sans", 15), corner_radius=20,
                      fg_color="#555", text_color="white", command=lambda: view_contact(username)).pack(pady=10)

        ctk.CTkButton(menu_window, text="Удалить контакт", font=("Pixelify Sans", 15), corner_radius=20,
                      fg_color="#555", text_color="white", command=lambda: delete_contact(username)).pack(pady=10)

        ctk.CTkButton(menu_window, text="Закрыть меню", font=("Pixelify Sans", 15), corner_radius=20,
                      fg_color="red", text_color="white", command=menu_window.destroy).pack(pady=20)

    menu_button = ctk.CTkButton(
        dashboard_window, text="☰", font=("Pixelify Sans", 20, "bold"), corner_radius=50, fg_color="#668598", hover_color="#555",
        width=50, height=50, text_color="black", border_color="gray", command=open_menu
    )
    menu_button.place(relx=0.005, rely=0.01)

    btn_logout = ctk.CTkButton(
        dashboard_window, text="Выйти", font=custom_font1, corner_radius=20, fg_color="red", hover_color="#555",
        command=lambda: (dashboard_window.destroy(), root.deiconify())
    )
    btn_logout.place(relx = 0.85, rely = 0.9, anchor="center")

title = ctk.CTkLabel(root, text="ДОБРО ПОЖАЛОВАТЬ\nВ АДРЕСНУЮ КНИГУ 🦝", font=custom_font, fg_color="#668598",
                     text_color="black")
title.pack(pady=50)

btn_login = ctk.CTkButton(root, text="Войти", font=custom_font1, corner_radius=20, fg_color="green",
                          hover_color="#555", width= 200, height= 50, border_width= 3, border_color="gray", command=open_login)
btn_login.pack(pady=10)

btn_register = ctk.CTkButton(root, text="Зарегистрироваться", font=custom_font1, corner_radius=20, fg_color="black",
                             hover_color="#555",  width= 200, height= 50, border_width= 3, border_color="gray", command=open_register)
btn_register.pack(pady=10)

root.mainloop()
