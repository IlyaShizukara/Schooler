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
                self.homeworks = data.get("homeworks", [])
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

    def show_shedule(self):
        print('\n' + '-'*50)
        print('Расписание Уроков'.upper())
        print('-'*50)

        print('\n1. Показать всю неделю')
        print('2. Показать конкретный день')
        choice = input("Выберите вариант: ")

        if choice == "1":
            for day, subjects in self.schedule.items():
                print(f'\n{day}:')
                for i, subject in enumerate(subjects, 1):
                    print(f'  {i}. {subject}')
        elif choice == '2':
            print('\nДни недели:', ', '.join(self.schedule.keys()))
            day = input("Выберите день: ")
            print(f'\n{day}:')
            if day in self.schedule:
                for i, subject in enumerate(self.schedule[day], 1):
                    print(f'  {i}. {subject}')
            else:
                print("День не найден!")

    def add_homework(self):
        print('\n' + '-'*50)
        print('Добавление Домашнего задания'.upper())
        print('-'*50)

        subject = input('Предмет: ')
        task = input('Задание: ')
        date = input('Дата сдачи: ')

        homework = {
            'subject': subject,
            'task': task,
            'date': date,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.homeworks.append(homework)
        self.save_data()

    def show_homework(self):
        print('\n' + '-'*50)
        print('Домашние задания'.upper())
        print('-'*50)

        if not self.homeworks:
            print('Нет домшнего задания')
            return

        for i, hw, in enumerate(self.homeworks, 1):
            print(f'\n{i}. {hw['subject']}')
            print(f"    Задание: {hw["task"]}")
            print(f"    Сдать до: {hw["date"]}")
            print(f"    Добавлено: {hw["created_at"]}")

    def remove_homework(self):
        self.show_homework()
        if self.homeworks:
            try:
                num = int(input("\nНомер задания для удаления: ")) - 1
                if 0 <= num < len(self.homeworks):
                    removed = self.homeworks.pop(num)
                    self.save_data()
                    print(f"Задание по {removed['subject']} успешно удалено")
                else:
                    print('Неверный номер!')
            except ValueError:
                print("Введите число!")

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
        print("\t\tSCHOOLER")
        print('-'*30)

        print('1. Расписание уроков')
        print('2. Домашние задания')
        print('3. Полезные ссылки')
        print('4. Добавить домашнее задание')
        print('5. Удалить домащнее задания')
        print('6. Сохранить данные')
        print('7. Показать день')
        print('8. Показать всю неделю')
        print('0. Выход')


def main():
    app = Schooler()

    while True:
        app.show_menu()
        choice = input('Выберите действие: ')

        if choice == '1':
            app.show_shedule()
        elif choice == '2':
            app.show_homework()
        elif choice == '3':
            app.manage_links()
        elif choice == '4':
            app.add_homework()
        elif choice == '5':
            app.remove_homework()
        elif choice == '6':
            app.save_data()
            print('Данные успешно сохранены')
        elif choice == '7':
            app.show_day(input('Введите день: '))
        elif choice == '8':
            app.show_all_week()
        elif choice == '0':
            print('До свидания!')
            break
        else:
            print("Неверный выбор! Попробуйте ещё раз!")

        input("\nНажмите Enter для продолжения")


if __name__ == '__main__':
    main()
