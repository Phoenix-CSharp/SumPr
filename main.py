#импорты для графического интерфейса
import sys
import json
import random
from collections import defaultdict
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem, QLabel, QLineEdit,
                             QComboBox, QSpinBox, QFileDialog, QMessageBox, QHeaderView,
                             QDialog, QDialogButtonBox, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# импорты для генетического алгоритма
from deap import base, creator, tools, algorithms
import random
import numpy as np
import json
import pandas as pd
from tabulate import tabulate


class Class_range:
    CLASS_RANGE = { 
                        "1-11" : 0,
                        "1-4": 1,
                        "10-11": 2,
                        "1-6": 3,
                        "7-11": 4,
                        "5-11": 5,
                        "8-11": 6,
                        "5-6": 7,
                        "2-11": 8,
                        "5-8": 9,
                        "1-8": 10,
                        }
    def __init__(self, class_range: str = "1-11"):
        self.class_range = class_range
        self.type = self.CLASS_RANGE[class_range]

    def __call__(self, *key, **options) -> int | str | list[int] | None:
        """
            Обработчик события прямого обращения к экземпляру класса с заданными аргументами\n
            key == None | -1 => CLASS_RANGE[self.class_range]\n
            key == -2 => self.class_range\n
            key == -3 => list( map( int, self.class_range.split( "-" ) ) )\n
            key == 1 and arg != None => CLASS_RANGE[arg] if arg in CLASS_RANGE\n
            key == 2 and arg != None => _key == [(k, t) for (k, t) in CLASS_RANGE.items()\\
            if arg in CLASS_RANGE.values() and t == arg][0]\n
            key == 3 and arg != None => list( map( int, [(k, t) for (k, t) in CLASS_RANGE.items()\\
            if arg in CLASS_RANGE.values() and t == arg][0]split( "-" ) ) )
        """
        _key = -1 if len(key) == 0 else key[0]
        _arg = options.get("arg", 0)

        if _key == -1:
            return self.type

        elif _key == -2:
            return self.class_range
        
        elif _key == -3:
            return list(map(int, self.class_range.split("-")))
        
        elif _key == 1 and _arg and _arg in self.CLASS_RANGE: 
            return self.CLASS_RANGE[_arg]
        
        elif _key == 2 and _arg in self.CLASS_RANGE.values():
            for _k, _t in self.CLASS_RANGE.items():
                if _t == _arg:
                    return _k
                
        elif _key == 3 and _arg in self.CLASS_RANGE.values():
            for _k, _t in self.CLASS_RANGE.items():
                if _t == _arg:
                    return list(map(int, _k.split("-")))
                
        else: return None
        

class Teacher_type:
    subjects_dic = {
                        "Учитель математики": ["Математика", "Алгебра", "Геометрия", "Экономика", "ВиС", "Разговоры о важном", "Индивидуальный проект"],
                        "Учитель русского и литературы": ["Русский язык", "Литература", "Разговоры о важном", "Индивидуальный проект"],
                        "Учитель физической культуры": ["Физ-ра", "Разговоры о важном"],
                        "Учитель информатики": ["Информатика", "Разговоры о важном", "Индивидуальный проект"],
                        "Учитель технологии": ["Технология", "Разговоры о важном"],
                        "Учитель музыки": ["Музыка", "Разговоры о важном"],
                        "Учитель географии": ["География", "Разговоры о важном"],
                        "Учитель биологии": ["Биология", "Разговоры о важном", "Индивидуальный проект"], 
                        "Учитель химии": ["Химия", "Разговоры о важном", "Индивидуальный проект"],
                        "Учитель физики": ["Физика", "Астрономия", "Разговоры о важном", "Индивидуальный проект"],
                        "Учитель ОБЖ": ["ОБЖ", "Разговоры о важном"],
                        "Учитель истории и обществознания": ["История", "Обществознание", "Право", "Разговоры о важном", "Индивидуальный проект"],
                        "Учитель иностранного языка": ["Иностранный язык", "Разговоры о важном", "Индивидуальный проект"],
                        "Учитель изобразительного искусства": ["ИЗО", "Разговоры о важном", "МХК", "Индивидуальный проект"],
                        "Учитель начальных классов": ["Русский язык", "Математика", "Труд", "Окружающий мир", "Чтение", "Разговоры о важном"]
                    }
                    
    def __init__(self, type: str):
        self.type = type
        self.subjetcs = self.subjects_dic[type]

    def __call__(self, *key):
        _key = -1 if len(key) == 0 else key[0]
        if _key == -1: 
            return self.type
        else: 
            return self.subjetcs
    def __eq__(self, name: str = ""):
        return self.name == name if isinstance(name, str) else False
        

