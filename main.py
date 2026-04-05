import json
import os
from datetime import datetime


class Schooler:
    def __init__(self):
        self.schedule = {}
        self.homeworks = {}
        self.useful_links = []
        self.data_file = 'school_data.json'
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.schedule = data.get("schedule", {})
                self.homeworks = data.get("homeworks", {})
                self.useful_links = data.get("useful_links", [])

        else:
            pass  # значения по умолчанию
            self.save_data()

    def save_data(self):
        data = {
            'schedule': self.schedule,
            'homeworks': self.homeworks,
            'useful_links': self.useful_links,
        }
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def show_day(self, day):
        print('\n' + '-' * 50)
        print(day.upper())
        print('-' * 50)

        if day in self.schedule:
            print("\nРАСПИСАНИЕ")
            for i, subject in enumerate(self.schedule[day], 1):
                print(f' {i}. {subject}')
        else:
            print("День не найден!")

        print('\nДомашнее задания: '.upper())
        day_hw = self.homeworks.get(day, {})
        if day_hw:
            for subject, task in day_hw.items():
                print(f' * {subject}: {task}')
        else:
            print("Нет домашнего задания!")

    def show_all_week(self):
        for day in self.schedule.keys():
            self.show_day(day)

    def add_homework(self):
        print(f"\n{'-' * 50}")
        print("ДОБАВЛЕНИЕ ДОМАШНЕГО ЗАДАНИЯ")
        print(f"{'-' * 50}")

        print("\nДни недели:", ", ".join(self.schedule.keys()))
        day = input("Выберите день: ")

        if day not in self.schedule:
            print("День не найден!")
            return

        # Показываем предметы
        print(f"\nПредметы в {day}:")
        for i, subject in enumerate(self.schedule[day], 1):
            if (day in self.homeworks and
                    subject in self.homeworks[day] and
                    self.homeworks[day][subject] and
                    self.homeworks[day][subject].strip()):
                print(f"  {i}. {subject} (уже есть задание)")
            else:
                print(f"  {i}. {subject}")

        subject = input("\nВведите предмет: ")

        if subject not in self.schedule[day]:
            print(f"Предмет '{subject}' не найден!")
            return

        task = input("Введите задание: ").strip()

        if not task:
            print("Задание не может быть пустым!")
            return

        if (day in self.homeworks and
                subject in self.homeworks[day] and
                self.homeworks[day][subject] and
                self.homeworks[day][subject].strip()):
            print(f"\nУже есть задание: {self.homeworks[day][subject]}")
            rewrite = input("Заменить? (да/нет): ")
            if rewrite.lower() != "да":
                print("Отменено")
                return

        if day not in self.homeworks:
            self.homeworks[day] = {}

        self.homeworks[day][subject] = task
        self.save_data()

        print(f"\nДомашка добавлена!")
        print(f"   {day} | {subject} → {task}")

    def edit_homework(self):
        print(f"\n{'-' * 50}")
        print("РЕДАКТИРОВАНИЕ ДОМАШНЕГО ЗАДАНИЯ")
        print(f"{'-' * 50}")

        days_with_hw = []
        for day, tasks in self.homeworks.items():
            non_empty = {subj: task for subj, task in tasks.items() if task and task.strip()}
            if non_empty:
                days_with_hw.append(day)

        if not days_with_hw:
            print("\nНет домашних заданий!")
            return

        print("\nДни с домашними заданиями:")
        for day in days_with_hw:
            non_empty_count = len([t for t in self.homeworks[day].values() if t and t.strip()])
            print(f"  • {day} ({non_empty_count} заданий)")

        day = input("\nВыберите день: ")

        if day not in self.homeworks:
            print("На этот день нет заданий!")
            return

        non_empty_items = [(subj, task) for subj, task in self.homeworks[day].items() if task and task.strip()]

        if not non_empty_items:
            print("На этот день нет заданий!")
            return

        print(f"\nЗадания на {day}:")
        for i, (subject, task) in enumerate(non_empty_items, 1):
            print(f"  {i}. {subject}: {task}")

        print("\n1. Редактировать")
        print("2. Удалить")
        print("3. Назад")

        choice = input("Выберите: ")

        if choice == '1':
            subject = input("Предмет: ")
            if subject in self.homeworks[day]:
                current = self.homeworks[day][subject]
                if current:
                    print(f"Текущее: {current}")
                new_task = input("Новое задание: ").strip()

                if not new_task:
                    del self.homeworks[day][subject]
                    print(f"Задание удалено (было пустым)")
                else:
                    self.homeworks[day][subject] = new_task
                    print(f"Обновлено!")

                self.save_data()
            else:
                print("Не найдено!")

        elif choice == '2':
            subject = input("Предмет: ")
            if subject in self.homeworks[day]:
                del self.homeworks[day][subject]
                self.save_data()
                print(f"Удалено!")
            else:
                print("Не найдено!")

    def search_homework(self):
        query = input("\nВведите предмет: ").lower()
        found = []

        for day, tasks in self.homeworks.items():
            for subject, task in tasks.items():
                if query in subject.lower():
                    found.append((day, subject, task))

        if found:
            print(f"\nНайдено {len(found)}:")
            for day, subject, task in found:
                print(f"  * {day} | {subject}: {task}")
        else:
            print("Ничего не найдено")

    def get_tomorrow_homework(self):
        weekdays = {
            "Monday": "Понедельник",
            "Tuesday": "Вторник",
            "Wednesday": "Среда",
            "Thursday": "Четверг",
            "Friday": "Пятница",
            "Saturday": "Суббота",
            "Sunday": "Воскресенье"
        }

        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        today_en = datetime.now().strftime("%A")
        today_index = days_order.index(today_en)

        for offset in range(1, 8):
            next_index = (today_index + offset) % 7
            next_en = days_order[next_index]
            next_ru = weekdays[next_en]

            if next_ru in self.schedule:
                if offset == 1:
                    print(f"\nЗавтра, {next_ru.upper()}:")
                else:
                    print(f"Ближайший учебный день ({next_ru.upper()}):")
                self.show_day(next_ru)
                return

        print("Нет учебных дней в расписании!")

    def manage_links(self):
        while True:
            print('\n' + '-'*50)
            print("Полезные ссылки".upper())
            print('-'*50)

            if self.useful_links:
                print("\nСохранённые ссылки:")
                for i, link in enumerate(self.useful_links, 1):
                    print(f'{i}. {link['name']}: {link['url']}')
            else:
                print("Нет сохранённых ссылок")

            print('\n1. Добавить ссылку')
            print('2. Удалить ссылку')
            print('3. Назад')

            choice = input('Выберите действие:')

            if choice == '1':
                name = input("Название: ")
                url = input("Ссылка: ")
                self.useful_links.append({'name': name, 'url': url})
                self.save_data()
                print(f"Ссылка '{name}' успешно добавлена")
            elif choice == '2' and self.useful_links:
                try:
                    num = int(input('Номер ссылки для удаления: ')) - 1
                    if 0 <= num < len(self.useful_links):
                        removed = self.useful_links.pop(num)
                        self.save_data()
                        print(f"Ссылка {removed['name']} успешно удалена")
                except ValueError:
                    print("Введите число")
            elif choice == '3':
                break

    @staticmethod
    def show_menu():
        """Главное меню"""
        print('\n'+'-'*30)
        print("\tSCHOOLER")
        print('-'*30)

        print('1. Посмотреть день')
        print('2. Вся неделя')
        print('3. Добавить домашнее задание')
        print('4. Редактировать/удалить домащнее задания')
        print('5. Поиск по предмету')
        print('6. Домашка на завтра')
        print('7. Полезные ссылки')
        print('0. Выход')
        print('-' * 30)


def main():
    app = Schooler()

    while True:
        app.show_menu()
        choice = input('Выберите действие: ')

        if choice == '1':
            print("\nДни:", ", ".join(app.schedule.keys()))
            day = input("Введите день: ")
            if day in app.schedule:
                app.show_day(day)
            else:
                print("День не найден!")
        elif choice == '2':
            app.show_all_week()
        elif choice == '3':
            app.add_homework()
        elif choice == '4':
            app.edit_homework()
        elif choice == '5':
            app.search_homework()
        elif choice == '6':
            app.get_tomorrow_homework()
        elif choice == '7':
            app.manage_links()
        elif choice == '0':
            print('До свидания!')
            break
        else:
            print("Неверный выбор! Попробуйте ещё раз!")

        input("\nНажмите Enter для продолжения")


if __name__ == '__main__':
    main()
