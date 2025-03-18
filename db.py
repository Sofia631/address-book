import sqlite3

conn = sqlite3.connect("contacts.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        users_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        contacts_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        fname TEXT NOT NULL,
        lname TEXT NOT NULL,
        phone TEXT NOT NULL,
        patronymic TEXT DEFAULT NULL,
        address TEXT DEFAULT NULL,
        photo TEXT DEFAULT NULL,
        company_name TEXT DEFAULT NULL,
        contact_type TEXT DEFAULT "Физическое лицо",
        FOREIGN KEY (user_id) REFERENCES users(users_id) ON DELETE CASCADE
    )  
''')

conn.commit()

def search_contacts(query):
    cursor.execute("""
        SELECT fname, lname, phone, patronymic, address, company_name
        FROM contacts
        WHERE fname LIKE ? OR lname LIKE ? OR phone LIKE ? OR patronymic LIKE ? OR address LIKE ? OR company_name LIKE ?
    """, (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"))

    return cursor.fetchall()

def load_contact(contact):
    try:
        if len(contact) < 8:
            print("❌ Ошибка: контакт содержит недостаточно данных", contact)
            return

        contact_id, user_id, fname, lname, patronymic, phone, address, company_name = contact

        print(f"📞 Просмотр контакта: {fname} {lname}")

        contact_info = f"""
        Фамилия: {lname}
        Имя: {fname}
        Отчество: {patronymic if patronymic else 'Не указано'}
        Телефон: {phone}
        Адрес: {address if address else 'Не указано'}
        Компания: {company_name if company_name else 'Не указано'}
        """
        print(contact_info)

    except Exception as e:
        print(f"❌ Ошибка при загрузке контакта: {e}")

def add_contact(user_id, fname, lname, phone, patronymic=None, address=None, company_name=None):
    try:
        cursor.execute("""
            INSERT INTO contacts (user_id, fname, lname, phone, patronymic, address, company_name)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, fname.strip(), lname.strip(), phone.strip(),
              patronymic.strip() if patronymic else None,
              address.strip() if address else None,
              company_name.strip() if company_name else None))

        conn.commit()
        print(f"✅ Контакт {fname} {lname} успешно добавлен!")
    except sqlite3.IntegrityError:
        print(f"⚠️ Контакт {fname} {lname} уже существует!")
    except Exception as e:
        print(f"❌ Ошибка при добавлении контакта: {e}")

def register_user(username, password):
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()  # Если пользователь найден, он вернет строку с данными

    if existing_user:
        print("Ошибка: логин занят ")
        return False  # Возвращаем False, если логин занят

    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    print(f"Пользователь {username} успешно зарегистрирован! ")
    return True

def login_user(username, password):
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    return user is not None

def save_contact(user_id, fname, lname, patronymic, phone, address, photo, company_name=None):
    if not lname or not fname or not phone:
        print("Ошибка: Фамилия, имя и телефон обязательны!")
        return False

    cursor.execute("""
        INSERT INTO contacts (user_id, fname, lname, phone, patronymic, address, photo, company_name) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                   (user_id, fname, lname, phone, patronymic, address, photo, company_name))

    conn.commit()
    print("Контакт добавлен!")
    return True

def update_contact(contact_id, fname, lname, patronymic, phone, address, photo, company_name):
    try:
        cursor.execute("""
            UPDATE contacts
            SET fname = ?, lname = ?, patronymic = ?, phone = ?, address = ?, photo = ?, 
                company_name = ?
            WHERE contacts_id = ?
        """, (fname, lname, patronymic, phone, address, photo, company_name, contact_id))

        conn.commit()
        return True  # Если обновление успешно
    except sqlite3.Error as e:
        print(f"Ошибка при обновлении контакта: {e}")
        return False

def delete_contact_from_db(contact_id):
    try:
        # Запрос для удаления контакта по правильному имени столбца
        cursor.execute("DELETE FROM contacts WHERE contacts_id = ?", (contact_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Ошибка при удалении контакта: {e}")
        return False

def get_contacts(user_id):
    cursor.execute("SELECT * FROM contacts WHERE user_id = ?", (user_id,))
    return cursor.fetchall()

def close_db():
    conn.close()

