import sqlite3
import random
import time
from datetime import datetime

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication, QMessageBox, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
import sys
from PyQt5 import uic
from PyQt5 import QtCore, QtWidgets

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class NullLine(Exception):
    pass


class CountNull(Exception):
    pass


class Window(QMainWindow):

    def __init__(self):

        super().__init__()
        uic.loadUi('LW.ui', self)

        self.succ_label.setHidden(True)
        self.succ2_label.setHidden(True)
        self.press_label.setHidden(True)

        self.add_functions()
        self.setWindowTitle("Authorization")

        self.is_secret = False

        self.count_secret = 0

    def add_functions(self):

        self.login_btn.clicked.connect(lambda: self.login_clicked(self.user_edit.text(), self.password_edit.text()))
        self.reg_btn.clicked.connect(lambda: self.reg_clicked(self.user_edit.text(), self.password_edit.text()))
        self.secret_btn.clicked.connect(self.secret_clicked)

    def reg_clicked(self, user, password):

        if user and password:

            with sqlite3.connect("Users_db.db") as db:

                t = int(time.time())

                cur = db.cursor()
                query = f'''INSERT INTO users(name, password, reg_date)
                            VALUES('{user}', '{password}', '{datetime.fromtimestamp(t)}')'''

                try:

                    ltry = cur.execute(f'''SELECT password
                                           FROM users
                                           WHERE name = '{user}' ''').fetchall()
                    if ltry:

                        aiberror = QMessageBox()
                        aiberror.setWindowTitle("Aib error!")
                        aiberror.setText("User already in base!")
                        aiberror.setIcon(QMessageBox.Icon.Warning)
                        aiberror.setStandardButtons(QMessageBox.Ok)
                        aiberror.setInformativeText("Try to log in using the entered data or come up "
                                                    "with a new username.")

                        aiberror.exec()

                    else:

                        raise sqlite3.OperationalError

                except sqlite3.OperationalError:

                    cur.execute(query)

                    self.succ2_label.setHidden(False)
                    self.press_label.setHidden(False)

                db.commit()

        else:

            if not password and not user:

                notpau = QMessageBox()
                notpau.setText("Enter your username and password!")
                notpau.setIcon(QMessageBox.Icon.Critical)
                notpau.setWindowTitle("Notpau error!")

                notpau.exec()

            elif not password and user:

                notp = QMessageBox()
                notp.setText("Enter your password!")
                notp.setIcon(QMessageBox.Icon.Critical)
                notp.setWindowTitle("Notp error!")

                notp.exec()

            else:

                notu = QMessageBox()
                notu.setText("Enter your username!")
                notu.setIcon(QMessageBox.Icon.Critical)
                notu.setWindowTitle("Notu error!")

                notu.exec()

    def login_clicked(self, user, password):

        if password and user:

            with sqlite3.connect("Users_db.db") as db:

                cur = db.cursor()
                query = f'''SELECT password
                            FROM users
                            WHERE name = '{user}' '''
                try:

                    pswrd = cur.execute(query).fetchone()

                    if pswrd:

                        if pswrd[0] == password:

                            self.succ_label.setHidden(False)

                            self.timer = QTimer()
                            self.timer.timeout.connect(self.show_main)
                            self.timer.start(750)

                        else:

                            wrongdata = QMessageBox()
                            wrongdata.setWindowTitle("Wrong data!")
                            wrongdata.setText("Incorrect login or password!")
                            wrongdata.setInformativeText("Try again.")
                            wrongdata.setIcon(QMessageBox.Icon.Critical)

                            wrongdata.exec()

                    else:
                        raise sqlite3.OperationalError

                except sqlite3.OperationalError:

                    niberror = QMessageBox()
                    niberror.setWindowTitle("Nib error!")
                    niberror.setText(f"There is no such username as '{user}' in the db!")
                    niberror.setInformativeText("Try to login with other data or register.")
                    niberror.setIcon(QMessageBox.Icon.Warning)
                    niberror.setStandardButtons(QMessageBox.Ok)

                    niberror.exec()

                db.commit()

        else:

            if not password and not user:

                notpau = QMessageBox()
                notpau.setText("Enter your username and password!")
                notpau.setIcon(QMessageBox.Icon.Critical)
                notpau.setWindowTitle("Notpau error!")

                notpau.exec()

            elif not password and user:

                notp = QMessageBox()
                notp.setText("Enter your password!")
                notp.setIcon(QMessageBox.Icon.Critical)
                notp.setWindowTitle("Notp error!")

                notp.exec()

            else:

                notu = QMessageBox()
                notu.setText("Enter your username!")
                notu.setIcon(QMessageBox.Icon.Critical)
                notu.setWindowTitle("Notu error!")

                notu.exec()

    def secret_clicked(self):

        self.count_secret += 1

        if not self.is_secret:

            pixmap = QPixmap("C:\ENGLISHPROGRAMM\PROGRAMM\images\SECRET\duosecretok.jpg")

            self.DuoPix_label.setPixmap(pixmap)
            self.is_secret = True

        else:

            pixmap = QPixmap("C:\ENGLISHPROGRAMM\PROGRAMM\images\Duo\DUOCOOLLW.jpg")

            self.DuoPix_label.setPixmap(pixmap)
            self.is_secret = False

    def show_main(self):

        self.timer.stop()

        self.setHidden(True)

        login = self.user_edit.text()

        with sqlite3.connect("Users_db.db") as db:
            cur = db.cursor()

            query = f'''UPDATE users
                        SET count_secret = count_secret + '{self.count_secret}'
                        WHERE name = '{login}' '''

            cur.execute(query)

        db.commit()

        self.main = MainWindow(login)
        self.main.show()


