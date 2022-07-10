import sys

import psycopg2
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from datetime import timedelta, datetime
import calendar
from datetime import date


class MainWindow(QMainWindow):  # главное окно
    def __init__(self, parent=None):
        super().__init__(parent)

        self.date_today = None
        self.category = None
        self.button_edit_family = None
        self.button_delete_family = None
        self.button_info_family = None
        self.list_family = None
        self.button_add_family = None
        self.index_family = []
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Семейный бюджет")  # Заголовок окна
        self.resize(1200, 480)  # Размер окна
        self.center()  # Окно по центу

        self.date_today = False
        self.date_week = False
        self.date_month = False
        self.number_income = False

        " СОСТАВ СЕМЬИ "

        self.family = QGroupBox('Состав семьи', self)
        self.family.setGeometry(QRect(25, 9, 270, 190))
        self.family.setAlignment(Qt.AlignCenter)
        self.family.setFont(QFont("Roboto", 14))

        self.list_family = QListWidget(self.family)
        self.list_family.setFont(QFont("Roboto", 13))
        self.list_family.setGeometry(QRect(10, 35, 250, 107))
        self.list_family.currentRowChanged.connect(self.update_table)

        self.button_add_family = QPushButton('Добавить', self.family)
        self.button_add_family.setGeometry(QRect(10, 150, 80, 30))
        self.button_add_family.setFont(QFont("Roboto", 13))
        self.button_add_family.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
        self.button_add_family.clicked.connect(self.show_window_add_family)

        self.button_info_family = QPushButton('Сведения', self.family)
        self.button_info_family.setGeometry(QRect(95, 150, 80, 30))
        self.button_info_family.setFont(QFont("Roboto", 13))
        self.button_info_family.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
        self.button_info_family.clicked.connect(self.show_window_info_family)

        self.button_delete_family = QPushButton('Удалить', self.family)
        self.button_delete_family.setGeometry(QRect(180, 150, 80, 30))
        self.button_delete_family.setFont(QFont("Roboto", 13))
        self.button_delete_family.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
        self.button_delete_family.clicked.connect(self.delete_member_family)

        " СОСТАВ СЕМЬИ "

        " ПЕРИОД "

        period = QGroupBox('Период', self)
        period.setGeometry(QRect(915, 175, 270, 175))
        period.setAlignment(Qt.AlignCenter)
        period.setFont(QFont("Roboto", 14))

        label = QLabel('<b>С<b/>', period)
        label.setFont(QFont("Roboto", 10))
        label.setGeometry(10, 40, 20, 25)

        label = QLabel('<b>ПО<b/>', period)
        label.setFont(QFont("Roboto", 10))
        label.setGeometry(135, 40, 20, 25)

        self.date_begin = QDateTimeEdit(QDate.currentDate(), period)
        self.date_begin.setGeometry(20, 35, 110, 25)
        self.date_begin.setFont(QFont("Roboto", 12))
        self.date_begin.setTimeSpec(Qt.LocalTime)
        self.date_begin.setDisplayFormat("dd.MM.yyyy")

        self.date_end = QDateTimeEdit(QDate.currentDate(), period)
        self.date_end.setGeometry(155, 35, 110, 25)
        self.date_end.setFont(QFont("Roboto", 12))
        self.date_end.setTimeSpec(Qt.LocalTime)
        self.date_end.setDisplayFormat("dd.MM.yyyy")
        self.date_end.setTimeSpec(Qt.LocalTime)

        self.button_perform_period = QPushButton('Применить фильтр', period)
        self.button_perform_period.setGeometry(QRect(10, 65, 250, 30))
        self.button_perform_period.setFont(QFont("Roboto", 13))
        self.button_perform_period.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
        self.button_perform_period.clicked.connect(self.click_button_perform_period)

        self.button_date_today = QPushButton('Сегодня', period)
        self.button_date_today.setGeometry(QRect(10, 100, 80, 30))
        self.button_date_today.setFont(QFont("Roboto", 13))
        self.button_date_today.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
        self.button_date_today.clicked.connect(self.click_button_date_today)

        self.button_date_week = QPushButton('Неделя', period)
        self.button_date_week.setGeometry(QRect(95, 100, 80, 30))
        self.button_date_week.setFont(QFont("Roboto", 13))
        self.button_date_week.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
        self.button_date_week.clicked.connect(self.click_button_date_week)

        self.button_date_month = QPushButton('Месяц', period)
        self.button_date_month.setGeometry(QRect(180, 100, 80, 30))
        self.button_date_month.setFont(QFont("Roboto", 13))
        self.button_date_month.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
        self.button_date_month.clicked.connect(self.click_button_date_month)

        button_clear_period = QPushButton('Сбросить фильтр', period)
        button_clear_period.setGeometry(QRect(10, 135, 250, 30))
        button_clear_period.setFont(QFont("Roboto", 13))
        button_clear_period.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
        button_clear_period.clicked.connect(self.click_button_clear_filter)

        " ПЕРИОД "

        " ДОХОД/РАСХОД "

        self.filter = QGroupBox('Доход', self)
        self.filter.setGeometry(QRect(915, 355, 270, 115))
        self.filter.setAlignment(Qt.AlignCenter)
        self.filter.setFont(QFont("Roboto", 14))

        self.comboBox_math = QComboBox(self.filter)
        self.comboBox_math.setGeometry(QRect(10, 35, 40, 30))
        self.comboBox_math.setFont(QFont("Roboto", 13))
        self.comboBox_math.addItems(['<', '>', '='])

        self.line_math = QLineEdit(self.filter)
        self.line_math.setFont(QFont("Roboto", 13))
        self.line_math.setGeometry(QRect(55, 35, 125, 30))

        self.button_math = QPushButton('Найти', self.filter)
        self.button_math.setGeometry(QRect(190, 35, 70, 30))
        self.button_math.setFont(QFont("Roboto", 13))
        self.button_math.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
        self.button_math.clicked.connect(self.click_button_math)

        button_clear_math = QPushButton('Сбросить фильтр', self.filter)
        button_clear_math.setGeometry(QRect(10, 75, 250, 30))
        button_clear_math.setFont(QFont("Roboto", 13))
        button_clear_math.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
        button_clear_math.clicked.connect(self.click_button_clear_math)

        " ДОХОД/РАСХОД "

        " КАТЕГОРИИ "

        self.category = QGroupBox('Категории', self)
        self.category.setGeometry(QRect(915, 10, 270, 160))
        self.category.setAlignment(Qt.AlignCenter)
        self.category.setFont(QFont("Roboto", 14))

        self.index_category = []
        self.list_category = QListWidget(self.category)
        self.list_category.setFont(QFont("Roboto", 13))
        self.list_category.setGeometry(QRect(10, 35, 150, 110))

        self.button_add_category = QPushButton('Добавить', self.category)
        self.button_add_category.setGeometry(QRect(170, 35, 90, 50))
        self.button_add_category.setFont(QFont("Roboto", 13))
        self.button_add_category.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
        self.button_add_category.clicked.connect(self.click_button_add_category)

        self.button_delete_category = QPushButton('Удалить', self.category)
        self.button_delete_category.setGeometry(QRect(170, 95, 90, 50))
        self.button_delete_category.setFont(QFont("Roboto", 13))
        self.button_delete_category.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
        self.button_delete_category.clicked.connect(self.delete_category)

        " КАТЕГОРИИ "

        self.tabs = QTabWidget(self)
        self.tabs.setFont(QFont("Roboto", 14))
        self.tabs.setGeometry(QRect(320, 5, 592, 465))

        " ВКЛАДКА ДОХОДЫ "

        tab_income = QWidget()
        self.tabs.addTab(tab_income, "   Доходы   ")

        self.income = QGroupBox(' Добавить доход', tab_income)
        self.income.setFont(QFont("Roboto", 14))
        self.income.setGeometry(QRect(9, 5, 555, 70))

        self.comboBox_member_income = QComboBox(self.income)
        self.comboBox_member_income.setFont(QFont("Roboto", 12))
        self.comboBox_member_income.setGeometry(QRect(10, 35, 180, 25))

        self.dateEdit_income = QDateTimeEdit(QDateTime.currentDateTime(), self.income)
        self.dateEdit_income.setFont(QFont("Roboto", 12))
        self.dateEdit_income.setDisplayFormat("dd.MM.yyyy")
        self.dateEdit_income.setCalendarPopup(True)
        self.dateEdit_income.setTimeSpec(Qt.LocalTime)
        self.dateEdit_income.setGeometry(QRect(195, 35, 110, 25))

        self.comboBox_category_add_income = QComboBox(self.income)
        self.comboBox_category_add_income.setFont(QFont("Roboto", 10))
        self.comboBox_category_add_income.setGeometry(QRect(310, 35, 95, 25))

        self.line_income = QLineEdit(self.income)
        self.line_income.setFont(QFont("Roboto", 12))
        self.line_income.setGeometry(QRect(410, 35, 100, 25))

        button_income = QPushButton(self.income)
        button_income.setGeometry(QRect(520, 35, 25, 25))
        button_income.setIcon(QIcon('check.png'))
        button_income.clicked.connect(self.click_button_add_income)

        self.index_income = []
        self.table_income = QTableWidget(tab_income)
        self.table_income.setFont(QFont("Roboto", 12))
        self.table_income.verticalHeader().setVisible(False)
        self.table_income.setGeometry(QRect(9, 90, 570, 325))
        self.table_income.horizontalHeader().setDefaultSectionSize(106)
        self.table_income.setColumnCount(5)
        self.table_income.setRowCount(11)
        self.table_income.setShowGrid(False)
        self.table_income.setStyleSheet('QTableView::item {border-bottom: 1px solid #d6d9dc;}')
        self.table_income.setHorizontalHeaderLabels(["Член семьи", "Дата", "Категория", "Доход", ''])
        self.table_income.setColumnWidth(0, 200)
        self.table_income.setColumnWidth(1, 100)
        self.table_income.setColumnWidth(3, 105)
        self.table_income.setColumnWidth(4, 20)

        " ВКЛАДКА ДОХОДЫ  "

        " ВКЛАДКА РАСХОДЫ "

        tab_expense = QWidget()
        self.tabs.addTab(tab_expense, "  Расходы  ")
        self.expense = QGroupBox(' Добавить расход', tab_expense)
        self.expense.setFont(QFont("Roboto", 14))
        self.expense.setGeometry(QRect(9, 5, 555, 70))

        self.comboBox_member_expense = QComboBox(self.expense)
        self.comboBox_member_expense.setFont(QFont("Roboto", 12))
        self.comboBox_member_expense.setGeometry(QRect(10, 35, 180, 25))

        self.dateEdit_expense = QDateTimeEdit(QDateTime.currentDateTime(), self.expense)
        self.dateEdit_expense.setFont(QFont("Roboto", 12))
        self.dateEdit_expense.setDisplayFormat("dd.MM.yyyy")
        self.dateEdit_expense.setCalendarPopup(True)
        self.dateEdit_expense.setTimeSpec(Qt.LocalTime)
        self.dateEdit_expense.setGeometry(QRect(195, 35, 110, 25))

        self.comboBox_category_add_expense = QComboBox(self.expense)
        self.comboBox_category_add_expense.setFont(QFont("Roboto", 10))
        self.comboBox_category_add_expense.setGeometry(QRect(310, 35, 95, 25))

        self.line_expense = QLineEdit(self.expense)
        self.line_expense.setFont(QFont("Roboto", 12))
        self.line_expense.setGeometry(QRect(410, 35, 100, 25))

        button_expense = QPushButton(self.expense)
        button_expense.setGeometry(QRect(520, 35, 25, 25))
        button_expense.setIcon(QIcon('check.png'))
        button_expense.clicked.connect(self.click_button_add_expense)

        self.index_expense = []
        self.table_expense = QTableWidget(tab_expense)
        self.table_expense.setFont(QFont("Roboto", 12))
        self.table_expense.verticalHeader().setVisible(False)
        self.table_expense.setGeometry(QRect(9, 90, 570, 325))
        self.table_expense.horizontalHeader().setDefaultSectionSize(106)
        self.table_expense.setColumnCount(5)
        self.table_expense.setRowCount(11)
        self.table_expense.setShowGrid(False)
        self.table_expense.setStyleSheet('QTableView::item {border-bottom: 1px solid #d6d9dc;}')
        self.table_expense.setHorizontalHeaderLabels(["Член семьи", "Дата", "Категория", "Доход", ''])
        self.table_expense.setColumnWidth(0, 200)
        self.table_expense.setColumnWidth(1, 100)
        self.table_expense.setColumnWidth(3, 105)
        self.table_expense.setColumnWidth(4, 20)

        " ВКЛАДКА РАСХОДЫ "

        " ВКЛАДКА СБЕР. СЧЕТ "

        tab_savings_account = QWidget()
        self.tabs.addTab(tab_savings_account, "Сберегательные счета")
        savings_account = QGroupBox(' Добавить сберегательный счет', tab_savings_account)
        savings_account.setFont(QFont("Roboto", 14))
        savings_account.setGeometry(QRect(10, 5, 555, 140))

        label = QLabel('Член семьи', savings_account)
        label.setFont(QFont("Roboto", 11))
        label.setGeometry(QRect(10, 37, 85, 25))

        self.comboBox_member_savings_account = QComboBox(savings_account)
        self.comboBox_member_savings_account.setFont(QFont("Roboto", 12))
        self.comboBox_member_savings_account.setGeometry(QRect(130, 35, 115, 25))

        label = QLabel('Название банка', savings_account)
        label.setFont(QFont("Roboto", 11))
        label.setGeometry(QRect(265, 37, 110, 25))

        self.comboBox_bank_savings_account = QComboBox(savings_account)
        self.comboBox_bank_savings_account.setFont(QFont("Roboto", 12))
        self.comboBox_bank_savings_account.setGeometry(QRect(410, 35, 100, 25))

        label = QLabel('Сумма вклада', savings_account)
        label.setFont(QFont("Roboto", 11))
        label.setGeometry(QRect(10, 70, 105, 25))

        self.line_deposit_amount = QLineEdit(savings_account)
        self.line_deposit_amount.setFont(QFont("Roboto", 12))
        self.line_deposit_amount.setGeometry(QRect(130, 70, 115, 25))

        label = QLabel('Процентная ставка', savings_account)
        label.setFont(QFont("Roboto", 11))
        label.setGeometry(QRect(265, 70, 140, 25))

        self.line_interest_rate = QLineEdit(savings_account)
        self.line_interest_rate.setFont(QFont("Roboto", 12))
        self.line_interest_rate.setGeometry(QRect(410, 70, 100, 25))

        label = QLabel('Дата вложения', savings_account)
        label.setFont(QFont("Roboto", 11))
        label.setGeometry(QRect(10, 105, 115, 25))

        self.dateEdit_savings_account = QDateTimeEdit(QDateTime.currentDateTime(), savings_account)
        self.dateEdit_savings_account.setFont(QFont("Roboto", 12))
        self.dateEdit_savings_account.setDisplayFormat("dd.MM.yyyy")
        self.dateEdit_savings_account.setCalendarPopup(True)
        self.dateEdit_savings_account.setTimeSpec(Qt.LocalTime)
        self.dateEdit_savings_account.setGeometry(QRect(130, 105, 115, 25))

        label = QLabel('Срок хранения', savings_account)
        label.setFont(QFont("Roboto", 11))
        label.setGeometry(QRect(265, 105, 100, 25))

        self.line_term = QLineEdit(savings_account)
        self.line_term.setFont(QFont("Roboto", 12))
        self.line_term.setGeometry(QRect(410, 105, 100, 25))

        button_savings_account = QPushButton(savings_account)
        button_savings_account.setGeometry(QRect(520, 105, 25, 25))
        button_savings_account.setIcon(QIcon('check.png'))
        button_savings_account.clicked.connect(self.add_savings_account)

        self.index_savings_account = []
        self.table_savings_account = QTableWidget(tab_savings_account)
        self.table_savings_account.setFont(QFont("Roboto", 12))
        self.table_savings_account.verticalHeader().setVisible(False)
        self.table_savings_account.setGeometry(QRect(10, 160, 570, 265))
        self.table_savings_account.horizontalHeader().setDefaultSectionSize(106)
        self.table_savings_account.setColumnCount(5)
        self.table_savings_account.setRowCount(11)
        self.table_savings_account.setShowGrid(False)
        self.table_savings_account.setStyleSheet('QTableView::item {border-bottom: 1px solid #d6d9dc;}')
        self.table_savings_account.setHorizontalHeaderLabels(["Член семьи", "Дата", "Категория", "Доход", ''])
        self.table_savings_account.setColumnWidth(0, 200)
        self.table_savings_account.setColumnWidth(1, 100)
        self.table_savings_account.setColumnWidth(3, 105)
        self.table_savings_account.setColumnWidth(4, 20)

        " ВКЛАДКА СБЕР. СЧЕТ "

        " ВКЛАДКА КРЕДИТ "

        tab_credit = QWidget()
        self.tabs.addTab(tab_credit, "  Кредиты  ")
        credit = QGroupBox('Добавить кредит', tab_credit)
        credit.setFont(QFont("Roboto", 14))
        credit.setGeometry(QRect(10, 5, 555, 140))

        label = QLabel('Член семьи', credit)
        label.setFont(QFont("Roboto", 11))
        label.setGeometry(QRect(10, 37, 85, 25))

        self.comboBox_member_savings_credit = QComboBox(credit)
        self.comboBox_member_savings_credit.setFont(QFont("Roboto", 12))
        self.comboBox_member_savings_credit.setGeometry(QRect(130, 35, 115, 25))

        label = QLabel('Название банка', credit)
        label.setFont(QFont("Roboto", 11))
        label.setGeometry(QRect(265, 37, 110, 25))

        self.comboBox_bank_credit = QComboBox(credit)
        self.comboBox_bank_credit.setFont(QFont("Roboto", 12))
        self.comboBox_bank_credit.setGeometry(QRect(410, 35, 100, 25))

        label = QLabel('Сумма кредита', credit)
        label.setFont(QFont("Roboto", 11))
        label.setGeometry(QRect(10, 70, 105, 25))

        self.line_loan_amount = QLineEdit(credit)
        self.line_loan_amount.setFont(QFont("Roboto", 12))
        self.line_loan_amount.setGeometry(QRect(130, 70, 115, 25))

        label = QLabel('Процентная ставка', credit)
        label.setFont(QFont("Roboto", 11))
        label.setGeometry(QRect(265, 70, 140, 25))

        self.line_interest_rate_credit = QLineEdit(credit)
        self.line_interest_rate_credit.setFont(QFont("Roboto", 12))
        self.line_interest_rate_credit.setGeometry(QRect(410, 70, 100, 25))

        label = QLabel('Дата взятия', credit)
        label.setFont(QFont("Roboto", 11))
        label.setGeometry(QRect(10, 105, 115, 25))

        self.dateEdit_credit = QDateTimeEdit(QDateTime.currentDateTime(), credit)
        self.dateEdit_credit.setFont(QFont("Roboto", 12))
        self.dateEdit_credit.setDisplayFormat("dd.MM.yyyy")
        self.dateEdit_credit.setCalendarPopup(True)
        self.dateEdit_credit.setTimeSpec(Qt.LocalTime)
        self.dateEdit_credit.setGeometry(QRect(130, 105, 115, 25))

        label = QLabel('Срок кредита', credit)
        label.setFont(QFont("Roboto", 11))
        label.setGeometry(QRect(265, 105, 100, 25))

        self.line_term_credit = QLineEdit(credit)
        self.line_term_credit.setFont(QFont("Roboto", 12))
        self.line_term_credit.setGeometry(QRect(410, 105, 100, 25))

        button_credit = QPushButton(credit)
        button_credit.setGeometry(QRect(520, 105, 25, 25))
        button_credit.setIcon(QIcon('check.png'))
        button_credit.clicked.connect(self.add_credit)

        self.index_credit = []
        self.table_credit = QTableWidget(tab_credit)
        self.table_credit.setFont(QFont("Roboto", 12))
        self.table_credit.verticalHeader().setVisible(False)
        self.table_credit.setGeometry(QRect(10, 160, 570, 265))
        self.table_credit.horizontalHeader().setDefaultSectionSize(106)
        self.table_credit.setColumnCount(5)
        self.table_credit.setRowCount(11)
        self.table_credit.setShowGrid(False)
        self.table_credit.setStyleSheet('QTableView::item {border-bottom: 1px solid #d6d9dc;}')
        self.table_credit.setHorizontalHeaderLabels(["Член семьи", "Дата", "Категория", "Доход", ''])
        self.table_credit.setColumnWidth(0, 200)
        self.table_credit.setColumnWidth(1, 100)
        self.table_credit.setColumnWidth(3, 105)
        self.table_credit.setColumnWidth(4, 20)

        " ВКЛАДКА КРЕДИТ "

        " СТАТИСТИКА "

        static = QGroupBox('Общая статистика', self)
        static.setGeometry(QRect(5, 210, 310, 260))
        static.setAlignment(Qt.AlignCenter)
        static.setFont(QFont("Roboto", 14))

        group_box = QGroupBox('За сегодня', static)
        group_box.setAlignment(Qt.AlignCenter)
        group_box.setGeometry(QRect(10, 30, 290, 70))
        group_box.setFont(QFont("Roboto", 11))

        label = QLabel('Доход', group_box)
        label.setGeometry(QRect(0, 20, 100, 30))
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Roboto", 11))

        self.income_today = QLabel('0', group_box)
        self.income_today.setGeometry(QRect(0, 40, 100, 30))
        self.income_today.setAlignment(Qt.AlignCenter)
        self.income_today.setFont(QFont("Roboto", 10))

        label = QLabel('Расход', group_box)
        label.setGeometry(QRect(95, 20, 100, 30))
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Roboto", 11))

        self.expense_today = QLabel('0', group_box)
        self.expense_today.setGeometry(QRect(95, 40, 100, 30))
        self.expense_today.setAlignment(Qt.AlignCenter)
        self.expense_today.setFont(QFont("Roboto", 10))

        label = QLabel('Итогo', group_box)
        label.setGeometry(QRect(190, 20, 100, 30))
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Roboto", 11))

        self.sum_today = QLabel('0', group_box)
        self.sum_today.setGeometry(QRect(190, 40, 100, 30))
        self.sum_today.setAlignment(Qt.AlignCenter)
        self.sum_today.setFont(QFont("Roboto", 10))

        group_box = QGroupBox('За неделю', static)
        group_box.setAlignment(Qt.AlignCenter)
        group_box.setGeometry(QRect(10, 105, 290, 70))
        group_box.setFont(QFont("Roboto", 11))

        label = QLabel('Доход', group_box)
        label.setGeometry(QRect(0, 20, 100, 30))
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Roboto", 11))

        self.income_week = QLabel('0', group_box)
        self.income_week.setGeometry(QRect(0, 40, 100, 30))
        self.income_week.setAlignment(Qt.AlignCenter)
        self.income_week.setFont(QFont("Roboto", 10))

        label = QLabel('Расход', group_box)
        label.setGeometry(QRect(95, 20, 100, 30))
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Roboto", 11))

        self.expense_week = QLabel('0', group_box)
        self.expense_week.setGeometry(QRect(95, 40, 100, 30))
        self.expense_week.setAlignment(Qt.AlignCenter)
        self.expense_week.setFont(QFont("Roboto", 10))

        label = QLabel('Итогo', group_box)
        label.setGeometry(QRect(190, 20, 100, 30))
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Roboto", 11))

        self.sum_week = QLabel('0', group_box)
        self.sum_week.setGeometry(QRect(190, 40, 100, 30))
        self.sum_week.setAlignment(Qt.AlignCenter)
        self.sum_week.setFont(QFont("Roboto", 10))

        group_box = QGroupBox('За месяц', static)
        group_box.setAlignment(Qt.AlignCenter)
        group_box.setGeometry(QRect(10, 180, 290, 70))
        group_box.setFont(QFont("Roboto", 11))

        label = QLabel('Доход', group_box)
        label.setGeometry(QRect(0, 20, 100, 30))
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Roboto", 11))

        self.income_month = QLabel('0', group_box)
        self.income_month.setGeometry(QRect(0, 40, 100, 30))
        self.income_month.setAlignment(Qt.AlignCenter)
        self.income_month.setFont(QFont("Roboto", 10))

        label = QLabel('Расход', group_box)
        label.setGeometry(QRect(95, 20, 100, 30))
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Roboto", 11))

        self.expense_month = QLabel('0', group_box)
        self.expense_month.setGeometry(QRect(95, 40, 100, 30))
        self.expense_month.setAlignment(Qt.AlignCenter)
        self.expense_month.setFont(QFont("Roboto", 10))

        label = QLabel('Итогo', group_box)
        label.setGeometry(QRect(190, 20, 100, 30))
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Roboto", 11))

        self.sum_month = QLabel('0', group_box)
        self.sum_month.setGeometry(QRect(190, 40, 100, 30))
        self.sum_month.setAlignment(Qt.AlignCenter)
        self.sum_month.setFont(QFont("Roboto", 10))

        " СТАТИСТИКА "

        self.update_list_category()
        self.list_category.setCurrentRow(0)

        self.update_list_family()
        self.list_family.setCurrentRow(0)

        self.update_table_expense()
        self.tabs.currentChanged.connect(self.update_list_category)
        self.tabs.currentChanged.connect(self.click_tabs)
        self.list_category.currentRowChanged.connect(self.update_table)
        self.comboBox_math.currentTextChanged.connect(self.update_table)

    def update_static(self):
        with psycopg2.connect(database="kurs",
                              user="postgres",
                              password="Cactys14",
                              host="localhost",
                              port="5432"
                              ) as conn:
            with conn.cursor() as cur:
                cur.callproc('get_today_income')
                for row in cur:
                    income_today = row[0]

                if income_today is None:
                    income_today = 0

                cur.callproc('get_today_expense')
                for row in cur:
                    expense_today = row[0]

                if expense_today is None:
                    expense_today = 0

                now = datetime.now()
                days = timedelta(7)
                date = datetime.strftime(now - days, "%Y-%m-%d")
                now = datetime.strftime(now, "%Y-%m-%d")
                cur.callproc('get_state_date_begin_end_income', [date, now])
                for row in cur:
                    income_week = row[0]

                if income_week is None:
                    income_week = 0

                now = datetime.now()
                days = timedelta(7)
                date = datetime.strftime(now - days, "%Y-%m-%d")
                now = datetime.strftime(now, "%Y-%m-%d")
                cur.callproc('get_state_date_begin_end_expense', [date, now])
                for row in cur:
                    expense_week = row[0]

                if expense_week is None:
                    expense_week = 0

                now = datetime.now()
                days = timedelta(30)
                date = datetime.strftime(now - days, "%Y-%m-%d")
                now = datetime.strftime(now, "%Y-%m-%d")
                cur.callproc('get_state_date_begin_end_income', [date, now])
                for row in cur:
                    income_month = row[0]

                if income_month is None:
                    income_month = 0

                now = datetime.now()
                days = timedelta(30)
                date = datetime.strftime(now - days, "%Y-%m-%d")
                now = datetime.strftime(now, "%Y-%m-%d")
                cur.callproc('get_state_date_begin_end_expense', [date, now])
                for row in cur:
                    expense_month = row[0]

                if expense_month is None:
                    expense_month = 0

                self.income_today.setText('<b>' + str(income_today) + '</b>')
                self.expense_today.setText('<b>' + str(expense_today) + '</b>')

                if income_today - expense_today >= 0:
                    self.sum_today.setStyleSheet(
                        'QLabel {color: #008000;}')
                else:
                    self.sum_today.setStyleSheet(
                        'QLabel {color: #ff0000;}')

                self.income_week.setText('<b>' + str(income_week) + '</b>')
                self.expense_week.setText('<b>' + str(expense_week) + '</b>')

                if income_week - expense_week >= 0:
                    self.sum_week.setStyleSheet(
                        'QLabel {color: #008000;}')
                else:
                    self.sum_week.setStyleSheet(
                        'QLabel {color: #ff0000;}')

                self.income_month.setText('<b>' + str(income_month) + '</b>')
                self.expense_month.setText('<b>' + str(expense_month) + '</b>')

                if income_month - expense_month >= 0:
                    self.sum_month.setStyleSheet(
                        'QLabel {color: #008000;}')
                else:
                    self.sum_month.setStyleSheet(
                        'QLabel {color: #ff0000;}')

                self.sum_month.setText('<b>' + str(income_month - expense_month) + '</b>')
                self.sum_week.setText('<b>' + str(income_week - expense_week) + '</b>')
                self.sum_today.setText('<b>' + str(income_today - expense_today) + '</b>')

                ""
                # self.income_today.setText('1000000000.00')
                # self.expense_today.setText('1000000000.00')
                # self.sum_today.setText('1000000000.00')
                ""

    def update_table(self):
        self.update_static()

        if self.tabs.currentIndex() == 0:
            self.update_table_income()

        elif self.tabs.currentIndex() == 1:
            self.update_table_expense()

        elif self.tabs.currentIndex() == 2:
            self.update_table_savings_account()

        else:
            self.update_table_credit()

    def update_table_credit(self):
        self.table_credit.clear()
        self.table_credit.setHorizontalHeaderLabels(["Член семьи", "Дата", "Банк", "Сумма", ''])
        self.table_credit.setRowCount(11)
        self.index_credit.clear()

        if self.list_category.currentRow() == -1:
            self.list_category.setCurrentRow(0)

        with psycopg2.connect(database="kurs",
                              user="postgres",
                              password="Cactys14",
                              host="localhost",
                              port="5432"
                              ) as conn:
            with conn.cursor() as cur:
                if not self.date_today and not self.date_week and not self.date_month:
                    if not self.number_income:
                        if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                            cur.callproc('get_all_credit')

                        elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                            cur.callproc('get_member_family_category_credit',
                                         [self.index_family[self.list_family.currentRow()],
                                          self.index_category[self.list_category.currentRow()]])

                        elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                            cur.callproc('get_category_credit',
                                         [self.index_category[self.list_category.currentRow()]])

                        else:
                            cur.callproc('get_member_family_credit',
                                         [self.index_family[self.list_family.currentRow()]])
                    else:
                        if self.comboBox_math.currentText() == '<':
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_less_numeric_credit',
                                             [float(self.line_math.text())])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_less_numeric_member_category_credit',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_less_numeric_category_credit',
                                             [float(self.line_math.text()),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_less_numeric_member_credit',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()]])

                        elif self.comboBox_math.currentText() == '>':
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_more_numeric_credit',
                                             [float(self.line_math.text())])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_more_numeric_member_category_credit',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_more_numeric_category_credit',
                                             [float(self.line_math.text()),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_more_numeric_member_credit',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()]])
                        else:
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_equally_numeric_credit',
                                             [float(self.line_math.text())])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_equally_numeric_member_category_credit',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_equally_numeric_category_credit',
                                             [float(self.line_math.text()),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_equally_numeric_member_credit',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()]])

                elif self.date_today:
                    if not self.number_income:
                        if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                            cur.callproc('get_date_today_credit')

                        elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                            cur.callproc('get_date_today_category_member_credit',
                                         [self.index_family[self.list_family.currentRow()],
                                          self.index_category[self.list_category.currentRow()]])

                        elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                            cur.callproc('get_date_today_category_credit',
                                         [self.index_category[self.list_category.currentRow()]])

                        else:
                            cur.callproc('get_date_today_member_credit',
                                         [self.index_family[self.list_family.currentRow()]])
                    else:
                        if self.comboBox_math.currentText() == '<':
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_today_less_numeric_credit',
                                             [float(self.line_math.text())])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_today_less_numeric_member_category_credit',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_today_less_numeric_category_credit',
                                             [float(self.line_math.text()),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_today_less_numeric_member_credit',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()]])

                        elif self.comboBox_math.currentText() == '>':
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_today_more_numeric_credit',
                                             [float(self.line_math.text())])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_today_more_numeric_member_category_credit',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_today_more_numeric_category_credit',
                                             [float(self.line_math.text()),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_today_more_numeric_member_credit',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()]])

                        else:
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_today_equally_numeric_credit',
                                             [float(self.line_math.text())])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_today_equally_numeric_member_category_credit',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_today_equally_numeric_category_credit',
                                             [float(self.line_math.text()),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_today_equally_numeric_member_credit',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()]])

                elif self.date_month or self.date_week:
                    if not self.number_income:
                        if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                            cur.callproc('get_date_begin_end_credit',
                                         [self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                          self.date_end.dateTime().toString('yyyy-MM-dd')])

                        elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                            cur.callproc('get_date_begin_end_member_category_credit',
                                         [self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                          self.date_end.dateTime().toString('yyyy-MM-dd'),
                                          self.index_family[self.list_family.currentRow()],
                                          self.index_category[self.list_category.currentRow()]])

                        elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                            cur.callproc('get_date_begin_end_category_credit',
                                         [self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                          self.date_end.dateTime().toString('yyyy-MM-dd'),
                                          self.index_category[self.list_category.currentRow()]])

                        else:
                            cur.callproc('get_date_begin_end_member_credit',
                                         [self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                          self.date_end.dateTime().toString('yyyy-MM-dd'),
                                          self.index_family[self.list_family.currentRow()]])

                    else:
                        if self.comboBox_math.currentText() == '<':
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_date_less_numeric_credit',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd')])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_date_less_numeric_member_category_credit',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_date_less_numeric_category_credit',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_date_less_numeric_member_credit',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_family[self.list_family.currentRow()]])

                        elif self.comboBox_math.currentText() == '>':
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_date_more_numeric_credit',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd')])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_date_more_numeric_member_category_credit',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_date_more_numeric_category_credit',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_date_more_numeric_member_credit',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_family[self.list_family.currentRow()]])

                        else:
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_date_equally_numeric_credit',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd')])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_date_equally_numeric_member_category_credit',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_date_equally_numeric_category_credit',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_date_equally_numeric_member_credit',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_family[self.list_family.currentRow()]])
                row_table = 0
                for row in cur:
                    self.index_credit.append(row[0])

                    if row_table > 7:
                        self.table_credit.setRowCount(row_table + 1)

                    self.table_credit.setItem(row_table, 0, QTableWidgetItem(row[1] + ' ' + row[2]))

                    item = QTableWidgetItem(str(row[3]))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table_credit.setItem(row_table, 1, item)

                    item = QTableWidgetItem(row[4])
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table_credit.setItem(row_table, 2, item)

                    item = QTableWidgetItem(str(row[5]))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table_credit.setItem(row_table, 3, item)

                    btn = QPushButton()
                    btn.setIcon(QIcon('info.png'))
                    btn.setFixedSize(30, 30)
                    btn.setStyleSheet('QPushButton {border: none; color: #ffffff;}')
                    btn.clicked.connect(self.show_window_info_credit)
                    widget = QWidget()
                    pLayout = QHBoxLayout(widget)
                    pLayout.addWidget(btn)
                    pLayout.setAlignment(Qt.AlignCenter)
                    pLayout.setContentsMargins(0, 0, 0, 0)
                    widget.setLayout(pLayout)

                    self.table_credit.setCellWidget(row_table, 4, widget)

                    row_table += 1

    def update_table_savings_account(self):
        self.table_savings_account.clear()
        self.table_savings_account.setHorizontalHeaderLabels(["Член семьи", "Дата", "Банк", "Сумма вклада", ''])
        self.table_savings_account.setRowCount(11)
        self.index_savings_account.clear()

        with psycopg2.connect(database="kurs",
                              user="postgres",
                              password="Cactys14",
                              host="localhost",
                              port="5432"
                              ) as conn:
            with conn.cursor() as cur:
                if not self.date_today and not self.date_week and not self.date_month:
                    if not self.number_income:
                        if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                            cur.callproc('get_all_savings_account')

                        elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                            cur.callproc('get_member_family_category_savings_account',
                                         [self.index_family[self.list_family.currentRow()],
                                          self.index_category[self.list_category.currentRow()]])

                        elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                            cur.callproc('get_category_savings_account',
                                         [self.index_category[self.list_category.currentRow()]])

                        else:
                            cur.callproc('get_member_family_savings_account',
                                         [self.index_family[self.list_family.currentRow()]])
                    else:
                        if self.comboBox_math.currentText() == '<':
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_less_numeric_savings_account',
                                             [float(self.line_math.text())])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_less_numeric_member_category_savings_account',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_less_numeric_category_savings_account',
                                             [float(self.line_math.text()),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_less_numeric_member_savings_account',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()]])

                        elif self.comboBox_math.currentText() == '>':
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_more_numeric_savings_account',
                                             [float(self.line_math.text())])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_more_numeric_member_category_savings_account',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_more_numeric_category_savings_account',
                                             [float(self.line_math.text()),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_more_numeric_member_savings_account',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()]])
                        else:
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_equally_numeric_savings_account',
                                             [float(self.line_math.text())])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_equally_numeric_member_category_savings_account',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_equally_numeric_category_savings_account',
                                             [float(self.line_math.text()),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_equally_numeric_member_savings_account',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()]])

                elif self.date_today:
                    if not self.number_income:
                        if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                            cur.callproc('get_date_today_savings_account')

                        elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                            cur.callproc('get_date_today_category_member_savings_account',
                                         [self.index_family[self.list_family.currentRow()],
                                          self.index_category[self.list_category.currentRow()]])

                        elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                            cur.callproc('get_date_today_category_savings_account',
                                         [self.index_category[self.list_category.currentRow()]])

                        else:
                            cur.callproc('get_date_today_member_savings_account',
                                         [self.index_family[self.list_family.currentRow()]])
                    else:
                        if self.comboBox_math.currentText() == '<':
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_today_less_numeric_savings_account',
                                             [float(self.line_math.text())])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_today_less_numeric_member_category_savings_account',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_today_less_numeric_category_savings_account',
                                             [float(self.line_math.text()),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_today_less_numeric_member_savings_account',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()]])

                        elif self.comboBox_math.currentText() == '>':
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_today_more_numeric_savings_account',
                                             [float(self.line_math.text())])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_today_more_numeric_member_category_savings_account',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_today_more_numeric_category_savings_account',
                                             [float(self.line_math.text()),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_today_more_numeric_member_savings_account',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()]])

                        else:
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_today_equally_numeric_savings_account',
                                             [float(self.line_math.text())])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_today_equally_numeric_member_category_savings_account',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_today_equally_numeric_category_savings_account',
                                             [float(self.line_math.text()),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_today_equally_numeric_member_savings_account',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()]])

                elif self.date_month or self.date_week:
                    if not self.number_income:
                        if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                            cur.callproc('get_date_begin_end_savings_account',
                                         [self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                          self.date_end.dateTime().toString('yyyy-MM-dd')])

                        elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                            cur.callproc('get_date_begin_end_member_category_savings_account',
                                         [self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                          self.date_end.dateTime().toString('yyyy-MM-dd'),
                                          self.index_family[self.list_family.currentRow()],
                                          self.index_category[self.list_category.currentRow()]])

                        elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                            cur.callproc('get_date_begin_end_category_savings_account',
                                         [self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                          self.date_end.dateTime().toString('yyyy-MM-dd'),
                                          self.index_category[self.list_category.currentRow()]])

                        else:
                            cur.callproc('get_date_begin_end_member_savings_account',
                                         [self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                          self.date_end.dateTime().toString('yyyy-MM-dd'),
                                          self.index_family[self.list_family.currentRow()]])

                    else:
                        if self.comboBox_math.currentText() == '<':
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_date_less_numeric_savings_account',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd')])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_date_less_numeric_member_category_savings_account',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_date_less_numeric_category_savings_account',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_date_less_numeric_member_savings_account',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_family[self.list_family.currentRow()]])

                        elif self.comboBox_math.currentText() == '>':
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_date_more_numeric_savings_account',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd')])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_date_more_numeric_member_category_savings_account',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_date_more_numeric_category_savings_account',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_date_more_numeric_member_savings_account',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_family[self.list_family.currentRow()]])

                        else:
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_date_equally_numeric_savings_account',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd')])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_date_equally_numeric_member_category_savings_account',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_date_equally_numeric_category_savings_account',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_date_equally_numeric_member_savings_account',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_family[self.list_family.currentRow()]])

                row_table = 0
                for row in cur:
                    self.index_savings_account.append(row[0])

                    if row_table > 7:
                        self.table_savings_account.setRowCount(row_table + 1)

                    self.table_savings_account.setItem(row_table, 0, QTableWidgetItem(row[1] + ' ' + row[2]))

                    item = QTableWidgetItem(str(row[3]))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table_savings_account.setItem(row_table, 1, item)

                    item = QTableWidgetItem(row[4])
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table_savings_account.setItem(row_table, 2, item)

                    item = QTableWidgetItem(str(row[5]))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table_savings_account.setItem(row_table, 3, item)

                    btn = QPushButton()
                    btn.setIcon(QIcon('info.png'))
                    btn.setFixedSize(30, 30)
                    btn.setStyleSheet('QPushButton {border: none; color: #ffffff;}')
                    btn.clicked.connect(self.show_window_info_savings_account)
                    widget = QWidget()
                    pLayout = QHBoxLayout(widget)
                    pLayout.addWidget(btn)
                    pLayout.setAlignment(Qt.AlignCenter)
                    pLayout.setContentsMargins(0, 0, 0, 0)
                    widget.setLayout(pLayout)

                    self.table_savings_account.setCellWidget(row_table, 4, widget)

                    row_table += 1

    def click_tabs(self):
        self.list_category.setCurrentRow(0)

        if self.tabs.currentIndex() == 0:
            self.filter.setTitle('Доход')
            self.category.setTitle('Категории')
            self.button_add_category.setText('Добавить\nкатегорию')
            self.button_delete_category.setText('Удалить\nкатегорию')

        elif self.tabs.currentIndex() == 1:
            self.filter.setTitle('Расход')
            self.category.setTitle('Категории')
            self.button_add_category.setText('Добавить\nкатегорию')
            self.button_delete_category.setText('Удалить\nкатегорию')

        elif self.tabs.currentIndex() == 2:
            self.filter.setTitle('Сумма счета')
            self.category.setTitle('Банк')
            self.button_add_category.setText('Добавить\nбанк')
            self.button_delete_category.setText('Удалить\nбанк')

        else:
            self.filter.setTitle('Сумма кредита')

    def click_button_clear_math(self):
        self.button_math.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')

        self.number_income = False
        self.update_table()

        self.line_math.clear()

    def click_button_math(self):
        self.button_math.setStyleSheet('QPushButton {background-color: #363237; color: #ffffff;}')

        self.number_income = True
        self.update_table()

    def click_button_perform_period(self):
        self.button_date_today.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
        self.button_date_week.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
        self.button_date_month.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
        self.button_perform_period.setStyleSheet('QPushButton {background-color: #363237; color: #ffffff;}')

        self.date_today = False
        self.date_week = True
        self.date_month = True

        self.update_table()

    def click_button_date_month(self):
        self.button_date_today.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
        self.button_date_week.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
        self.button_date_month.setStyleSheet('QPushButton {background-color: #363237; color: #ffffff;}')
        self.button_perform_period.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')

        now = datetime.now()
        two_days = timedelta(30)
        in_two_days = now - two_days
        self.date_begin.setDate(QDate.fromString(datetime.strftime(in_two_days, "%d/%m/%Y"), "dd/MM/yyyy"))

        self.date_today = False
        self.date_week = False
        self.date_month = True

        self.update_table()

    def click_button_date_week(self):
        self.button_date_today.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
        self.button_date_week.setStyleSheet('QPushButton {background-color: #363237; color: #ffffff;}')
        self.button_date_month.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
        self.button_perform_period.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')

        now = datetime.now()
        two_days = timedelta(7)
        in_two_days = now - two_days
        self.date_begin.setDate(QDate.fromString(datetime.strftime(in_two_days, "%d/%m/%Y"), "dd/MM/yyyy"))

        self.date_today = False
        self.date_week = True
        self.date_month = False

        self.update_table()

    def click_button_clear_filter(self):
        self.button_date_today.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
        self.button_date_week.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
        self.button_date_month.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
        self.button_perform_period.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')

        self.date_begin.setDate(QDate.currentDate())
        self.date_end.setDate(QDate.currentDate())

        self.date_today = False
        self.date_week = False
        self.date_month = False

        self.update_table()

    def click_button_date_today(self):
        self.button_date_today.setStyleSheet('QPushButton {background-color: #363237; color: #ffffff;}')
        self.button_date_week.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
        self.button_date_month.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
        self.button_perform_period.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')

        self.date_begin.setDate(QDate.currentDate())
        self.date_end.setDate(QDate.currentDate())

        self.date_today = True
        self.date_week = False
        self.date_month = False

        self.update_table()

    def update_table_income(self):
        self.table_income.clear()
        self.table_income.setHorizontalHeaderLabels(["Член семьи", "Дата", "Категория", "Доход", ''])
        self.table_income.setRowCount(11)
        self.index_income.clear()

        with psycopg2.connect(database="kurs",
                              user="postgres",
                              password="Cactys14",
                              host="localhost",
                              port="5432"
                              ) as conn:
            with conn.cursor() as cur:
                if not self.date_today and not self.date_week and not self.date_month:
                    if not self.number_income:
                        if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                            cur.callproc('get_all_income')

                        elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                            cur.callproc('get_member_family_category_income',
                                         [self.index_family[self.list_family.currentRow()],
                                          self.index_category[self.list_category.currentRow()]])

                        elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                            cur.callproc('get_category_income',
                                         [self.index_category[self.list_category.currentRow()]])

                        else:
                            cur.callproc('get_member_family_income',
                                         [self.index_family[self.list_family.currentRow()]])
                    else:
                        if self.comboBox_math.currentText() == '<':
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_less_numeric_income',
                                             [float(self.line_math.text())])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_less_numeric_member_category_income',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_less_numeric_category_income',
                                             [float(self.line_math.text()),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_less_numeric_member_income',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()]])

                        elif self.comboBox_math.currentText() == '>':
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_more_numeric_income',
                                             [float(self.line_math.text())])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_more_numeric_member_category_income',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_more_numeric_category_income',
                                             [float(self.line_math.text()),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_more_numeric_member_income',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()]])
                        else:
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_equally_numeric_income',
                                             [float(self.line_math.text())])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_equally_numeric_member_category_income',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_equally_numeric_category_income',
                                             [float(self.line_math.text()),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_equally_numeric_member_income',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()]])

                elif self.date_today:
                    if not self.number_income:
                        if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                            cur.callproc('get_date_today_income')

                        elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                            cur.callproc('get_date_today_category_member_income',
                                         [self.index_family[self.list_family.currentRow()],
                                          self.index_category[self.list_category.currentRow()]])

                        elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                            cur.callproc('get_date_today_category_income',
                                         [self.index_category[self.list_category.currentRow()]])

                        else:
                            cur.callproc('get_date_today_member_income',
                                         [self.index_family[self.list_family.currentRow()]])
                    else:
                        if self.comboBox_math.currentText() == '<':
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_today_less_numeric_income',
                                             [float(self.line_math.text())])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_today_less_numeric_member_category_income',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_today_less_numeric_category_income',
                                             [float(self.line_math.text()),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_today_less_numeric_member_income',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()]])

                        elif self.comboBox_math.currentText() == '>':
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_today_more_numeric_income',
                                             [float(self.line_math.text())])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_today_more_numeric_member_category_income',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_today_more_numeric_category_income',
                                             [float(self.line_math.text()),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_today_more_numeric_member_income',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()]])

                        else:
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_today_equally_numeric_income',
                                             [float(self.line_math.text())])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_today_equally_numeric_member_category_income',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_today_equally_numeric_category_income',
                                             [float(self.line_math.text()),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_today_equally_numeric_member_income',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()]])

                elif self.date_month or self.date_week:
                    if not self.number_income:
                        if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                            cur.callproc('get_date_begin_end_income',
                                         [self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                          self.date_end.dateTime().toString('yyyy-MM-dd')])

                        elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                            cur.callproc('get_date_begin_end_member_category_income',
                                         [self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                          self.date_end.dateTime().toString('yyyy-MM-dd'),
                                          self.index_family[self.list_family.currentRow()],
                                          self.index_category[self.list_category.currentRow()]])

                        elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                            cur.callproc('get_date_begin_end_category_income',
                                         [self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                          self.date_end.dateTime().toString('yyyy-MM-dd'),
                                          self.index_category[self.list_category.currentRow()]])

                        else:
                            cur.callproc('get_date_begin_end_member_income',
                                         [self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                          self.date_end.dateTime().toString('yyyy-MM-dd'),
                                          self.index_family[self.list_family.currentRow()]])

                    else:
                        if self.comboBox_math.currentText() == '<':
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_date_less_numeric_income',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd')])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_date_less_numeric_member_category_income',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_date_less_numeric_category_income',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_date_less_numeric_member_income',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_family[self.list_family.currentRow()]])

                        elif self.comboBox_math.currentText() == '>':
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_date_more_numeric_income',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd')])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_date_more_numeric_member_category_income',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_date_more_numeric_category_income',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_date_more_numeric_member_income',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_family[self.list_family.currentRow()]])

                        else:
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_date_equally_numeric_income',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd')])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_date_equally_numeric_member_category_income',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_date_equally_numeric_category_income',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_date_equally_numeric_member_income',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_family[self.list_family.currentRow()]])

                row_table = 0
                for row in cur:
                    self.index_income.append(row[0])

                    if row_table > 10:
                        self.table_income.setRowCount(row_table + 1)

                    self.table_income.setItem(row_table, 0, QTableWidgetItem(row[1] + ' ' + row[2]))

                    item = QTableWidgetItem(str(row[3]))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table_income.setItem(row_table, 1, item)

                    item = QTableWidgetItem(row[4])
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table_income.setItem(row_table, 2, item)

                    item = QTableWidgetItem(str(row[5]))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table_income.setItem(row_table, 3, item)

                    btn = QPushButton()
                    btn.setIcon(QIcon('cross.png'))
                    btn.setFixedSize(30, 30)
                    btn.setStyleSheet('QPushButton {border: none; color: #ffffff;}')
                    btn.clicked.connect(self.delete_income)
                    widget = QWidget()
                    pLayout = QHBoxLayout(widget)
                    pLayout.addWidget(btn)
                    pLayout.setAlignment(Qt.AlignCenter)
                    pLayout.setContentsMargins(0, 0, 0, 0)
                    widget.setLayout(pLayout)

                    self.table_income.setCellWidget(row_table, 4, widget)

                    row_table += 1

    def add_credit(self):
        index_member = self.index_family[self.comboBox_member_savings_credit.currentIndex() + 1]
        index_category = self.index_category[self.comboBox_bank_credit.currentIndex() + 1]

        try:
            if float(self.line_loan_amount.text()) < 10e8:
                with psycopg2.connect(database="kurs",
                                      user="postgres",
                                      password="Cactys14",
                                      host="localhost",
                                      port="5432"
                                      ) as conn:
                    with conn.cursor() as cur:
                        cur.callproc('add_credit', [index_member, index_category,
                                                    float(self.line_loan_amount.text()),
                                                    int(self.line_term_credit.text()),
                                                    float(self.line_interest_rate_credit.text()),
                                                    self.dateEdit_credit.dateTime().toString(
                                                        'yyyy-MM-dd')])
                self.update_table()
                # self.line_expense.clear()
            else:
                self.line_expense.clear()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Введено слишком большое число!")
                msg.setWindowTitle("Ошибка")
                msg.exec_()
        except:
            self.line_expense.clear()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Введен не числовой тип данных!")
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    def add_savings_account(self):
        index_member = self.index_family[self.comboBox_member_savings_account.currentIndex() + 1]
        index_category = self.index_category[self.comboBox_bank_savings_account.currentIndex() + 1]

        try:
            if float(self.line_deposit_amount.text()) < 10e8:
                with psycopg2.connect(database="kurs",
                                      user="postgres",
                                      password="Cactys14",
                                      host="localhost",
                                      port="5432"
                                      ) as conn:
                    with conn.cursor() as cur:
                        cur.callproc('add_savings_account', [index_member, index_category,
                                                             float(self.line_deposit_amount.text()),
                                                             int(self.line_term.text()),
                                                             self.dateEdit_savings_account.dateTime().toString(
                                                                 'yyyy-MM-dd'),
                                                             float(self.line_interest_rate.text())])
                self.update_table()
                # self.line_expense.clear()
            else:
                self.line_expense.clear()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Введено слишком большое число!")
                msg.setWindowTitle("Ошибка")
                msg.exec_()

        except:
            self.line_expense.clear()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Введен не числовой тип данных!")
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    def click_button_add_expense(self):
        index_member = self.index_family[self.comboBox_member_expense.currentIndex() + 1]
        index_category = self.index_category[self.comboBox_category_add_expense.currentIndex() + 1]

        try:
            if float(self.line_expense.text()) < 10e8:
                with psycopg2.connect(database="kurs",
                                      user="postgres",
                                      password="Cactys14",
                                      host="localhost",
                                      port="5432"
                                      ) as conn:
                    with conn.cursor() as cur:
                        cur.callproc('add_income_expense', ['expense', index_member,
                                                            self.dateEdit_expense.dateTime().toString('yyyy-MM-dd'),
                                                            index_category, float(self.line_expense.text())])
                self.update_table()
                self.line_expense.clear()
            else:
                self.line_expense.clear()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Введено слишком большое число!")
                msg.setWindowTitle("Ошибка")
                msg.exec_()

        except:
            self.line_expense.clear()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Введен не числовой тип данных!")
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    def update_table_expense(self):
        self.table_expense.clear()
        self.table_expense.setHorizontalHeaderLabels(["Член семьи", "Дата", "Категория", "Расходы", ''])
        self.table_expense.setRowCount(11)
        self.index_expense.clear()

        with psycopg2.connect(database="kurs",
                              user="postgres",
                              password="Cactys14",
                              host="localhost",
                              port="5432"
                              ) as conn:
            with conn.cursor() as cur:
                if not self.date_today and not self.date_week and not self.date_month:
                    if not self.number_income:
                        if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                            cur.callproc('get_all_expense')

                        elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                            cur.callproc('get_member_family_category_expense',
                                         [self.index_family[self.list_family.currentRow()],
                                          self.index_category[self.list_category.currentRow()]])

                        elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                            cur.callproc('get_category_expense',
                                         [self.index_category[self.list_category.currentRow()]])

                        else:
                            cur.callproc('get_member_family_expense',
                                         [self.index_family[self.list_family.currentRow()]])
                    else:
                        if self.comboBox_math.currentText() == '<':
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_less_numeric_expense',
                                             [float(self.line_math.text())])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_less_numeric_member_category_expense',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_less_numeric_category_expense',
                                             [float(self.line_math.text()),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_less_numeric_member_expense',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()]])

                        elif self.comboBox_math.currentText() == '>':
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_more_numeric_expense',
                                             [float(self.line_math.text())])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_more_numeric_member_category_expense',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_more_numeric_category_expense',
                                             [float(self.line_math.text()),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_more_numeric_member_expense',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()]])
                        else:
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_equally_numeric_expense',
                                             [float(self.line_math.text())])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_equally_numeric_member_category_expense',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_equally_numeric_category_expense',
                                             [float(self.line_math.text()),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_equally_numeric_member_expense',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()]])

                elif self.date_today:
                    if not self.number_income:
                        if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                            cur.callproc('get_date_today_expense')

                        elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                            cur.callproc('get_date_today_category_member_expense',
                                         [self.index_family[self.list_family.currentRow()],
                                          self.index_category[self.list_category.currentRow()]])

                        elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                            cur.callproc('get_date_today_category_expense',
                                         [self.index_category[self.list_category.currentRow()]])

                        else:
                            cur.callproc('get_date_today_member_expense',
                                         [self.index_family[self.list_family.currentRow()]])
                    else:
                        if self.comboBox_math.currentText() == '<':
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_today_less_numeric_expense',
                                             [float(self.line_math.text())])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_today_less_numeric_member_category_expense',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_today_less_numeric_category_expense',
                                             [float(self.line_math.text()),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_today_less_numeric_member_expense',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()]])

                        elif self.comboBox_math.currentText() == '>':
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_today_more_numeric_expense',
                                             [float(self.line_math.text())])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_today_more_numeric_member_category_expense',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_today_more_numeric_category_expense',
                                             [float(self.line_math.text()),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_today_more_numeric_member_expense',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()]])

                        else:
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_today_equally_numeric_expense',
                                             [float(self.line_math.text())])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_today_equally_numeric_member_category_expense',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_today_equally_numeric_category_expense',
                                             [float(self.line_math.text()),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_today_equally_numeric_member_expense',
                                             [float(self.line_math.text()),
                                              self.index_family[self.list_family.currentRow()]])

                elif self.date_month or self.date_week:
                    if not self.number_income:
                        if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                            cur.callproc('get_date_begin_end_expense',
                                         [self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                          self.date_end.dateTime().toString('yyyy-MM-dd')])

                        elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                            cur.callproc('get_date_begin_end_member_category_expense',
                                         [self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                          self.date_end.dateTime().toString('yyyy-MM-dd'),
                                          self.index_family[self.list_family.currentRow()],
                                          self.index_category[self.list_category.currentRow()]])

                        elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                            cur.callproc('get_date_begin_end_category_expense',
                                         [self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                          self.date_end.dateTime().toString('yyyy-MM-dd'),
                                          self.index_category[self.list_category.currentRow()]])

                        else:
                            cur.callproc('get_date_begin_end_member_expense',
                                         [self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                          self.date_end.dateTime().toString('yyyy-MM-dd'),
                                          self.index_family[self.list_family.currentRow()]])

                    else:
                        if self.comboBox_math.currentText() == '<':
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_date_less_numeric_expense',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd')])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_date_less_numeric_member_category_expense',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_date_less_numeric_category_expense',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_date_less_numeric_member_expense',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_family[self.list_family.currentRow()]])

                        elif self.comboBox_math.currentText() == '>':
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_date_more_numeric_expense',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd')])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_date_more_numeric_member_category_expense',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_date_more_numeric_category_expense',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_date_more_numeric_member_expense',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_family[self.list_family.currentRow()]])

                        else:
                            if self.list_family.currentRow() == 0 and self.list_category.currentRow() == 0:
                                cur.callproc('get_date_equally_numeric_expense',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd')])

                            elif self.list_family.currentRow() != 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_date_equally_numeric_member_category_expense',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_family[self.list_family.currentRow()],
                                              self.index_category[self.list_category.currentRow()]])

                            elif self.list_family.currentRow() == 0 and self.list_category.currentRow() != 0:
                                cur.callproc('get_date_equally_numeric_category_expense',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_category[self.list_category.currentRow()]])

                            else:
                                cur.callproc('get_date_equally_numeric_member_expense',
                                             [float(self.line_math.text()),
                                              self.date_begin.dateTime().toString('yyyy-MM-dd'),
                                              self.date_end.dateTime().toString('yyyy-MM-dd'),
                                              self.index_family[self.list_family.currentRow()]])

                row_table = 0
                for row in cur:
                    self.index_expense.append(row[0])

                    if row_table > 10:
                        self.table_expense.setRowCount(row_table + 1)

                    self.table_expense.setItem(row_table, 0, QTableWidgetItem(row[1] + ' ' + row[2]))

                    item = QTableWidgetItem(str(row[3]))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table_expense.setItem(row_table, 1, item)

                    item = QTableWidgetItem(row[4])
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table_expense.setItem(row_table, 2, item)

                    item = QTableWidgetItem(str(row[5]))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table_expense.setItem(row_table, 3, item)

                    btn = QPushButton()
                    btn.setIcon(QIcon('cross.png'))
                    btn.setFixedSize(30, 30)
                    btn.setStyleSheet('QPushButton {border: none; color: #ffffff;}')
                    btn.clicked.connect(self.delete_expense)
                    widget = QWidget()
                    pLayout = QHBoxLayout(widget)
                    pLayout.addWidget(btn)
                    pLayout.setAlignment(Qt.AlignCenter)
                    pLayout.setContentsMargins(0, 0, 0, 0)
                    widget.setLayout(pLayout)

                    self.table_expense.setCellWidget(row_table, 4, widget)

                    row_table += 1

    def delete_expense(self):
        button = self.sender()
        if button:
            row = self.table_expense.indexAt(button.parent().pos()).row()
            with psycopg2.connect(database="kurs",
                                  user="postgres",
                                  password="Cactys14",
                                  host="localhost",
                                  port="5432"
                                  ) as conn:
                with conn.cursor() as cur:
                    cur.callproc('delete_income_expense', ['expense', self.index_expense[row]])
            self.update_table()

    def update_all_table_income(self):
        self.table_income.clear()
        self.table_income.setHorizontalHeaderLabels(["Член семьи", "Дата", "Категория", "Доход", ''])
        self.table_income.setRowCount(11)
        self.index_income.clear()

        with psycopg2.connect(database="kurs",
                              user="postgres",
                              password="Cactys14",
                              host="localhost",
                              port="5432"
                              ) as conn:
            with conn.cursor() as cur:
                cur.callproc('get_all_income')
                row_table = 0
                for row in cur:
                    self.index_income.append(row[0])

                    if row_table > 10:
                        self.table_income.setRowCount(row_table + 1)

                    self.table_income.setItem(row_table, 0, QTableWidgetItem(row[1] + ' ' + row[2]))

                    item = QTableWidgetItem(str(row[3]))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table_income.setItem(row_table, 1, item)

                    item = QTableWidgetItem(row[4])
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table_income.setItem(row_table, 2, item)

                    item = QTableWidgetItem(str(row[5]))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table_income.setItem(row_table, 3, item)

                    btn = QPushButton()
                    btn.setIcon(QIcon('cross.png'))
                    btn.setFixedSize(30, 30)
                    btn.setStyleSheet('QPushButton {border: none; color: #ffffff;}')
                    btn.clicked.connect(self.delete_income)
                    widget = QWidget()
                    pLayout = QHBoxLayout(widget)
                    pLayout.addWidget(btn)
                    pLayout.setAlignment(Qt.AlignCenter)
                    pLayout.setContentsMargins(0, 0, 0, 0)
                    widget.setLayout(pLayout)

                    self.table_income.setCellWidget(row_table, 4, widget)

                    row_table += 1

    def delete_income(self):
        button = self.sender()
        if button:
            row = self.table_income.indexAt(button.parent().pos()).row()
            with psycopg2.connect(database="kurs",
                                  user="postgres",
                                  password="Cactys14",
                                  host="localhost",
                                  port="5432"
                                  ) as conn:
                with conn.cursor() as cur:
                    cur.callproc('delete_income_expense', ['income', self.index_income[row]])
            self.update_table()

    def click_button_add_income(self):
        index_member = self.index_family[self.comboBox_member_income.currentIndex() + 1]
        index_category = self.index_category[self.comboBox_category_add_income.currentIndex() + 1]

        try:
            if float(self.line_income.text()) < 10e8:
                with psycopg2.connect(database="kurs",
                                      user="postgres",
                                      password="Cactys14",
                                      host="localhost",
                                      port="5432"
                                      ) as conn:
                    with conn.cursor() as cur:
                        cur.callproc('add_income_expense', ['income', index_member,
                                                            self.dateEdit_income.dateTime().toString('yyyy-MM-dd'),
                                                            index_category, float(self.line_income.text())])
                self.update_table()
                self.line_income.clear()
            else:
                self.line_income.clear()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Введено слишком большое число!")
                msg.setWindowTitle("Ошибка")
                msg.exec_()

        except:
            self.line_income.clear()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Введен не числовой тип данных!")
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    def delete_category(self):
        if self.list_category.currentRow() != 0:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Удаление")
            dlg.setIcon(QMessageBox.Question)
            dlg.setText("Действительно хотите удалить категорию?")
            buttonAceptar = dlg.addButton("Да", QMessageBox.YesRole)
            buttonCancelar = dlg.addButton("Отмена", QMessageBox.RejectRole)
            dlg.setDefaultButton(buttonAceptar)
            dlg.exec_()

            if dlg.clickedButton() == buttonAceptar:
                index = self.index_category[self.list_category.currentRow()]
                with psycopg2.connect(database="kurs",
                                      user="postgres",
                                      password="Cactys14",
                                      host="localhost",
                                      port="5432"
                                      ) as conn:
                    with conn.cursor() as cur:
                        if self.tabs.currentIndex() == 0:
                            cur.callproc('delete_category', ['income', index])

                        elif self.tabs.currentIndex() == 1:
                            cur.callproc('delete_category', ['expense', index])

                        else:
                            cur.callproc('delete_category', ['bank', index])

                self.update_list_category()
                self.update_table()
            else:
                pass

    def click_button_add_category(self):
        text, ok = QInputDialog.getText(self, 'Добавление', 'Введите название категории:')
        if ok:
            with psycopg2.connect(database="kurs",
                                  user="postgres",
                                  password="Cactys14",
                                  host="localhost",
                                  port="5432"
                                  ) as conn:
                with conn.cursor() as cur:
                    if self.tabs.currentIndex() == 0:
                        cur.callproc('add_category', ['income', text])

                    elif self.tabs.currentIndex() == 1:
                        cur.callproc('add_category', ['expense', text])

                    elif self.tabs.currentIndex() == 2:
                        cur.callproc('add_category', ['bank', text])

            self.update_list_category()

    def update_list_category(self):
        self.list_category.clear()

        self.index_category.clear()
        self.index_category.append(0)

        self.comboBox_category_add_income.clear()
        self.comboBox_category_add_expense.clear()
        self.comboBox_bank_savings_account.clear()
        self.comboBox_bank_credit.clear()

        with psycopg2.connect(database="kurs",
                              user="postgres",
                              password="Cactys14",
                              host="localhost",
                              port="5432"
                              ) as conn:
            with conn.cursor() as cur:
                if self.tabs.currentIndex() == 0:
                    cur.execute('SELECT * FROM income_category ORDER BY id ASC ')
                    self.list_category.addItem('Все категории')

                elif self.tabs.currentIndex() == 1:
                    cur.execute('SELECT * FROM expense_category ORDER BY id ASC ')
                    self.list_category.addItem('Все категории')

                else:
                    cur.execute('SELECT * FROM bank ORDER BY id ASC ')
                    self.list_category.addItem('Все банки')

                self.list_category.setCurrentRow(0)
                for row in cur:
                    self.index_category.append(row[0])
                    self.list_category.addItem(row[1])
                    self.comboBox_category_add_income.addItem(row[1])
                    self.comboBox_category_add_expense.addItem(row[1])
                    self.comboBox_bank_savings_account.addItem(row[1])
                    self.comboBox_bank_credit.addItem(row[1])

    def delete_member_family(self):
        if self.list_family.currentRow() != 0:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Удаление")
            dlg.setIcon(QMessageBox.Question)
            dlg.setText("Действительно хотите удалить члена семьи?")
            buttonAceptar = dlg.addButton("Да", QMessageBox.YesRole)
            buttonCancelar = dlg.addButton("Отмена", QMessageBox.RejectRole)
            dlg.setDefaultButton(buttonAceptar)
            dlg.exec_()

            if dlg.clickedButton() == buttonAceptar:
                index = self.index_family[self.list_family.currentRow()]
                with psycopg2.connect(database="kurs",
                                      user="postgres",
                                      password="Cactys14",
                                      host="localhost",
                                      port="5432"
                                      ) as conn:
                    with conn.cursor() as cur:
                        cur.callproc('delete_family_member', [index])
                self.update_list_family()
                self.update_all_table_income()
            else:
                pass

    def update_list_family(self):
        self.list_family.clear()
        self.list_family.addItem('Вся семья')
        self.list_family.setCurrentRow(0)

        self.index_family.clear()
        self.index_family.append(0)

        self.comboBox_member_income.clear()
        self.comboBox_member_expense.clear()
        self.comboBox_member_savings_account.clear()
        self.comboBox_member_savings_credit.clear()

        with psycopg2.connect(database="kurs",
                              user="postgres",
                              password="Cactys14",
                              host="localhost",
                              port="5432"
                              ) as conn:
            with conn.cursor() as cur:
                cur.callproc('get_all_family_member')
                for row in cur:
                    self.index_family.append(row[0])
                    self.list_family.addItem(row[1] + ' ' + row[2])
                    self.comboBox_member_income.addItem(row[1])
                    self.comboBox_member_expense.addItem(row[1])
                    self.comboBox_member_savings_account.addItem(row[1])
                    self.comboBox_member_savings_credit.addItem(row[1])

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def show_window_info_savings_account(self):
        button = self.sender()
        if button:
            row = self.table_savings_account.indexAt(button.parent().pos()).row()
            self.windowInfoSavingsAccount = WindowInfoSavingsAccount(self.index_savings_account[row], self)
            self.windowInfoSavingsAccount.show()

    def show_window_info_credit(self):
        button = self.sender()
        if button:
            row = self.table_credit.indexAt(button.parent().pos()).row()
            print(self.index_credit[row])
            self.windowInfoCredit = WindowInfoCredit(self.index_credit[row], self)
            self.windowInfoCredit.show()

    def show_window_add_family(self):
        self.windowAddFamily = WindowAddFamily(self)
        self.windowAddFamily.show()

    def show_window_info_family(self):
        if self.list_family.currentRow() != 0:
            self.windowInfoFamily = WindowInfoFamily(self,
                                                     self.index_family[self.list_family.currentRow()])
            self.windowInfoFamily.show()