class Subject:
    def __init__(self, name: str = "", hours: int = 0 , room_type: str = "", class_range: Class_range = Class_range("1-11")):
        self.name = name
        self.hours = hours
        self.room_type = room_type
        self.class_range = class_range

    def __eq__(self, name: str = ""):
        return self.name == name if isinstance(name, str) else False


class Teacher:
    def __init__(self, name: str = "", type: Teacher_type = None):
        self.name = name
        self.type = type
        self.subjects = self.type()
    def __eq__(self, type: str = ""):
        return self.type == type if isinstance(type, str) else False


class Classroom:
    def __init__(self, number: str = "", room_type: str =""):
        self.number = number
        self.room_type = room_type
    def __eq__(self, room_type: str = ""):
        return self.room_type == room_type if isinstance(room_type, str) else False


class SchoolClass:
    def __init__(self, name: str = "", subjects: dict = None):
        self.name = name
        # Словарь предметов: {название предмета: часы в неделю}
        self.subjects = subjects if subjects else {}
        self.schedule = {}


class Scheduler:
    DAYS = ["Пн", "Вт", "Ср", "Чт", "Пт"]  # Дни недели
    MAX_SLOTS = 7  # Максимальное количество уроков в день
    MAX_CLASS_LESSONS_PER_DAY = 8  # Максимум уроков в день для класса

    def __init__(self):
        self.teachers = []
        self.classrooms = []
        self.subjects = []
        self.classes = []
        self.schedule = {}
        self.init_enter_value()

    def init_enter_value(self):
        """Инициализируем входные значения для алгоритма"""
        self.num_classes = len(self.classes)
        self.num_subjects = len(self.subjects)
        self.num_teachers = len(self.teachers)
        self.num_classrooms = len(self.classrooms)
        self.num_days = len(self.DAYS)
        self.num_periods = self.MAX_CLASS_LESSONS_PER_DAY
        self.num_time_slots = self.num_days * self.num_periods  # 30 временных слотов
        self.teacher_subjects = {t.name: t.subjects for t in self.teachers} if self.teachers else {}
        self.required_lessons = {c.name: c.subjects for c in self.classes} if self.classes else {}
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)
        self.ind_size = self.num_time_slots * self.num_classrooms

    def create_individual(self):
        individual = [(-1, -1, -1)] * self.ind_size
        lessons_to_schedule = []
        for c in self.classes:
            for s in self.subjects:
                for _ in range(self.required_lessons[c.name][s.name]):
                    lessons_to_schedule.append((c, s))
        random.shuffle(lessons_to_schedule)
        # Распределяем уроки по слотам
        used_slots = set()
        for c, s in lessons_to_schedule:
            possible_teachers = [t for t in self.teachers if s in self.teacher_subjects[t.name]]
            if not possible_teachers:
                continue
            t = random.choice(self.possible_teachers)
            for _ in range(500):
                slot = random.choice(0, self.ind_size - 1)
                if slot not in used_slots:
                    individual[slot] = (c, s, t)
                    used_slots.add(slot)
                    break
        return individual
    
    def toolbox_init(self):
        self.toolbox = base.Toolbox()
        self.toolbox.register("individual", tools.initIterate, creator.Individual, self.create_individual)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

    def evalute(self, individual: tuple[int, int, int]):
        penalty = 0
        schedule = [individual[i * self.num_classrooms:(i + 1) * self.num_classrooms] for i in range(self.num_time_slots)]

        for t in range(self.num_time_slots):
            assigments = [a for a in schedule[t] if a != (-1, -1, -1)]
            assigned_classes = [a[0] for a in assigments]
            assigned_teachers = [a[2] for a in assigments]

            class_count = {c.name: assigned_classes.count(c.name) for c in set(assigned_classes)}
            for count in class_count.values():
                if count > 1: 
                    penalty += (count - 1) * 1000