class MainWindow(QMainWindow):

    def __init__(self, login):

        super().__init__()
        uic.loadUi('MMW.ui', self)

        self.setWindowTitle("Main Menu")

        self.login = login

        self.jokePix_label.setHidden(True)
        self.profile_btn.setText(login)

        rand = random.randint(1, 2)

        pixmap = QPixmap(f"C:\ENGLISHPROGRAMM\PROGRAMM\images\Duo\{rand}")

        if rand == 1:

            self.Duo_label.resize(250, 190)
            self.Duo_label.move(480, 460)
            self.Duo_label.setPixmap(pixmap)

        else:

            self.Duo_label.resize(400, 190)
            self.Duo_label.move(400, 470)
            self.Duo_label.setPixmap(pixmap)

        self.add_functions()

    def add_functions(self):

        self.joketime_btn.clicked.connect(self.joke_time)
        self.profile_btn.clicked.connect(self.profile_clicked)
        self.lessons_btn.clicked.connect(self.lessons_clicked)
        self.leaderboard_btn.clicked.connect(self.leaderboard_clicked)

    def leaderboard_clicked(self):

        self.setHidden(True)

        self.leadeboard = LeaderBoard(self.login)
        self.leadeboard.show()

    def lessons_clicked(self):

        self.setHidden(True)

        self.lessons = Lessons(self.login)
        self.lessons.show()

    def profile_clicked(self):

        self.setHidden(True)

        self.profile = ProfileStats(self.login)
        self.profile.show()

    def joke_time(self):

        self.Duo_label.setHidden(True)

        self.lessons_btn.move(10, 150)
        self.leaderboard_btn.move(10, 270)
        self.joketime_btn.move(10, 390)
        self.jokePix_label.move(410, 70)
        self.profile_btn.move(70, 10)

        self.jokePix_label.setHidden(False)

        pixmap = QPixmap(f"C:\ENGLISHPROGRAMM\PROGRAMM\images\Memes\{random.randint(1, 6)}")
        self.jokePix_label.setPixmap(pixmap)


class Exercise(QMainWindow):

    def __init__(self):
        super().__init__()