class WindowInfoCredit(QWidget):
    def __init__(self, index, mainwindow):
        super().__init__()

        self.setWindowTitle("Информация о кредите")
        self.resize(572, 217)
        self.center()

        with psycopg2.connect(database="kurs",
                              user="postgres",
                              password="Cactys14",
                              host="localhost",
                              port="5432"
                              ) as conn:
            with conn.cursor() as cur:
                cur.callproc('get_id_credit', [index])

                for row in cur:
                    group_box = QGroupBox('Вкладчик', self)
                    group_box.setAlignment(Qt.AlignCenter)
                    group_box.setGeometry(QRect(385, 5, 180, 115))
                    group_box.setFont(QFont("Roboto", 12))

                    label = QLabel('Фамилия', group_box)
                    label.setGeometry(QRect(10, 25, 100, 30))
                    label.setFont(QFont("Roboto", 10))

                    text = QLabel(str(row[0]), group_box)
                    text.setGeometry(QRect(80, 25, 100, 30))
                    text.setFont(QFont("Roboto", 10))

                    label = QLabel('Имя', group_box)
                    label.setGeometry(QRect(10, 55, 100, 30))
                    label.setFont(QFont("Roboto", 9))

                    text = QLabel(str(row[1]), group_box)
                    text.setGeometry(QRect(80, 55, 100, 30))
                    text.setFont(QFont("Roboto", 9))

                    label = QLabel('Отчество', group_box)
                    label.setGeometry(QRect(10, 85, 100, 30))
                    label.setFont(QFont("Roboto", 9))

                    text = QLabel(str(row[2]), group_box)
                    text.setGeometry(QRect(80, 85, 100, 30))
                    text.setFont(QFont("Roboto", 9))

                    group_box = QGroupBox('Период', self)
                    group_box.setAlignment(Qt.AlignCenter)
                    group_box.setGeometry(QRect(5, 5, 375, 90))
                    group_box.setFont(QFont("Roboto", 12))

                    label = QLabel('Дата взятия', group_box)
                    label.setGeometry(QRect(10, 35, 100, 30))
                    label.setFont(QFont("Roboto", 9))

                    _date = str(row[3]).split('-')
                    text = QLabel(_date[2] + '-' + _date[1] + '-' + _date[0], group_box)
                    text.setGeometry(QRect(25, 55, 100, 30))
                    text.setFont(QFont("Roboto", 9))

                    _date = str(row[3]).split('-')
                    date_begin = datetime(int(_date[0]), int(_date[1]), int(_date[2]))

                    current_date = date.today()
                    date_end = date_begin
                    for _ in range(row[6]):
                        days = calendar.monthrange(date_begin.year, date_begin.month)[1]
                        date_end += timedelta(days=days)

                    label = QLabel('Дата окончания', group_box)
                    label.setGeometry(QRect(275, 35, 100, 30))
                    label.setFont(QFont("Roboto", 9))

                    text = QLabel(datetime.strftime(date_end, "%d-%m-%Y"), group_box)
                    text.setGeometry(QRect(290, 55, 100, 30))
                    text.setFont(QFont("Roboto", 9))

                    pbar = QProgressBar(group_box)
                    pbar.setGeometry(110, 50, 150, 25)
                    try:
                        a = int(str(current_date - date_begin.date()).split()[0])
                        b = int(str(date_end - date_begin).split()[0])

                        pbar.setValue(min(int(a / b * 100), 100))

                    except:
                        pbar.setValue(0)

                    label = QLabel('Срок хранения ' + str(row[6]), group_box)
                    label.setGeometry(QRect(135, 23, 120, 30))
                    label.setFont(QFont("Roboto", 9))

                    group_box = QGroupBox('Информация о кредите', self)
                    group_box.setAlignment(Qt.AlignCenter)
                    group_box.setGeometry(QRect(5, 100, 375, 110))
                    group_box.setFont(QFont("Roboto", 12))

                    label = QLabel('Банк', group_box)
                    label.setGeometry(QRect(10, 25, 100, 30))
                    label.setFont(QFont("Roboto", 9))

                    text = QLabel(str(row[4]), group_box)
                    text.setGeometry(QRect(55, 25, 100, 30))
                    text.setFont(QFont("Roboto", 9))

                    label = QLabel('Сумма кредита', group_box)
                    label.setGeometry(QRect(140, 25, 100, 30))
                    label.setFont(QFont("Roboto", 9))

                    text = QLabel(str(row[5]), group_box)
                    text.setGeometry(QRect(285, 25, 100, 30))
                    text.setFont(QFont("Roboto", 9))

                    label = QLabel('Cтавка', group_box)
                    label.setGeometry(QRect(10, 50, 45, 30))
                    label.setFont(QFont("Roboto", 9))

                    text = QLabel(str(row[7]) + '%', group_box)
                    text.setGeometry(QRect(55, 50, 100, 30))
                    text.setFont(QFont("Roboto", 9))

                    label = QLabel('Ежемесячный платеж', group_box)
                    label.setGeometry(QRect(140, 50, 140, 30))
                    label.setFont(QFont("Roboto", 9))

                    text = QLabel(str(row[8]), group_box)
                    text.setGeometry(QRect(285, 50, 100, 30))
                    text.setFont(QFont("Roboto", 9))

                    label = QLabel('Сумма к выплате', group_box)
                    label.setGeometry(QRect(140, 75, 40, 30))
                    label.setFont(QFont("Roboto", 9))

                    text = QLabel(str(row[10]), group_box)
                    text.setGeometry(QRect(285, 75, 100, 30))
                    text.setFont(QFont("Roboto", 9))

                    button_close = QPushButton('Закрыть информацию', self)
                    button_close.setGeometry(QRect(400, 170, 150, 30))
                    button_close.setFont(QFont("Roboto", 10))
                    button_close.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
                    button_close.clicked.connect(self.close)

                    button_delete = QPushButton('Удалить вклад', self)
                    button_delete.setGeometry(QRect(400, 130, 150, 30))
                    button_delete.setFont(QFont("Roboto", 10))
                    button_delete.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
                    button_delete.clicked.connect(lambda: self.delete_credit(index, mainwindow))
                    button_delete.clicked.connect(mainwindow.update_table)

    def delete_credit(self, index, mainwindow):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Удаление")
        dlg.setIcon(QMessageBox.Question)
        dlg.setText("Действительно хотите удалить сберегательный счет?")
        buttonAceptar = dlg.addButton("Да", QMessageBox.YesRole)
        buttonCancelar = dlg.addButton("Отмена", QMessageBox.RejectRole)
        dlg.setDefaultButton(buttonAceptar)
        dlg.exec_()

        if dlg.clickedButton() == buttonAceptar:
            with psycopg2.connect(database="kurs",
                                  user="postgres",
                                  password="Cactys14",
                                  host="localhost",
                                  port="5432"
                                  ) as conn:
                with conn.cursor() as cur:
                    cur.callproc('delete_credit', [index])
                mainwindow.update_table()
                self.close()
        else:
            pass

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class WindowInfoSavingsAccount(QWidget):
    def __init__(self, index, mainwindow):
        super().__init__()

        self.setWindowTitle("Информация о вкладе")
        self.resize(572, 217)
        self.center()

        with psycopg2.connect(database="kurs",
                              user="postgres",
                              password="Cactys14",
                              host="localhost",
                              port="5432"
                              ) as conn:
            with conn.cursor() as cur:
                cur.callproc('get_id_savings_account', [index])

                for row in cur:
                    group_box = QGroupBox('Вкладчик', self)
                    group_box.setAlignment(Qt.AlignCenter)
                    group_box.setGeometry(QRect(385, 5, 180, 115))
                    group_box.setFont(QFont("Roboto", 12))

                    label = QLabel('Фамилия', group_box)
                    label.setGeometry(QRect(10, 25, 100, 30))
                    label.setFont(QFont("Roboto", 10))

                    text = QLabel(str(row[0]), group_box)
                    text.setGeometry(QRect(80, 25, 100, 30))
                    text.setFont(QFont("Roboto", 10))

                    label = QLabel('Имя', group_box)
                    label.setGeometry(QRect(10, 55, 100, 30))
                    label.setFont(QFont("Roboto", 9))

                    text = QLabel(str(row[1]), group_box)
                    text.setGeometry(QRect(80, 55, 100, 30))
                    text.setFont(QFont("Roboto", 9))

                    label = QLabel('Отчество', group_box)
                    label.setGeometry(QRect(10, 85, 100, 30))
                    label.setFont(QFont("Roboto", 9))

                    text = QLabel(str(row[2]), group_box)
                    text.setGeometry(QRect(80, 85, 100, 30))
                    text.setFont(QFont("Roboto", 9))

                    group_box = QGroupBox('Период', self)
                    group_box.setAlignment(Qt.AlignCenter)
                    group_box.setGeometry(QRect(5, 5, 375, 90))
                    group_box.setFont(QFont("Roboto", 12))

                    label = QLabel('Дата вложения', group_box)
                    label.setGeometry(QRect(10, 35, 100, 30))
                    label.setFont(QFont("Roboto", 9))

                    _date = str(row[3]).split('-')
                    text = QLabel(_date[2] + '-' + _date[1] + '-' + _date[0], group_box)
                    text.setGeometry(QRect(25, 55, 100, 30))
                    text.setFont(QFont("Roboto", 9))

                    _date = str(row[3]).split('-')
                    date_begin = datetime(int(_date[0]), int(_date[1]), int(_date[2]))

                    current_date = date.today()
                    date_end = date_begin
                    for _ in range(row[6]):
                        days = calendar.monthrange(date_begin.year, date_begin.month)[1]
                        date_end += timedelta(days=days)

                    label = QLabel('Дата окончания', group_box)
                    label.setGeometry(QRect(275, 35, 100, 30))
                    label.setFont(QFont("Roboto", 9))

                    text = QLabel(datetime.strftime(date_end, "%d-%m-%Y"), group_box)
                    text.setGeometry(QRect(290, 55, 100, 30))
                    text.setFont(QFont("Roboto", 9))

                    pbar = QProgressBar(group_box)
                    pbar.setGeometry(110, 50, 150, 25)
                    try:
                        a = int(str(current_date - date_begin.date()).split()[0])
                        b = int(str(date_end - date_begin).split()[0])

                        pbar.setValue(min(int(a / b * 100), 100))

                    except:
                        pbar.setValue(0)

                    label = QLabel('Срок хранения ' + str(row[6]), group_box)
                    label.setGeometry(QRect(135, 23, 120, 30))
                    label.setFont(QFont("Roboto", 9))

                    group_box = QGroupBox('Информация о вкладе', self)
                    group_box.setAlignment(Qt.AlignCenter)
                    group_box.setGeometry(QRect(5, 100, 375, 110))
                    group_box.setFont(QFont("Roboto", 12))

                    label = QLabel('Банк', group_box)
                    label.setGeometry(QRect(10, 25, 100, 30))
                    label.setFont(QFont("Roboto", 9))

                    text = QLabel(str(row[4]), group_box)
                    text.setGeometry(QRect(55, 25, 100, 30))
                    text.setFont(QFont("Roboto", 9))

                    label = QLabel('Сумма вклада', group_box)
                    label.setGeometry(QRect(140, 25, 100, 30))
                    label.setFont(QFont("Roboto", 9))

                    text = QLabel(str(row[5]), group_box)
                    text.setGeometry(QRect(285, 25, 100, 30))
                    text.setFont(QFont("Roboto", 9))

                    label = QLabel('Cтавка', group_box)
                    label.setGeometry(QRect(10, 50, 45, 30))
                    label.setFont(QFont("Roboto", 9))

                    text = QLabel(str(row[7]) + '%', group_box)
                    text.setGeometry(QRect(55, 50, 100, 30))
                    text.setFont(QFont("Roboto", 9))

                    label = QLabel('Начисленные проценты', group_box)
                    label.setGeometry(QRect(140, 50, 140, 30))
                    label.setFont(QFont("Roboto", 9))

                    text = QLabel(str(row[8]), group_box)
                    text.setGeometry(QRect(285, 50, 100, 30))
                    text.setFont(QFont("Roboto", 9))

                    label = QLabel('Итогo', group_box)
                    label.setGeometry(QRect(140, 75, 40, 30))
                    label.setFont(QFont("Roboto", 9))

                    text = QLabel(str(row[9]), group_box)
                    text.setGeometry(QRect(285, 75, 100, 30))
                    text.setFont(QFont("Roboto", 9))

                    button_close = QPushButton('Закрыть информацию', self)
                    button_close.setGeometry(QRect(400, 170, 150, 30))
                    button_close.setFont(QFont("Roboto", 10))
                    button_close.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
                    button_close.clicked.connect(self.close)

                    button_delete = QPushButton('Удалить вклад', self)
                    button_delete.setGeometry(QRect(400, 130, 150, 30))
                    button_delete.setFont(QFont("Roboto", 10))
                    button_delete.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
                    button_delete.clicked.connect(lambda: self.delete_savings_account(index, mainwindow))
                    button_delete.clicked.connect(mainwindow.update_table)

    def delete_savings_account(self, index, mainwindow):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Удаление")
        dlg.setIcon(QMessageBox.Question)
        dlg.setText("Действительно хотите удалить сберегательный счет?")
        buttonAceptar = dlg.addButton("Да", QMessageBox.YesRole)
        buttonCancelar = dlg.addButton("Отмена", QMessageBox.RejectRole)
        dlg.setDefaultButton(buttonAceptar)
        dlg.exec_()

        if dlg.clickedButton() == buttonAceptar:
            with psycopg2.connect(database="kurs",
                                  user="postgres",
                                  password="Cactys14",
                                  host="localhost",
                                  port="5432"
                                  ) as conn:
                with conn.cursor() as cur:
                    cur.callproc('delete_savings_account', [index])
                mainwindow.update_table()
                self.close()
        else:
            pass

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class WindowInfoFamily(QWidget):
    def __init__(self, MainWindow, index):
        super().__init__()

        self.setWindowTitle(" ")
        self.resize(215, 250)
        self.center()

        surname = QLabel('Фамилия', self)
        surname.setGeometry(QRect(5, 5, 100, 30))
        surname.setFont(QFont("Roboto", 9))

        self.line_surname = QLineEdit(self)
        self.line_surname.setGeometry(QRect(110, 5, 100, 30))
        self.line_surname.setFont(QFont("Roboto", 9))

        name = QLabel('Имя', self)
        name.setGeometry(QRect(5, 40, 100, 30))
        name.setFont(QFont("Roboto", 9))

        self.line_name = QLineEdit(self)
        self.line_name.setGeometry(QRect(110, 40, 100, 30))
        self.line_name.setFont(QFont("Roboto", 9))

        patronymic = QLabel('Отчество', self)
        patronymic.setGeometry(QRect(5, 75, 100, 30))
        patronymic.setFont(QFont("Roboto", 9))

        self.line_patronymic = QLineEdit(self)
        self.line_patronymic.setGeometry(QRect(110, 75, 100, 30))
        self.line_patronymic.setFont(QFont("Roboto", 9))

        birthday = QLabel('День рождения', self)
        birthday.setGeometry(QRect(5, 110, 100, 30))
        birthday.setFont(QFont("Roboto", 9))

        self.set_birthday = QDateTimeEdit(QDateTime.currentDateTime(), self)
        self.set_birthday.setDisplayFormat("dd.MM.yyyy")
        self.set_birthday.setCalendarPopup(True)
        self.set_birthday.setTimeSpec(Qt.LocalTime)
        self.set_birthday.setGeometry(QRect(110, 110, 100, 30))
        self.set_birthday.setFont(QFont("Roboto", 9))

        status_in_family = QLabel('Статус в семье', self)
        status_in_family.setGeometry(QRect(5, 145, 100, 30))
        status_in_family.setFont(QFont("Roboto", 9))

        self.comboBox_status = QComboBox(self)
        self.comboBox_status.setGeometry(QRect(110, 145, 100, 30))
        self.comboBox_status.addItems(['Отец', 'Мать', 'Сын',
                                       'Дочь', 'Бабушка', 'Дедушка',
                                       'Прабабушка', 'Прадедушка', 'Тетя', 'Дядя'])

        gender = QLabel('Пол', self)
        gender.setGeometry(QRect(5, 180, 100, 30))
        gender.setFont(QFont("Roboto", 9))

        self.comboBox_gender = QComboBox(self)
        self.comboBox_gender.setGeometry(QRect(110, 180, 100, 30))
        self.comboBox_gender.addItems(['Мужской', 'Женский'])

        button_ok = QPushButton('Изменить', self)
        button_ok.setFont(QFont("Roboto", 9))
        button_ok.setGeometry(QRect(5, 215, 100, 30))
        button_ok.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
        button_ok.clicked.connect(lambda: self.update_member(index, MainWindow))

        button_cancel = QPushButton('Отмена', self)
        button_cancel.setFont(QFont("Roboto", 9))
        button_cancel.setGeometry(QRect(110, 215, 100, 30))
        button_cancel.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
        button_cancel.clicked.connect(self.close)

        with psycopg2.connect(database="kurs",
                              user="postgres",
                              password="Cactys14",
                              host="localhost",
                              port="5432"
                              ) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM family_member WHERE id = ' + str(index))
                for row in cur:
                    self.line_surname.setText(row[1])
                    self.line_name.setText(row[2])
                    self.line_patronymic.setText(row[3])
                    self.set_birthday.setDate(row[4])
                    status = ['Отец', 'Мать', 'Сын',
                              'Дочь', 'Бабушка', 'Дедушка',
                              'Прабабушка', 'Прадедушка', 'Тетя', 'Дядя']
                    self.comboBox_status.setCurrentIndex(status.index(row[5]))
                    self.comboBox_gender.setCurrentIndex(['Мужской', 'Женский'].index(row[6]))

    def update_member(self, index, MainWindow):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Изменение")
        dlg.setIcon(QMessageBox.Question)
        dlg.setText("Действительно хотите изменить данные?")
        buttonAceptar = dlg.addButton("Да", QMessageBox.YesRole)
        buttonCancelar = dlg.addButton("Отмена", QMessageBox.RejectRole)
        dlg.setDefaultButton(buttonAceptar)
        dlg.exec_()

        if dlg.clickedButton() == buttonAceptar:
            with psycopg2.connect(database="kurs",
                                  user="postgres",
                                  password="Cactys14",
                                  host="localhost",
                                  port="5432"
                                  ) as conn:
                with conn.cursor() as cur:
                    cur.callproc('update_family_member', [index,
                                                          self.line_surname.text(),
                                                          self.line_name.text(),
                                                          self.line_patronymic.text(),
                                                          self.set_birthday.dateTime().toString('yyyy-MM-dd'),
                                                          self.comboBox_status.currentText(),
                                                          self.comboBox_gender.currentText()])
            MainWindow.update_list_family()
            MainWindow.update_all_table_income()
            self.close()
        else:
            pass

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class WindowAddFamily(QWidget):
    def __init__(self, MainWindow):
        super().__init__()

        self.setWindowTitle(" ")  # Заголовок окна
        self.resize(215, 250)  # Размер окна
        self.center()

        surname = QLabel('Фамилия', self)
        surname.setGeometry(QRect(5, 5, 100, 30))
        surname.setFont(QFont("Roboto", 9))

        self.line_surname = QLineEdit(self)
        self.line_surname.setGeometry(QRect(110, 5, 100, 30))
        self.line_surname.setFont(QFont("Roboto", 9))

        name = QLabel('Имя', self)
        name.setGeometry(QRect(5, 40, 100, 30))
        name.setFont(QFont("Roboto", 9))

        self.line_name = QLineEdit(self)
        self.line_name.setGeometry(QRect(110, 40, 100, 30))
        self.line_name.setFont(QFont("Roboto", 9))

        patronymic = QLabel('Отчество', self)
        patronymic.setGeometry(QRect(5, 75, 100, 30))
        patronymic.setFont(QFont("Roboto", 9))

        self.line_patronymic = QLineEdit(self)
        self.line_patronymic.setGeometry(QRect(110, 75, 100, 30))
        self.line_patronymic.setFont(QFont("Roboto", 9))

        birthday = QLabel('День рождения', self)
        birthday.setGeometry(QRect(5, 110, 100, 30))
        birthday.setFont(QFont("Roboto", 9))

        self.set_birthday = QDateTimeEdit(QDateTime.currentDateTime(), self)
        self.set_birthday.setDisplayFormat("dd.MM.yyyy")
        self.set_birthday.setCalendarPopup(True)
        self.set_birthday.setTimeSpec(Qt.LocalTime)
        self.set_birthday.setGeometry(QRect(110, 110, 100, 30))
        self.set_birthday.setFont(QFont("Roboto", 9))

        status_in_family = QLabel('Статус в семье', self)
        status_in_family.setGeometry(QRect(5, 145, 100, 30))
        status_in_family.setFont(QFont("Roboto", 9))

        self.comboBox_status = QComboBox(self)
        self.comboBox_status.setGeometry(QRect(110, 145, 100, 30))
        self.comboBox_status.addItems(['Отец', 'Мать', 'Сын',
                                       'Дочь', 'Бабушка', 'Дедушка',
                                       'Прабабушка', 'Прадедушка', 'Тетя', 'Дядя'])

        gender = QLabel('Пол', self)
        gender.setGeometry(QRect(5, 180, 100, 30))
        gender.setFont(QFont("Roboto", 9))

        self.comboBox_gender = QComboBox(self)
        self.comboBox_gender.setGeometry(QRect(110, 180, 100, 30))
        self.comboBox_gender.addItems(['Мужской', 'Женский'])

        button_ok = QPushButton('Добавить', self)
        button_ok.setFont(QFont("Roboto", 9))
        button_ok.setGeometry(QRect(5, 215, 100, 30))
        button_ok.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
        button_ok.clicked.connect(self.add_member)
        button_ok.clicked.connect(self.close)
        button_ok.clicked.connect(MainWindow.update_list_family)

        button_cancel = QPushButton('Отмена', self)
        button_cancel.setFont(QFont("Roboto", 9))
        button_cancel.setGeometry(QRect(110, 215, 100, 30))
        button_cancel.setStyleSheet('QPushButton {background-color: #2D4262; color: #ffffff;}')
        button_cancel.clicked.connect(self.close)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def add_member(self):
        with psycopg2.connect(database="kurs",
                              user="postgres",
                              password="Cactys14",
                              host="localhost",
                              port="5432"
                              ) as conn:
            with conn.cursor() as cur:
                cur.callproc('add_family_member', [self.line_surname.text(),
                                                   self.line_name.text(),
                                                   self.line_patronymic.text(),
                                                   self.set_birthday.dateTime().toString('yyyy-MM-dd'),
                                                   self.comboBox_status.currentText(),
                                                   self.comboBox_gender.currentText()])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    win = MainWindow()
    win.show()

    sys.exit(app.exec_())