class ClassSubjectsDialog(QDialog):
    """Диалоговое окно для добавления предметов в класс"""

    def __init__(self, class_obj, subjects, parent=None):
        super().__init__(parent)
        self.class_obj = class_obj
        self.subjects = subjects
        self.class_val = int("".join([s for s in self.class_obj.name if s in "0123456789"]))
        self.setWindowTitle(f"Предметы для класса {class_obj.name}")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout()

        # Форма добавления предмета
        form_layout = QGridLayout()

        self.subject_combo = QComboBox()
        self.subject_combo.addItems([s.name for s in subjects if self.class_val in range(s.class_range(3, arg = s.class_range())[0], s.class_range(3, arg = s.class_range())[1] + 1)])
        form_layout.addWidget(QLabel("Предмет:"), 0, 0)
        form_layout.addWidget(self.subject_combo, 0, 1)

        self.hours_spin = QSpinBox()
        self.hours_spin.setRange(1, 10)
        self.hours_spin.setValue(3)
        form_layout.addWidget(QLabel("Часов в неделю:"), 1, 0)
        form_layout.addWidget(self.hours_spin, 1, 1)

        self.add_btn = QPushButton("Добавить предмет")
        self.add_btn.clicked.connect(self.add_subject)
        form_layout.addWidget(self.add_btn, 2, 0, 1, 2)

        layout.addLayout(form_layout)

        # Таблица предметов класса
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Предмет", "Часов в неделю", "Действия"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        # Кнопки диалога
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)
        self.update_table()

    def update_table(self):
        self.table.setRowCount(len(self.class_obj.subjects))

        for row, (subject_name, hours) in enumerate(self.class_obj.subjects.items()):
            self.table.setItem(row, 0, QTableWidgetItem(subject_name))
            self.table.setItem(row, 1, QTableWidgetItem(str(hours)))

            # Кнопка удаления
            btn = QPushButton("Удалить")
            btn.clicked.connect(lambda _, s=subject_name: self.delete_subject(s))
            self.table.setCellWidget(row, 2, btn)

    def add_subject(self):
        subject_name = self.subject_combo.currentText()
        hours = self.hours_spin.value()

        # Проверяем, не добавлен ли уже этот предмет
        if subject_name in self.class_obj.subjects:
            QMessageBox.warning(self, "Ошибка", f"Этот предмет уже добавлен в {self.class_obj.name} класс")
            return

        # Добавляем предмет в класс
        self.class_obj.subjects[subject_name] = hours
        self.update_table()

    def delete_subject(self, subject_name):
        if subject_name in self.class_obj.subjects:
            del self.class_obj.subjects[subject_name]
            self.update_table()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scheduler = Scheduler()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Школьное расписание")
        self.setGeometry(100, 100, 1000, 700)

        # Создание вкладок
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Вкладка расписания
        self.schedule_tab = QWidget()
        self.tabs.addTab(self.schedule_tab, "Расписание")
        self.init_schedule_tab()

        # Вкладка классов
        self.classes_tab = QWidget()
        self.tabs.addTab(self.classes_tab, "Классы")
        self.init_classes_tab()

        # Вкладка предметов
        self.subjects_tab = QWidget()
        self.tabs.addTab(self.subjects_tab, "Предметы")
        self.init_subjects_tab()

        # Вкладка учителей
        self.teachers_tab = QWidget()
        self.tabs.addTab(self.teachers_tab, "Учителя")
        self.init_teachers_tab()

        # Вкладка кабинетов
        self.classrooms_tab = QWidget()
        self.tabs.addTab(self.classrooms_tab, "Кабинеты")
        self.init_classrooms_tab()

        # Вкладка помощи
        self.help_tab = QWidget()
        self.tabs.addTab(self.help_tab, "Помощь")
        self.init_help_tab()

        # Создание меню
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Файл")

        save_action = file_menu.addAction("Сохранить данные")
        save_action.triggered.connect(self.save_data)

        load_action = file_menu.addAction("Загрузить данные")
        load_action.triggered.connect(self.load_data)

        export_action = file_menu.addAction("Экспорт расписания")
        export_action.triggered.connect(self.export_schedule)

        # Статус бар
        self.statusBar().showMessage("Готово")

    def init_schedule_tab(self):
        layout = QVBoxLayout()

        # Кнопки управления
        btn_layout = QHBoxLayout()
        self.generate_btn = QPushButton("Сгенерировать расписание")
        self.generate_btn.clicked.connect(self.generate_schedule)
        btn_layout.addWidget(self.generate_btn)

        self.clear_btn = QPushButton("Очистить расписание")
        self.clear_btn.clicked.connect(self.clear_schedule)
        btn_layout.addWidget(self.clear_btn)

        layout.addLayout(btn_layout)

        # Таблица расписания
        self.schedule_table = QTableWidget()
        self.schedule_table.setColumnCount(8)
        self.schedule_table.setHorizontalHeaderLabels(
            ["Класс", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        )
        self.schedule_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.schedule_table)

        self.schedule_tab.setLayout(layout)

    def init_classes_tab(self):
        layout = QVBoxLayout()

        # Форма добавления класса
        form_layout = QHBoxLayout()

        self.class_name_input = QLineEdit()
        self.class_name_input.setPlaceholderText("Название класса")
        form_layout.addWidget(self.class_name_input)

        self.add_class_btn = QPushButton("Добавить класс")
        self.add_class_btn.clicked.connect(self.add_class)
        form_layout.addWidget(self.add_class_btn)

        layout.addLayout(form_layout)

        # Таблица классов
        self.classes_table = QTableWidget()
        self.classes_table.setColumnCount(4)
        self.classes_table.setHorizontalHeaderLabels(["Класс", "Количество предметов", "Действия", "X"])
        self.classes_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.classes_table)

        self.classes_tab.setLayout(layout)

    def init_subjects_tab(self):
        layout = QVBoxLayout()

        # Форма добавления предмета
        form_layout = QHBoxLayout()

        self.subject_name_input = QComboBox()
        self.subject_name_input.addItems([
                                            "", "Математика", "Алгебра", "Геометрия", "ВиС", "Информатика", "Окружающий мир", "География",
                                            "Биология", "Химия", "Физика", "ОБЖ", "Астрономия", "Обществознание", "История", "ОДНКР",
                                            "Право", "Экономика", "Разговоры о важном", "Русский язык", "Чтение", "Литература", "Иностранный язык",
                                            "Технология", "ИЗО", "Труд", "Музыка", "Физ-ра", "МХК", "Индивидуальный проект"])
        form_layout.addWidget(QLabel("Название предмета:"))
        form_layout.addWidget(self.subject_name_input)

        self.room_type_input = QComboBox()
        self.room_type_input.addItems([
                                        "", "Компьютерный класс", "Общепредметный", "Биология", "Химия",
                                        "Физика", "Астрономия", "Музей", "Актовый зал", "Мастерская",
                                        "Художественный зал", "Музыка", "Спортзал"])
        form_layout.addWidget(QLabel("Тип кабинета:"))
        form_layout.addWidget(self.room_type_input)

        self.class_range_input = QComboBox()
        self.class_range_input.addItems(["", "1-11", "1-4", "10-11", "1-6", "7-11", "5-11", "8-11", "5-6", "2-11", "5-8", "1-8"])
        form_layout.addWidget(QLabel("Границы классов:"))
        form_layout.addWidget(self.class_range_input)

        self.add_subject_btn = QPushButton("Добавить предмет")
        self.add_subject_btn.clicked.connect(self.add_subject)
        form_layout.addWidget(self.add_subject_btn)

        layout.addLayout(form_layout)

        # Таблица предметов
        self.subjects_table = QTableWidget()
        self.subjects_table.setColumnCount(4)
        self.subjects_table.setHorizontalHeaderLabels(["Предмет", "Тип кабинета", "Границы классов", "X"])
        self.subjects_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.subjects_table)

        self.subjects_tab.setLayout(layout)

    def init_teachers_tab(self):
        layout = QVBoxLayout()

        # Форма добавления учителя
        form_layout = QHBoxLayout()

        self.teacher_name_input = QLineEdit()
        self.teacher_name_input.setPlaceholderText("ФИО учителя")
        form_layout.addWidget(self.teacher_name_input)

        self.teacher_type_input = QComboBox()
        self.teacher_type_input.addItems([
                                                "Учитель математики", "Учитель русского и литературы", "Учитель физической культуры",
                                                "Учитель информатики", "Учитель технологии", "Учитель музыки", "Учитель географии",
                                                "Учитель биологии", "Учитель химии", "Учитель Физики",  "Учитель ОБЖ",
                                                "Учитель истории и обществознания", "Учитель иностранного языка", "Учитель изобразительного искусства",
                                                "Учитель начальных классов"])
        form_layout.addWidget(QLabel("Тип учителя:"))
        form_layout.addWidget(self.teacher_type_input)

        self.add_teacher_btn = QPushButton("Добавить учителя")
        self.add_teacher_btn.clicked.connect(self.add_teacher)
        form_layout.addWidget(self.add_teacher_btn)

        layout.addLayout(form_layout)

        # Таблица учителей
        self.teachers_table = QTableWidget()
        self.teachers_table.setColumnCount(4)
        self.teachers_table.setHorizontalHeaderLabels(["Учитель", "Тип учителя", "Предметы", "X"])
        self.teachers_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.teachers_table)

        self.teachers_tab.setLayout(layout)

    def init_classrooms_tab(self):
        layout = QVBoxLayout()

        # Форма добавления кабинета
        form_layout = QHBoxLayout()

        self.classroom_number_input = QLineEdit()
        self.classroom_number_input.setPlaceholderText("Номер кабинета")
        form_layout.addWidget(self.classroom_number_input)

        self.classroom_type_input = QComboBox()
        self.classroom_type_input.addItems(["", "Компьютерный класс", "Общепредметный", "Биология", "Химия",
                                            "Физика", "Астрономия", "Музей", "Актовый зал", "Мастерская",
                                            "Художественный зал", "Музыка", "Спортзал"])
        form_layout.addWidget(QLabel("Тип кабинета:"))
        form_layout.addWidget(self.classroom_type_input)

        self.add_classroom_btn = QPushButton("Добавить кабинет")
        self.add_classroom_btn.clicked.connect(self.add_classroom)
        form_layout.addWidget(self.add_classroom_btn)

        layout.addLayout(form_layout)

        # Таблица кабинетов
        self.classrooms_table = QTableWidget()
        self.classrooms_table.setColumnCount(3)
        self.classrooms_table.setHorizontalHeaderLabels(["Кабинет", "Тип", "Действия"])
        self.classrooms_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.classrooms_table)

        self.classrooms_tab.setLayout(layout)

    def init_help_tab(self):
        layout = QVBoxLayout()

        help_text = """
        <h2>Руководство пользователя</h2>

        <h3>Добавление предметов в класс</h3>
        <p>Для добавления предметов в учебный план класса:</p>
        <ol>
            <li>Перейдите на вкладку "Классы"</li>
            <li>Нажмите кнопку "Управление предметами" напротив нужного класса</li>
            <li>В открывшемся окне выберите предмет из списка</li>
            <li>Укажите количество часов в неделю</li>
            <li>Нажмите "Добавить предмет"</li>
            <li>После добавления всех предметов нажмите "ОК"</li>
        </ol>

        <p>Для удаления предмета из класса нажмите кнопку "Удалить" напротив предмета.</p>

        <h3>Генерация расписания</h3>
        <p>После добавления всех необходимых данных перейдите на вкладку "Расписание" 
        и нажмите кнопку "Сгенерировать расписание". Программа автоматически распределит 
        уроки по дням недели с учетом указанных часов и ограничений.</p>

        <h3>Ограничения</h3>
        <ul>
            <li>Один предмет не может преподаваться одновременно в разных классах</li>
            <li>Учитель не может вести два урока одновременно</li>
            <li>Кабинет не может использоваться двумя классами одновременно</li>
            <li>Специализированные предметы проводятся в соответствующих кабинетах</li>
        </ul>
        """

        help_label = QLabel(help_text)
        help_label.setFont(QFont("Arial", 11))
        help_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        help_label.setWordWrap(True)

        layout.addWidget(help_label)
        self.help_tab.setLayout(layout)

    def update_tables(self):
        # Обновление таблицы классов
        self.classes_table.setRowCount(len(self.scheduler.classes))
        for i, cls in enumerate(self.scheduler.classes):
            self.classes_table.setItem(i, 0, QTableWidgetItem(cls.name))
            self.classes_table.setItem(i, 1, QTableWidgetItem(str(len(cls.subjects))))

            # Кнопка управления предметами
            subjects_btn = QPushButton("Управление предметами")
            subjects_btn.clicked.connect(lambda _, c=cls: self.manage_class_subjects(c))
            self.classes_table.setCellWidget(i, 2, subjects_btn)

            btn = QPushButton("Удалить")
            btn.clicked.connect(lambda _, idx = i: self.delete_class(idx))
            self.classes_table.setCellWidget(i, 3, btn)

        # Обновление таблицы предметов
        self.subjects_table.setRowCount(len(self.scheduler.subjects))
        for i, subject in enumerate(self.scheduler.subjects):
            self.subjects_table.setItem(i, 0, QTableWidgetItem(subject.name))
            self.subjects_table.setItem(i, 1, QTableWidgetItem(subject.room_type))
            if subject.name == any(["Физ-ра", "Разговоры о важном", "Русский язык"]): print(subject.class_range())
            self.subjects_table.setItem(i, 2, QTableWidgetItem(subject.class_range(2, arg = subject.class_range())))

            btn = QPushButton("Удалить")
            btn.clicked.connect(lambda _, idx=i: self.delete_subject(idx))
            self.subjects_table.setCellWidget(i, 3, btn)

        # Обновление таблицы учителей
        self.teachers_table.setRowCount(len(self.scheduler.teachers))
        for i, teacher in enumerate(self.scheduler.teachers):
            self.teachers_table.setItem(i, 0, QTableWidgetItem(teacher.name))
            self.teachers_table.setItem(i, 1, QTableWidgetItem(teacher.type()))
            self.teachers_table.setItem(i, 2, QTableWidgetItem(", ".join(teacher.type(-2))))

            btn = QPushButton("Удалить")
            btn.clicked.connect(lambda _, idx=i: self.delete_teacher(idx))
            self.teachers_table.setCellWidget(i, 3, btn)

        # Обновление таблицы кабинетов
        self.classrooms_table.setRowCount(len(self.scheduler.classrooms))
        for i, room in enumerate(self.scheduler.classrooms):
            self.classrooms_table.setItem(i, 0, QTableWidgetItem(room.number))
            self.classrooms_table.setItem(i, 1, QTableWidgetItem(room.room_type))

            btn = QPushButton("Удалить")
            btn.clicked.connect(lambda _, idx=i: self.delete_classroom(idx))
            self.classrooms_table.setCellWidget(i, 2, btn)

    def add_class(self):
        name = self.class_name_input.text().strip()
        if name and (int("".join([s for s in name if s in "0123456789"])) > 0):
            # Создаем класс с пустым списком предметов
            self.scheduler.classes.append(SchoolClass(name, {}))
            self.class_name_input.clear()
            self.update_tables()
            self.statusBar().showMessage(f"Добавлен класс: {name}")
        else:
            QMessageBox.warning(self, "Ошибка", "Введите корректное название класса")

    def add_subject(self):
        name = self.subject_name_input.currentText() if self.subject_name_input.currentText() != "" else None
        room_type = self.room_type_input.currentText()
        class_rng = self.class_range_input.currentText()

        if name:
            self.scheduler.subjects.append(Subject(name, 0, room_type, Class_range(class_rng)))
            self.subject_name_input.setCurrentIndex(0)
            self.room_type_input.setCurrentIndex(0)
            self.class_range_input.setCurrentIndex(0)
            self.update_tables()
            self.statusBar().showMessage(f"Добавлен предмет: {name}")
        else:
            QMessageBox.warning(self, "Ошибка", "Выберете название предмета")

    def add_teacher(self):
        name = self.teacher_name_input.text().strip()
        teacher_type = Teacher_type(self.teacher_type_input.currentText())
        subjects = teacher_type.subjetcs
        n_flag = False
        t_flag = False

        if name and '.' in name and name.count('.') == 2:
            n_flag = True
        else:
            QMessageBox.warning(self, "Ошибка", "Введите ФИО учителя")

        if teacher_type != None:
            t_flag = True
        else:
            QMessageBox.warning(self, "Ошибка", "Введите тип учителя")

        if n_flag and t_flag:
            self.scheduler.teachers.append(Teacher(name, teacher_type))
            self.teacher_type_input.setCurrentText("")
            self.teacher_name_input.clear()
            self.update_tables()
            self.statusBar().showMessage(f"Добавлен учитель: {name}")

    def add_classroom(self):
        number = self.classroom_number_input.text().strip()
        room_type = self.classroom_type_input.currentText()

        if number and int(number) > 0:
            self.scheduler.classrooms.append(Classroom(number, room_type))
            self.classroom_number_input.clear()
            self.classroom_type_input.setCurrentIndex(0)
            self.update_tables()
            self.statusBar().showMessage(f"Добавлен кабинет: {number}")
        else:
            QMessageBox.warning(self, "Ошибка", "Введите номер кабинета")

    def delete_subject(self, index):
        _subject = self.scheduler.subjects.pop(index)
        self.update_tables()
        self.statusBar().showMessage(f"Удалён предмет: {_subject.name}")

    def delete_class(self, index):
        _class = self.scheduler.classes.pop(index)
        self.update_tables()
        self.statusBar().showMessage(f"Удалён класс: {_class.name}")

    def delete_teacher(self, index):
        teacher = self.scheduler.teachers.pop(index)
        self.update_tables()
        self.statusBar().showMessage(f"Удален учитель: {teacher.name}")

    def delete_classroom(self, index):
        room = self.scheduler.classrooms.pop(index)
        self.update_tables()
        self.statusBar().showMessage(f"Удален кабинет: {room.number}")

    def manage_class_subjects(self, class_obj):
        """Открывает диалоговое окно для управления предметами класса"""
        dialog = ClassSubjectsDialog(class_obj, self.scheduler.subjects, self)
        if dialog.exec_() == QDialog.Accepted:
            self.update_tables()
            self.statusBar().showMessage(f"Предметы класса {class_obj.name} обновлены")

    def generate_schedule(self):
        try:
            if not self.scheduler.classes:
                QMessageBox.warning(self, "Ошибка", "Добавьте хотя бы один класс")
                return

            # Проверяем, что у всех классов есть предметы
            for cls in self.scheduler.classes:
                if not cls.subjects:
                    QMessageBox.warning(self, "Ошибка", f"Класс {cls.name} не имеет предметов!")
                    return

            schedule = self.scheduler.generate_schedule()
            self.schedule_table.setRowCount(len(self.scheduler.classes))

            days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

            for row, class_name in enumerate(schedule.keys()):
                class_schedule = schedule[class_name]
                self.schedule_table.setItem(row, 0, QTableWidgetItem(class_name))

                for col in range(1, 8):  # колонки 1-7: дни недели
                    if col <= 5:
                        # Получаем расписание для текущего дня
                        day_lessons = class_schedule.get(col, [])
                        lesson_lines = []

                        # Формируем список уроков с указанием времени и кабинета
                        for slot_index, lesson in enumerate(day_lessons):
                            if lesson:
                                # Добавляем информацию об уроке
                                lesson_info = f"{slot_index + 1}. {lesson['subject']}"
                                if lesson.get('classroom'):
                                    lesson_info += f" ({lesson['classroom']})"
                                lesson_lines.append(lesson_info)

                        lessons_str = "\n".join(lesson_lines) if lesson_lines else "Нет уроков"
                    else:
                        lessons_str = "Выходной"

                    self.schedule_table.setItem(row, col, QTableWidgetItem(lessons_str))

            self.statusBar().showMessage("Расписание успешно сгенерировано")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка генерации", f"Произошла ошибка при генерации расписания:\n{str(e)}")
            import traceback
            traceback.print_exc()

    def clear_schedule(self):
        self.schedule_table.setRowCount(0)
        self.statusBar().showMessage("Расписание очищено")

    def save_data(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить данные", "", "JSON Files (*.json)"
        )

        if file_path:
            data = {
                "classes": [{"name": cls.name, "subjects": cls.subjects} for cls in self.scheduler.classes],
                "subjects": [{"name": sub.name, "hours": sub.hours, "room_type": sub.room_type, "class_range": sub.class_range(2, arg = sub.class_range())}
                             for sub in self.scheduler.subjects],
                "teachers": [{"name": tch.name, "type": tch.type()} for tch in self.scheduler.teachers],
                "classrooms": [{"number": room.number, "room_type": room.room_type}
                               for room in self.scheduler.classrooms]
            }

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            self.statusBar().showMessage(f"Данные сохранены в {file_path}")

    def load_data(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Загрузить данные", "", "JSON Files (*.json)"
        )

        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                self.scheduler.classes = [
                    SchoolClass(item["name"], item.get("subjects", {})) for item in data["classes"]
                ]

                self.scheduler.subjects = [
                    Subject(item["name"], item["hours"], item["room_type"], Class_range(item["class_range"])) for item in data["subjects"]
                ]

                self.scheduler.teachers = [
                    Teacher(item["name"], Teacher_type(item["type"])) for item in data["teachers"]
                ]

                self.scheduler.classrooms = [
                    Classroom(item["number"], item["room_type"]) for item in data["classrooms"]
                ]

                self.update_tables()
                self.statusBar().showMessage(f"Данные загружены из {file_path}")

            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные: {str(e)}")

    def export_schedule(self):
        if not self.scheduler.schedule:
            QMessageBox.warning(self, "Ошибка", "Сначала сгенерируйте расписание")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Экспорт расписания", "", "Text Files (*.txt)"
        )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("ШКОЛЬНОЕ РАСПИСАНИЕ\n\n")

                    for class_name, class_schedule in self.scheduler.schedule.items():
                        f.write(f"===== Класс: {class_name} =====\n")

                        for day in range(1, 6):
                            f.write(f"\nДень {day}:\n")
                            lessons = class_schedule.get(day, [])

                            for slot_index, lesson in enumerate(lessons):
                                if lesson:
                                    f.write(
                                        f"{slot_index + 1}. {lesson['subject']} (Учитель: {lesson['teacher']}, Кабинет: {lesson['classroom']})\n")
                                else:
                                    f.write(f"{slot_index + 1}. ---\n")

                        f.write("\n" + "=" * 30 + "\n\n")

                self.statusBar().showMessage(f"Расписание экспортировано в {file_path}")

            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось экспортировать расписание: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())