class ProfileStats(QMainWindow):

    def __init__(self, login):
        super().__init__()
        uic.loadUi("SW.ui", self)

        self.setWindowTitle("Profile Stats")

        self.login = login

        self.stats_profile_btn.setText(login)

        with sqlite3.connect("Users_db.db") as db:
            cur = db.cursor()

            query = f'''SELECT count_exercise, count_secret, count_less, reg_date
                        FROM users
                        WHERE name = '{self.login}' '''

            lst = cur.execute(query).fetchone()

        self.reg_date.setText(str(lst[3]))
        self.count_less.setText(str(lst[2]))
        self.count_click.setText(str(lst[1]))
        self.count_exercise.setText(str(lst[0]))

        self.add_function()

        db.commit()

    def add_function(self):
        self.back_btn.clicked.connect(self.back_clicked)

    def back_clicked(self):
        self.setHidden(True)

        self.main = MainWindow(self.login)
        self.main.show()


class LeaderBoard(QMainWindow):

    def __init__(self, login):
        super().__init__()
        uic.loadUi("LBW.ui", self)

        self.login = login

        self.setWindowTitle("Leaderboard")

        with sqlite3.connect("Users_db.db") as db:
            cur = db.cursor()
            query = '''SELECT name, count_less
                       FROM users'''

            self.lst = sorted(cur.execute(query).fetchmany(5), key=lambda x: x[1], reverse=True)

            self.nick_1.setText(str(self.lst[0][0]))
            self.count_1.setText(str(self.lst[0][1]))

            self.initUi()

        db.commit()
        self.back_btn.clicked.connect(self.back_clicked)

    def initUi(self):
        for i in range(1, len(self.lst)):
            self.nick = QLabel(str(self.lst[i][0]), self)
            self.nick.move(310, 75 * (i + 1))
            self.nick.resize(171, 21)

            self.count = QLabel(str(self.lst[i][1]), self)
            self.count.move(500, 75 * (i + 1))
            self.count.resize(91, 20)

            self.num = QLabel(str(i + 1), self)
            self.num.move(220, 74 * (i + 1))
            self.num.resize(51, 31)

            self.nick.show()
            self.count.show()
            self.num.show()

    def back_clicked(self):
        self.setHidden(True)

        self.main = MainWindow(self.login)
        self.main.show()


class Lessons(QMainWindow):

    def __init__(self, login):
        super().__init__()
        uic.loadUi("LSNS.ui", self)

        self.setWindowTitle("Lessons")

        self.login = login

        self.add_functions()

        self.line_1.hide()
        self.line_2.hide()
        self.line_3.hide()
        self.line_4.hide()
        self.line_5.hide()
        self.topic_label.hide()
        self.count_ex_label.hide()
        self.start_btn.hide()

    def add_functions(self):

        self.lesson_1_btn.clicked.connect(self.lesson_information)
        self.lesson_2_btn.clicked.connect(self.lesson_information)
        self.lesson_3_btn.clicked.connect(self.lesson_information)
        self.lesson_4_btn.clicked.connect(self.lesson_information)
        self.lesson_5_btn.clicked.connect(self.lesson_information)
        self.start_btn.clicked.connect(self.start_lesson)
        self.back_btn.clicked.connect(self.back_clicked)

    def lesson_information(self):

        number = self.sender().text()[-1]
        self.number = number

        with sqlite3.connect("Lessons.db") as db:

            cur = db.cursor()
            query = f'''SELECT topic, count_ex
                               FROM lessons
                               WHERE id = '{self.number}' '''

            data = cur.execute(query).fetchone()

            db.commit()

        self.line_1.hide()
        self.line_2.hide()
        self.line_3.hide()
        self.line_4.hide()
        self.line_5.hide()

        self.topic_label.show()
        self.count_ex_label.show()
        self.start_btn.show()

        if number == '1':

            self.line_1.show()

        elif number == '2':
            self.line_2.show()

        elif number == '3':
            self.line_3.show()

        elif number == '4':
            self.line_4.show()

        elif number == '5':
            self.line_5.show()

        self.topic_label.move(830, 80 + 100 * (int(number) - 1))
        self.count_ex_label.move(840, 120 + 100 * (int(number) - 1))
        self.start_btn.move(800, 170 + 100 * (int(number) - 1))

        self.topic_label.setText(f"Тема: {data[0]}")
        self.count_ex_label.setText(f"{data[1]} заданий")

    def start_lesson(self):

        self.setHidden(True)

        self.lesswin = LessonWindow(self.login, self.number)
        self.lesswin.show()

    def back_clicked(self):
        self.setHidden(True)

        self.main = MainWindow(self.login)
        self.main.show()


