import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QComboBox, QTextEdit, QInputDialog, QListWidget, QListWidgetItem
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

# Подключение к базе данных SQLite3
conn = sqlite3.connect('sportcomplex.db')
cursor = conn.cursor()

# Создание таблиц в базе данных
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    login TEXT UNIQUE,
                    password TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    middle_name TEXT,
                    age INTEGER)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    rating INTEGER,
                    review TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS trainings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sport TEXT,
                    time TEXT,
                    coach TEXT,
                    day INTEGER)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS user_trainings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    training_id INTEGER,
                    day INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (training_id) REFERENCES trainings(id))''')

conn.commit()

# Функция для инициализации начальных данных о тренировках
def initialize_trainings():
    cursor.execute('SELECT COUNT(*) FROM trainings')
    count = cursor.fetchone()[0]
    if count == 0:
        trainings = [
            ('Плавание', '10:00', 'Морозов Н.К', 1),
            ('Футбол', '12:00', 'Шипулин А.А.', 1),
            ('Баскетбол', '14:00', 'Сарычев М.И.', 1),
            ('Волейбол', '16:00', 'Кондрашов В.С.', 1),
            ('Борьба', '18:00', 'Чупраков А.П.', 1)
        ]
        cursor.executemany('INSERT INTO trainings (sport, time, coach, day) VALUES (?, ?, ?, ?)', trainings)
        conn.commit()

# Вызов функции для инициализации начальных данных
initialize_trainings()

class HoverButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMouseTracking(True)  # Включаем отслеживание мыши
        self.setAutoFillBackground(True)  # Включаем автоматическое заполнение фона
        self.default_color = QColor(255, 255, 255)  # Цвет по умолчанию
        self.hover_color = QColor(200, 200, 255)  # Цвет при наведении
        self.pressed_color = QColor(150, 150, 255)  # Цвет при нажатии
        self.update_color(self.default_color)

    def enterEvent(self, event):
        self.update_color(self.hover_color)

    def leaveEvent(self, event):
        self.update_color(self.default_color)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.update_color(self.pressed_color)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.update_color(self.hover_color)
        super().mouseReleaseEvent(event)

    def update_color(self, color):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Button, color)
        self.setPalette(palette)

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.resize(350, 300)  # Установка размера окна

    def initUI(self):
        self.setWindowTitle('Спорткомплекс - Авторизация')
        layout = QVBoxLayout()

        self.btn_admin = HoverButton('Войти как администратор')
        self.btn_user = HoverButton('Войти как пользователь')
        self.btn_register = HoverButton('Зарегистрироваться')
        self.btn_admin.setFixedSize(350, 50)
        self.btn_user.setFixedSize(350, 50)
        self.btn_register.setFixedSize(350, 50)

        self.btn_admin.clicked.connect(self.openAdminLogin)
        self.btn_user.clicked.connect(self.openUserLogin)
        self.btn_register.clicked.connect(self.openRegister)

        layout.addWidget(self.btn_admin)
        layout.addWidget(self.btn_user)
        layout.addWidget(self.btn_register)

        self.setLayout(layout)

    def openAdminLogin(self):
        self.admin_login_window = AdminLoginWindow()
        self.admin_login_window.show()

    def openUserLogin(self):
        self.user_login_window = UserLoginWindow()
        self.user_login_window.show()

    def openRegister(self):
        self.register_window = RegisterWindow()
        self.register_window.show()

class AdminLoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.resize(400, 200)  # Установка размера окна

    def initUI(self):
        self.setWindowTitle('Администратор - Вход')
        layout = QVBoxLayout()

        self.lbl_login = QLabel('Логин:')
        self.txt_login = QLineEdit()
        self.lbl_password = QLabel('Пароль:')
        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.btn_login = HoverButton('Войти')

        self.btn_login.clicked.connect(self.login)

        layout.addWidget(self.lbl_login)
        layout.addWidget(self.txt_login)
        layout.addWidget(self.lbl_password)
        layout.addWidget(self.txt_password)
        layout.addWidget(self.btn_login)

        self.setLayout(layout)

    def login(self):
        login = self.txt_login.text()
        password = self.txt_password.text()

        if login == 'admin' and password == '1234':
            self.admin_window = AdminWindow()
            self.admin_window.show()
            self.close()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Логин или пароль введены неправильно')

class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.resize(350, 300)  # Установка размера окна

    def initUI(self):
        self.setWindowTitle('Администратор - Главное меню')
        layout = QVBoxLayout()

        self.btn_profiles = HoverButton('Профили')
        self.btn_trainings = HoverButton('Тренировки')
        self.btn_reviews = HoverButton('Отзывы')
        self.btn_profiles.setFixedSize(350, 50)
        self.btn_trainings.setFixedSize(350, 50)
        self.btn_reviews.setFixedSize(350, 50)

        self.btn_profiles.clicked.connect(self.openProfiles)
        self.btn_trainings.clicked.connect(self.openTrainings)
        self.btn_reviews.clicked.connect(self.openReviews)

        layout.addWidget(self.btn_profiles)
        layout.addWidget(self.btn_trainings)
        layout.addWidget(self.btn_reviews)

        self.setLayout(layout)

    def openProfiles(self):
        self.profiles_window = ProfilesWindow()
        self.profiles_window.show()

    def openTrainings(self):
        self.trainings_window = TrainingsWindow()
        self.trainings_window.show()

    def openReviews(self):
        self.reviews_window = ReviewsWindow()
        self.reviews_window.show()

class ProfilesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.resize(640, 400)  # Установка размера окна

    def initUI(self):
        self.setWindowTitle('Администратор - Профили')
        layout = QVBoxLayout()

        self.table = QTableWidget(self)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['ID', 'Логин', 'Пароль', 'Фамилия', 'Имя', 'Отчество'])

        self.loadProfiles()

        layout.addWidget(self.table)
        self.setLayout(layout)

    def loadProfiles(self):
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()

        self.table.setRowCount(len(users))
        for row, user in enumerate(users):
            for col, item in enumerate(user):
                self.table.setItem(row, col, QTableWidgetItem(str(item)))

class TrainingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.resize(400, 150)  # Установка размера окна

    def initUI(self):
        self.setWindowTitle('Администратор - Тренировки')
        layout = QVBoxLayout()

        self.day_combo = QComboBox()
        for i in range(1, 32):
            self.day_combo.addItem(str(i))

        self.btn_select_day = HoverButton('Выбрать день')
        self.btn_select_day.setFixedSize(350, 30)
        self.btn_select_day.clicked.connect(self.selectDay)

        layout.addWidget(self.day_combo)
        layout.addWidget(self.btn_select_day)

        self.setLayout(layout)

    def selectDay(self):
        day = int(self.day_combo.currentText())
        self.day_window = DayTrainingsWindow(day)
        self.day_window.show()

class DayTrainingsWindow(QWidget):
    def __init__(self, day):
        super().__init__()
        self.day = day
        self.initUI()
        self.resize(340, 400)  # Установка размера окна

    def initUI(self):
        self.setWindowTitle(f'Администратор - Тренировки на {self.day} день')
        layout = QVBoxLayout()

        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Спорт', 'Время', 'Тренер'])

        self.loadTrainings()

        self.btn_add = HoverButton('Добавить тренировку')
        self.btn_delete = HoverButton('Удалить тренировку')

        self.btn_add.clicked.connect(self.addTraining)
        self.btn_delete.clicked.connect(self.deleteTraining)

        layout.addWidget(self.table)
        layout.addWidget(self.btn_add)
        layout.addWidget(self.btn_delete)

        self.setLayout(layout)

    def loadTrainings(self):
        cursor.execute('SELECT sport, time, coach FROM trainings WHERE day = ?', (self.day,))
        trainings = cursor.fetchall()

        self.table.setRowCount(len(trainings))
        for row, training in enumerate(trainings):
            for col, item in enumerate(training):
                self.table.setItem(row, col, QTableWidgetItem(str(item)))

    def addTraining(self):
        sport, ok = QInputDialog.getText(self, 'Добавить тренировку', 'Спорт:')
        if ok and sport:
            time, ok = QInputDialog.getText(self, 'Добавить тренировку', 'Время:')
            if ok and time:
                coach, ok = QInputDialog.getText(self, 'Добавить тренировку', 'Тренер:')
                if ok and coach:
                    cursor.execute('INSERT INTO trainings (sport, time, coach, day) VALUES (?, ?, ?, ?)', (sport, time, coach, self.day))
                    conn.commit()
                    self.loadTrainings()

    def deleteTraining(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            sport = self.table.item(selected_row, 0).text()
            time = self.table.item(selected_row, 1).text()
            coach = self.table.item(selected_row, 2).text()
            cursor.execute('DELETE FROM trainings WHERE sport = ? AND time = ? AND coach = ? AND day = ?', (sport, time, coach, self.day))
            conn.commit()
            self.loadTrainings()

class ReviewsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.resize(350, 300)  # Установка размера окна

    def initUI(self):
        self.setWindowTitle('Администратор - Отзывы')
        layout = QVBoxLayout()

        self.review_list = QListWidget()
        self.loadReviews()

        self.review_list.itemClicked.connect(self.showReview)

        layout.addWidget(self.review_list)
        self.setLayout(layout)

    def loadReviews(self):
        cursor.execute('''SELECT r.rating, r.review, u.last_name, u.first_name, u.middle_name, u.id
                          FROM reviews r
                          JOIN users u ON r.user_id = u.id''')
        reviews = cursor.fetchall()

        for rating, review, last_name, first_name, middle_name, user_id in reviews:
            self.review_list.addItem(f'Оценка: {rating} (ФИО: {last_name} {first_name} {middle_name}, ID: {user_id})')

    def showReview(self, item):
        user_id = int(item.text().split('ID: ')[1])
        cursor.execute('SELECT review FROM reviews WHERE user_id = ?', (user_id,))
        review = cursor.fetchone()[0]

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('Отзыв')
        msg_box.setText(review)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        msg_box.buttonClicked.connect(lambda btn: self.openUserProfile(btn, user_id) if btn.text() == 'OK' else None)
        msg_box.exec()

    def openUserProfile(self, btn, user_id):
        self.user_profile_window = UserProfileWindow(user_id)
        self.user_profile_window.show()

class UserProfileWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.initUI()
        self.resize(400, 300)  # Установка размера окна

    def initUI(self):
        self.setWindowTitle('Профиль пользователя')
        layout = QVBoxLayout()

        cursor.execute('SELECT last_name, first_name, middle_name, age FROM users WHERE id = ?', (self.user_id,))
        profile = cursor.fetchone()

        profile_info = f'Фамилия: {profile[0]}\nИмя: {profile[1]}\nОтчество: {profile[2]}\nВозраст: {profile[3]}'
        self.lbl_profile = QLabel(profile_info)

        layout.addWidget(self.lbl_profile)
        self.setLayout(layout)

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.resize(400, 300)  # Установка размера окна

    def initUI(self):
        self.setWindowTitle('Регистрация')
        layout = QVBoxLayout()

        self.lbl_last_name = QLabel('Фамилия:')
        self.txt_last_name = QLineEdit()
        self.lbl_first_name = QLabel('Имя:')
        self.txt_first_name = QLineEdit()
        self.lbl_middle_name = QLabel('Отчество:')
        self.txt_middle_name = QLineEdit()
        self.lbl_age = QLabel('Возраст:')
        self.txt_age = QLineEdit()
        self.lbl_login = QLabel('Логин:')
        self.txt_login = QLineEdit()
        self.lbl_password = QLabel('Пароль:')
        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.btn_register = HoverButton('Зарегистрироваться')

        self.btn_register.clicked.connect(self.register)

        layout.addWidget(self.lbl_last_name)
        layout.addWidget(self.txt_last_name)
        layout.addWidget(self.lbl_first_name)
        layout.addWidget(self.txt_first_name)
        layout.addWidget(self.lbl_middle_name)
        layout.addWidget(self.txt_middle_name)
        layout.addWidget(self.lbl_age)
        layout.addWidget(self.txt_age)
        layout.addWidget(self.lbl_login)
        layout.addWidget(self.txt_login)
        layout.addWidget(self.lbl_password)
        layout.addWidget(self.txt_password)
        layout.addWidget(self.btn_register)

        self.setLayout(layout)

    def register(self):
        last_name = self.txt_last_name.text()
        first_name = self.txt_first_name.text()
        middle_name = self.txt_middle_name.text()
        age = self.txt_age.text()
        login = self.txt_login.text()
        password = self.txt_password.text()

        if not last_name or not first_name or not middle_name or not age or not login or not password:
            QMessageBox.warning(self, 'Ошибка', 'Все поля должны быть заполнены')
            return

        try:
            age = int(age)
        except ValueError:
            QMessageBox.warning(self, 'Ошибка', 'Возраст должен быть числом')
            return

        try:
            cursor.execute('INSERT INTO users (login, password, first_name, last_name, middle_name, age) VALUES (?, ?, ?, ?, ?, ?)',
                           (login, password, first_name, last_name, middle_name, age))
            conn.commit()
            QMessageBox.information(self, 'Успех', 'Регистрация прошла успешно')
            self.close()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, 'Ошибка', 'Логин уже занят')

class UserLoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.resize(400, 200)  # Установка размера окна

    def initUI(self):
        self.setWindowTitle('Пользователь - Вход')
        layout = QVBoxLayout()

        self.lbl_login = QLabel('Логин:')
        self.txt_login = QLineEdit()
        self.lbl_password = QLabel('Пароль:')
        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.btn_login = HoverButton('Войти')

        self.btn_login.clicked.connect(self.login)

        layout.addWidget(self.lbl_login)
        layout.addWidget(self.txt_login)
        layout.addWidget(self.lbl_password)
        layout.addWidget(self.txt_password)
        layout.addWidget(self.btn_login)

        self.setLayout(layout)

    def login(self):
        login = self.txt_login.text()
        password = self.txt_password.text()

        cursor.execute('SELECT id FROM users WHERE login = ? AND password = ?', (login, password))
        user_id = cursor.fetchone()

        if user_id:
            self.user_window = UserWindow(user_id[0])
            self.user_window.show()
            self.close()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Неверный логин или пароль')

class UserWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.initUI()
        self.resize(400, 300)  # Установка размера окна

    def initUI(self):
        self.setWindowTitle('Пользователь - Главное меню')
        layout = QVBoxLayout()

        self.btn_profile = HoverButton('Мой профиль')
        self.btn_trainings = HoverButton('Тренировки')
        self.btn_my_trainings = HoverButton('Мои тренировки')
        self.btn_review = HoverButton('Оставить отзыв')

        self.btn_profile.setFixedSize(350, 50)
        self.btn_trainings.setFixedSize(350, 50)
        self.btn_my_trainings.setFixedSize(350, 50)
        self.btn_review.setFixedSize(350, 50)

        self.btn_profile.clicked.connect(self.openProfile)
        self.btn_trainings.clicked.connect(self.openTrainings)
        self.btn_my_trainings.clicked.connect(self.openMyTrainings)
        self.btn_review.clicked.connect(self.openReview)

        layout.addWidget(self.btn_profile)
        layout.addWidget(self.btn_trainings)
        layout.addWidget(self.btn_my_trainings)
        layout.addWidget(self.btn_review)

        self.setLayout(layout)

    def openProfile(self):
        cursor.execute('SELECT last_name, first_name, middle_name, age FROM users WHERE id = ?', (self.user_id,))
        profile = cursor.fetchone()

        profile_info = f'Фамилия: {profile[0]}\nИмя: {profile[1]}\nОтчество: {profile[2]}\nВозраст: {profile[3]}'
        QMessageBox.information(self, 'Мой профиль', profile_info)

    def openTrainings(self):
        self.trainings_window = UserTrainingsWindow(self.user_id)
        self.trainings_window.show()

    def openMyTrainings(self):
        self.my_trainings_window = MyTrainingsWindow(self.user_id)
        self.my_trainings_window.show()

    def openReview(self):
        self.review_window = ReviewWindow(self.user_id)
        self.review_window.show()

class UserTrainingsWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.initUI()
        self.resize(400, 150)  # Установка размера окна

    def initUI(self):
        self.setWindowTitle('Пользователь - Тренировки')
        layout = QVBoxLayout()

        self.day_combo = QComboBox()
        for i in range(1, 32):
            self.day_combo.addItem(str(i))

        self.btn_select_day = HoverButton('Выбрать день')
        self.btn_select_day.clicked.connect(self.selectDay)

        layout.addWidget(self.day_combo)
        layout.addWidget(self.btn_select_day)

        self.setLayout(layout)

    def selectDay(self):
        day = int(self.day_combo.currentText())
        self.day_window = UserDayTrainingsWindow(self.user_id, day)
        self.day_window.show()

class UserDayTrainingsWindow(QWidget):
    def __init__(self, user_id, day):
        super().__init__()
        self.user_id = user_id
        self.day = day
        self.initUI()
        self.resize(340, 300)  # Установка размера окна

    def initUI(self):
        self.setWindowTitle(f'Пользователь - Тренировки на {self.day} день')
        layout = QVBoxLayout()

        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Спорт', 'Время', 'Тренер'])

        self.loadTrainings()

        self.btn_select = HoverButton('Выбрать тренировку')
        self.btn_select.clicked.connect(self.selectTraining)

        layout.addWidget(self.table)
        layout.addWidget(self.btn_select)

        self.setLayout(layout)

    def loadTrainings(self):
        cursor.execute('SELECT sport, time, coach FROM trainings WHERE day = ?', (self.day,))
        trainings = cursor.fetchall()

        self.table.setRowCount(len(trainings))
        for row, training in enumerate(trainings):
            for col, item in enumerate(training):
                self.table.setItem(row, col, QTableWidgetItem(str(item)))

    def selectTraining(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            sport = self.table.item(selected_row, 0).text()
            time = self.table.item(selected_row, 1).text()
            coach = self.table.item(selected_row, 2).text()
            cursor.execute('SELECT id FROM trainings WHERE sport = ? AND time = ? AND coach = ? AND day = ?', (sport, time, coach, self.day))
            training_id = cursor.fetchone()[0]
            cursor.execute('INSERT INTO user_trainings (user_id, training_id, day) VALUES (?, ?, ?)', (self.user_id, training_id, self.day))
            conn.commit()
            QMessageBox.information(self, 'Успех', 'Вы успешно записались на тренировку')

class MyTrainingsWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.initUI()
        self.resize(420, 400)  # Установка размера окна

    def initUI(self):
        self.setWindowTitle('Пользователь - Мои тренировки')
        layout = QVBoxLayout()

        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Спорт', 'Время', 'Тренер', 'День'])

        self.loadTrainings()

        self.btn_delete = HoverButton('Удалить тренировку')
        self.btn_delete.clicked.connect(self.deleteTraining)

        layout.addWidget(self.table)
        layout.addWidget(self.btn_delete)

        self.setLayout(layout)

    def loadTrainings(self):
        cursor.execute('''SELECT t.sport, t.time, t.coach, ut.day
                          FROM user_trainings ut
                          JOIN trainings t ON ut.training_id = t.id
                          WHERE ut.user_id = ?
                          ORDER BY ut.day, t.time''', (self.user_id,))
        trainings = cursor.fetchall()

        self.table.setRowCount(len(trainings))
        for row, training in enumerate(trainings):
            for col, item in enumerate(training):
                self.table.setItem(row, col, QTableWidgetItem(str(item)))

    def deleteTraining(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            sport = self.table.item(selected_row, 0).text()
            time = self.table.item(selected_row, 1).text()
            coach = self.table.item(selected_row, 2).text()
            day = self.table.item(selected_row, 3).text()
            cursor.execute('SELECT id FROM trainings WHERE sport = ? AND time = ? AND coach = ? AND day = ?', (sport, time, coach, day))
            training_id = cursor.fetchone()[0]
            cursor.execute('DELETE FROM user_trainings WHERE user_id = ? AND training_id = ? AND day = ?', (self.user_id, training_id, day))
            conn.commit()
            QMessageBox.information(self, 'Успех', 'Вы успешно удалили тренировку')
            self.loadTrainings()

class ReviewWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.initUI()
        self.resize(400, 300)  # Установка размера окна

    def initUI(self):
        self.setWindowTitle('Пользователь - Оставить отзыв')
        layout = QVBoxLayout()

        self.lbl_rating = QLabel('Оценка:')
        self.rating_combo = QComboBox()
        for i in range(1, 6):
            self.rating_combo.addItem(str(i))

        self.lbl_review = QLabel('Отзыв:')
        self.txt_review = QTextEdit()

        self.btn_submit = HoverButton('Отправить отзыв')
        self.btn_submit.clicked.connect(self.submitReview)

        layout.addWidget(self.lbl_rating)
        layout.addWidget(self.rating_combo)
        layout.addWidget(self.lbl_review)
        layout.addWidget(self.txt_review)
        layout.addWidget(self.btn_submit)

        self.setLayout(layout)

    def submitReview(self):
        rating = int(self.rating_combo.currentText())
        review = self.txt_review.toPlainText()

        if not review:
            QMessageBox.warning(self, 'Ошибка', 'Отзыв не может быть пустым')
            return

        cursor.execute('INSERT INTO reviews (user_id, rating, review) VALUES (?, ?, ?)', (self.user_id, rating, review))
        conn.commit()
        QMessageBox.information(self, 'Успех', 'Отзыв успешно отправлен')
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())