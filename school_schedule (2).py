from deap import base, creator, tools, algorithms
import random
import numpy as np
import json
import pandas as pd
from tabulate import tabulate

# Определение входных данных
NUM_CLASSES = 5
NUM_SUBJECTS = 5
NUM_TEACHERS = 5
NUM_ROOMS = 5
NUM_DAYS = 5
NUM_PERIODS = 6
NUM_TIME_SLOTS = NUM_DAYS * NUM_PERIODS  # 30 временных слотов

classes = list(range(NUM_CLASSES))
subjects = list(range(NUM_SUBJECTS))
teachers = list(range(NUM_TEACHERS))
rooms = list(range(NUM_ROOMS))
time_slots = list(range(NUM_TIME_SLOTS))

# Какие предметы может вести каждый учитель (каждый учитель ведет 2-3 предмета)
teacher_subjects = {t: random.sample(subjects, k=random.randint(2, 3)) for t in teachers}

# Требуемое количество уроков для каждого класса по каждому предмету (от 3 до 5 часов)
required_lessons = {c: {s: random.randint(3, 5) for s in subjects} for c in classes}

# Настройка DEAP
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

# Размер индивидуума: NUM_TIME_SLOTS * NUM_ROOMS
IND_SIZE = NUM_TIME_SLOTS * NUM_ROOMS

def create_individual():
    individual = [(-1, -1, -1)] * IND_SIZE  # Изначально все слоты пусты
    lessons_to_schedule = []
    # Собираем все необходимые уроки
    for c in classes:
        for s in subjects:
            for _ in range(required_lessons[c][s]):
                lessons_to_schedule.append((c, s))
    random.shuffle(lessons_to_schedule)
    # Распределяем уроки по слотам
    used_slots = set()
    for c, s in lessons_to_schedule:
        possible_teachers = [t for t in teachers if s in teacher_subjects[t]]
        if not possible_teachers:
            continue  # Пропускаем, если нет подходящего учителя
        t = random.choice(possible_teachers)
        for _ in range(100):  # Ограничение попыток
            slot = random.randint(0, IND_SIZE - 1)
            if slot not in used_slots:
                individual[slot] = (c, s, t)
                used_slots.add(slot)
                break
    return individual

toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluate(individual):
    penalty = 0
    # Преобразуем индивидуум в расписание: time_slots x rooms
    schedule = [individual[i * NUM_ROOMS:(i + 1) * NUM_ROOMS] for i in range(NUM_TIME_SLOTS)]

    # Проверка конфликтов
    for t in range(NUM_TIME_SLOTS):
        assignments = [a for a in schedule[t] if a != (-1, -1, -1)]
        assigned_classes = [a[0] for a in assignments]
        assigned_teachers = [a[2] for a in assignments]
        # Конфликты классов
        class_counts = {c: assigned_classes.count(c) for c in set(assigned_classes)}
        for count in class_counts.values():
            if count > 1:
                penalty += (count - 1) * 1000  # Большой штраф за конфликт
        # Конфликты учителей
        teacher_counts = {t: assigned_teachers.count(t) for t in set(assigned_teachers)}
        for count in teacher_counts.values():
            if count > 1:
                penalty += (count - 1) * 1000

    # Проверка количества уроков
    for c in classes:
        class_lessons = [a[1] for ts in schedule for a in ts if a[0] == c and a != (-1, -1, -1)]
        for s in subjects:
            required = required_lessons[c][s]
            actual = class_lessons.count(s)
            penalty += abs(required - actual) * 100  # Штраф за несоответствие

    # Подсчет окон для классов
    for c in classes:
        for day in range(NUM_DAYS):
            day_slots = range(day * NUM_PERIODS, (day + 1) * NUM_PERIODS)
            class_day_schedule = [any(a[0] == c and a != (-1, -1, -1) for a in schedule[ts]) 
                                 for ts in day_slots]
            if any(class_day_schedule):
                first_lesson = class_day_schedule.index(True)
                last_lesson = len(class_day_schedule) - 1 - class_day_schedule[::-1].index(True)
                gaps = sum(1 for i in range(first_lesson + 1, last_lesson) if not class_day_schedule[i])
                penalty += gaps * 10  # Штраф за окна у школьников

    # Подсчет окон для учителей (меньший приоритет)
    for t in teachers:
        for day in range(NUM_DAYS):
            day_slots = range(day * NUM_PERIODS, (day + 1) * NUM_PERIODS)
            teacher_day_schedule = [any(a[2] == t and a != (-1, -1, -1) for a in schedule[ts]) 
                                   for ts in day_slots]
            if any(teacher_day_schedule):
                first_lesson = teacher_day_schedule.index(True)
                last_lesson = len(teacher_day_schedule) - 1 - teacher_day_schedule[::-1].index(True)
                gaps = sum(1 for i in range(first_lesson + 1, last_lesson) if not teacher_day_schedule[i])
                penalty += gaps * 2  # Меньший штраф за окна у учителей

    return penalty,

# Генетические операторы
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

# Запуск алгоритма
def main():
    random.seed(42)
    pop = toolbox.population(n=100)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", np.min)
    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.7, mutpb=0.2, ngen=50, 
                                   stats=stats, halloffame=hof, verbose=True)

    best_schedule = hof[0]
    print("Лучшее значение фитнеса:", best_schedule.fitness.values[0])

    # Выводим расписание в JSON
    schedule = [best_schedule[i * NUM_ROOMS:(i + 1) * NUM_ROOMS] for i in range(NUM_TIME_SLOTS)]
    json_schedule = []
    for day in range(NUM_DAYS):
        for period in range(NUM_PERIODS):
            ts = day * NUM_PERIODS + period
            for room, assignment in enumerate(schedule[ts]):
                if assignment != (-1, -1, -1):
                    c, s, tchr = assignment
                    json_schedule.append({
                        "day": day,
                        "period": period,
                        "room": room,
                        "class": c,
                        "subject": s,
                        "teacher": tchr
                    })

    with open("schedule.json", "w") as f:
        json.dump({"schedule": json_schedule}, f, indent=2)

    return pop, log, hof

def visualize_schedule(json_file):
    # Загружаем JSON-файл
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Преобразуем данные в DataFrame
    df = pd.DataFrame(data['schedule'])
    
    # Группируем данные по дням и периодам
    grouped = df.groupby(['day', 'period'])
    
    # Создаем таблицу для каждого дня
    for day in range(5):  # Предполагаем, что дней 5
        day_schedule = []
        for period in range(6):  # Предполагаем, что периодов 6
            try:
                period_data = grouped.get_group((day, period))
                for _, row in period_data.iterrows():
                    day_schedule.append([period, row['room'], row['class'], row['subject'], row['teacher']])
            except KeyError:
                # Если для этого периода нет занятий, пропускаем
                pass
        
        # Создаем DataFrame для текущего дня
        day_df = pd.DataFrame(day_schedule, columns=['Период', 'Кабинет', 'Класс', 'Предмет', 'Учитель'])
        
        # Выводим таблицу для дня
        print(f"\nРасписание на день {day + 1}:")
        print(tabulate(day_df, headers='keys', tablefmt='pretty', showindex=False))



if __name__ == "__main__":
    main()
    visualize_schedule("schedule.json")