class LessonWindow(QMainWindow):

    def __init__(self, login, id):
        super().__init__()

        self.login = login
        self.id = id

        with sqlite3.connect("Lessons.db") as db:

            cur = db.cursor()

            self.type = cur.execute(f'''SELECT type
                                       FROM lessons
                                       WHERE id = '{self.id}' ''').fetchone()[0]

            db.commit()

        if self.type == 1:

            self.first_type()

        else:

            self.second_type()

    def second_type(self):

        uic.loadUi("LST2.ui", self)

        self.c_label.hide()
        self.unc_label.hide()
        self.cunc_label.hide()
        self.next_btn.hide()
        self.duo_pix.hide()

        self.count = 1
        self.correct_answers = 0
        self.cool = 0

        with sqlite3.connect("Lessons.db") as db:
            cur = db.cursor()
            query = f'''SELECT exercise_1
            FROM lessons
            WHERE id = '{self.id}' '''

            self.lst = cur.execute(query).fetchone()[0].split(';')
            self.len_lst = len(cur.execute(f'''SELECT *
                                          FROM lessons
                                          WHERE id = '{self.id}' ''').fetchone()) - 4

            self.ex_text.setText(self.lst[0])

            self.right = self.lst[1]

        db.commit()

        self.add_functions_2()

    def add_functions_2(self):

        self.next_btn.clicked.connect(self.next_clicked_2)
        self.exit_btn.clicked.connect(self.exit_clicked)
        self.check_btn.clicked.connect(self.check_clicked_2)

    def next_clicked_2(self):

        self.count += 1

        self.c_label.hide()
        self.unc_label.hide()
        self.cunc_label.hide()
        self.duo_pix.hide()
        self.next_btn.hide()

        self.aedit.setText("")

        with sqlite3.connect("Lessons.db") as db:
            cur = db.cursor()
            query = f'''SELECT exercise_{self.count}
            FROM lessons
            WHERE id = '{self.id}' '''

            self.lst = cur.execute(query).fetchone()[0].split(';')

            self.ex_text.setText(self.lst[0])

            self.right = self.lst[1]

        db.commit()

        self.check_btn.setEnabled(True)

    def check_clicked_2(self):

        if self.aedit.text() == self.right:
            self.c_label.show()
            self.duo_pix.show()

            self.check_btn.setEnabled(False)

            self.correct_answers += 1

        else:

            self.unc_label.show()
            self.cunc_label.show()
            self.cunc_label.setText(f"Correct answer - {self.right}.")

            self.check_btn.setEnabled(False)

        if self.count != self.len_lst - 5:

            self.next_btn.show()

        else:

            if self.correct_answers == self.len_lst:
                self.cool = 1

            self.perocorran = int(self.correct_answers / (self.len_lst - 5) * 100)

            self.timer = QTimer()
            self.timer.timeout.connect(self.WinWinOp)
            self.timer.start(750)

    def first_type(self):

        uic.loadUi("LS.ui", self)

        self.c_label.hide()
        self.unc_label.hide()
        self.cunc_label.hide()
        self.next_btn.hide()
        self.duo_pix.hide()

        self.count = 1
        self.correct_answers = 0
        self.cool = 0

        with sqlite3.connect("Lessons.db") as db:
            cur = db.cursor()
            query = f'''SELECT exercise_1
            FROM lessons
            WHERE id = '{self.id}' '''

            self.lst = cur.execute(query).fetchone()[0].split(';')
            self.len_lst = cur.execute(f'''SELECT *
                                          FROM lessons
                                          WHERE id = '{self.id}' ''').fetchone()

            self.ex_text.setText(self.lst[0])

            self.fanswer_btn.setText(self.lst[1])
            self.sanswer_btn.setText(self.lst[2])
            self.tanswer_btn.setText(self.lst[3])

            self.right = self.lst[4]

        db.commit()

        self.add_functions()

    def add_functions(self):

        self.next_btn.clicked.connect(self.next_clicked)
        self.exit_btn.clicked.connect(self.exit_clicked)
        self.check_btn.clicked.connect(self.check_clicked)
        self.fanswer_btn.toggled.connect(lambda fanswer_btn: self.answer_clicked(self.fanswer_btn.text()))
        self.sanswer_btn.toggled.connect(lambda sanswer_btn: self.answer_clicked(self.sanswer_btn.text()))
        self.tanswer_btn.toggled.connect(lambda tanswer_btn: self.answer_clicked(self.tanswer_btn.text()))

    def answer_clicked(self, text):

        self.answer = text

    def check_clicked(self):

        if self.fanswer_btn.isChecked():

            self.answer_clicked(self.fanswer_btn.text())

        elif self.sanswer_btn.isChecked():

            self.answer_clicked(self.sanswer_btn.text())

        elif self.tanswer_btn.isChecked():

            self.answer_clicked(self.tanswer_btn.text())

        if self.lst[int(self.right)] == self.answer:

            self.c_label.show()
            self.duo_pix.show()

            self.check_btn.setEnabled(False)
            self.correct_answers += 1

        else:

            self.unc_label.show()
            self.cunc_label.show()
            self.cunc_label.setText(f"Correct answer - {self.right}.")

            self.check_btn.setEnabled(False)

        if self.count + 4 != len(self.len_lst):

            self.next_btn.show()

        else:

            if self.correct_answers == len(self.len_lst) - 4:
                self.cool = 1

            self.perocorran = int(self.correct_answers / (len(self.len_lst) - 4) * 100)

            self.timer = QTimer()
            self.timer.timeout.connect(self.WinWinOp)
            self.timer.start(750)

    def WinWinOp(self):

        self.setHidden(True)

        self.win = WinWindow(self.login, self.correct_answers, self.perocorran, self.cool)
        self.win.show()

        self.timer.stop()

    def next_clicked(self):

        self.count += 1

        self.c_label.hide()
        self.unc_label.hide()
        self.cunc_label.hide()
        self.duo_pix.hide()
        self.next_btn.hide()

        with sqlite3.connect("Lessons.db") as db:
            cur = db.cursor()
            query = f'''SELECT exercise_{self.count}
            FROM lessons
            WHERE id = '{self.id}' '''

            self.lst = cur.execute(query).fetchone()[0].split(';')

            self.ex_text.setText(self.lst[0])

            self.fanswer_btn.setText(self.lst[1])
            self.sanswer_btn.setText(self.lst[2])
            self.tanswer_btn.setText(self.lst[3])

            self.right = self.lst[4]

        db.commit()

        self.check_btn.setEnabled(True)

    def exit_clicked(self):

        question = QMessageBox()
        question.setWindowTitle("Attention!")
        question.setText("Are you sure?")
        question.setInformativeText("If you exit, the progress won't be saved.")
        question.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        question.setIcon(QMessageBox.Icon.Question)

        question.buttonClicked.connect(self.yn_clicked)

        question.exec()

    def yn_clicked(self, btn):

        if btn.text() == "&Yes":
            self.setHidden(True)

            self.main = MainWindow(self.login)
            self.main.show()


class WinWindow(QMainWindow):

    def __init__(self, login, nocorran, perocorran, cool):
        super().__init__()
        uic.loadUi("WW.ui", self)

        self.login = login
        self.nocorran = nocorran
        self.percorran = perocorran
        self.cool = cool

        self.num_label.setText(str(self.nocorran))
        self.per_label.setText(str(self.percorran))

        with sqlite3.connect("Users_db.db") as db:
            cur = db.cursor()
            query = f'''UPDATE users
            SET count_exercise = count_exercise + '{self.nocorran}'
            WHERE name = '{self.login}' '''

            query2 = f'''UPDATE users
                         SET count_less = count_less + '{self.cool}' 
                         WHERE name = '{self.login}' '''

            cur.execute(query)
            cur.execute(query2)

            db.commit()

        self.exit_btn.clicked.connect(self.exit_clicked)

    def exit_clicked(self):
        self.setHidden(True)

        self.main = MainWindow(self.login)
        self.main.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
