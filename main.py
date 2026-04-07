import flet as ft
from Schooler import Schooler
from datetime import datetime


def main(page: ft.Page):
    page.title = "Schooler"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 700
    page.window_resizable = False
    page.padding = 20

    app = Schooler()

    def update_content(content):
        page.controls.clear()
        page.add(content)
        page.update()

    def show_main_menu():
        title = ft.Text("Schooler".upper(), size=28, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

        btn_schedule = ft.ElevatedButton(
            "Расписание",
            on_click=lambda _: show_days_list('schedule'),
            width=300,
            height=50
        )
        btn_homework = ft.ElevatedButton(
            "Домашнее задание",
            on_click=lambda _: show_days_list('homework'),
            width=300,
            height=50
        )
        btn_tomorrow_hw = ft.ElevatedButton(
            "Домашка на завтра",
            on_click=lambda _: show_tomorrow_homework(),
            width=300,
            height=50
        )
        btn_search = ft.ElevatedButton(
            "Поиск",
            on_click=lambda _: show_search(),
            width=300,
            height=50
        )
        btn_add_hw = ft.ElevatedButton(
            "Добавить домашку",
            on_click=lambda _: show_add_homework(),
            width=300,
            height=50
        )

        content = ft.Column(
            [
                ft.Container(height=20),
                title,
                ft.Container(height=30),
                btn_schedule,
                ft.Container(height=10),
                btn_homework,
                ft.Container(height=10),
                btn_tomorrow_hw,
                ft.Container(height=10),
                btn_search,
                ft.Container(height=10),
                btn_add_hw

            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        update_content(content)

    def show_days_list(mode):
        title = ft.Text("Выберите день", size=24, weight=ft.FontWeight.BOLD)

        day_buttons = []
        for day in app.schedule.keys():
            btn = ft.ElevatedButton(
                day,
                on_click=lambda _, d=day: show_day_detail(d, mode),
                width=250
            )
            day_buttons.append(btn)

        back_btn = ft.TextButton(
            "<- Назад",
            on_click=lambda _: show_main_menu()
        )

        content = ft.Column(
            [title, ft.Container(height=20)] + day_buttons + [ft.Container(height=20), back_btn],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        update_content(content)

    def show_day_detail(day, mode):
        title = ft.Text(day, size=24, weight=ft.FontWeight.BOLD)

        if mode == 'schedule':
            subjects = app.schedule.get(day, [])
            subjects_items = []
            for i, subject in enumerate(subjects, 1):
                subject_text = ft.Text(f"{i}. {subject}", size=16)

                subjects_items.append(subject_text)

            schedule_card = ft.Card(
                ft.Container(
                    content=ft.Column(
                        [ft.Text("Расписание", size=18, weight=ft.FontWeight.BOLD)] + subjects_items,
                        spacing=10

                    ),
                    padding=15
                )
            )

            content = ft.Column([title, ft.Container(height=20), schedule_card], spacing=10)

        else:
            day_hw = app.homeworks.get(day, {})
            non_empty = {s: t for s, t in day_hw.items() if t and t.strip()}

            if non_empty:
                hw_items = []
                for subject, task in non_empty.items():
                    hw_items.append(ft.Text(f"* {subject}: {task}", size=16))

                hw_card = ft.Card(
                    ft.Container(
                        content=ft.Column(
                            [ft.Text("Домашнее задание", size=18, weight=ft.FontWeight.BOLD)] + hw_items,
                            spacing=10
                        ),
                        padding=15
                    )
                )
            else:
                hw_card = ft.Card(
                    ft.Container(
                        content=ft.Text("Нет домашнего задания", size=16),
                        padding=15
                    )
                )

            content = ft.Column([title, ft.Container(height=20), hw_card], spacing=10)

        back_btn = ft.TextButton("<- Назад", on_click=lambda _: show_days_list(mode))
        content.controls.append(ft.Container(height=20))
        content.controls.append(back_btn)

        update_content(ft.Column([content], horizontal_alignment=ft.CrossAxisAlignment.CENTER))

    def show_tomorrow_homework():
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

        # Ищем следующий учебный день
        for offset in range(1, 8):
            next_index = (today_index + offset) % 7
            next_en = days_order[next_index]
            next_ru = weekdays[next_en]

            if next_ru in app.schedule:
                title_text = f"ЗАВТРА, {next_ru.upper()}" if offset == 1 else f"БЛИЖАЙШИЙ ДЕНЬ ({next_ru.upper()})"

                title = ft.Text(title_text, size=22, weight=ft.FontWeight.BOLD)

                subjects = app.schedule.get(next_ru, [])
                subject_items = []
                for i, subject in enumerate(subjects, 1):
                    subject_items.append(ft.Text(f"{i}. {subject}", size=16))

                schedule_card = ft.Card(
                    ft.Container(
                        content=ft.Column(
                            [ft.Text("Расписание", size=18, weight=ft.FontWeight.BOLD)] + subject_items,
                            spacing=10

                        ),
                        padding=15
                    )
                )
                day_hw = app.homeworks.get(next_ru, {})
                non_empty = {s: t for s, t in day_hw.items() if t and t.strip()}

                if non_empty:
                    hw_items = [ft.Text(f"* {s}: {t}", size=16) for s, t in non_empty.items()]

                    hw_card = ft.Card(
                        ft.Container(
                            content=ft.Column(
                                [ft.Text("Домашнее задание", size=18, weight=ft.FontWeight.BOLD)] + hw_items,
                                spacing=10
                            ),
                            padding=15
                        )
                    )
                else:
                    hw_card = ft.Card(
                        ft.Container(
                            content=ft.Text("Нет домашнего задания", size=16),
                            padding=15
                        )
                    )

                back_btn = ft.TextButton("<- Назад", on_click=lambda _: show_main_menu())

                content = ft.Column(
                    [title, ft.Container(height=20), schedule_card, ft.Container(height=10),
                     hw_card, ft.Container(height=20), back_btn],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )

                update_content(content)
                return

        content = ft.Column([
            ft.Text("Нет учебных дней", size=20),
            ft.TextButton("<- Назад", on_click=lambda _: show_main_menu())
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        update_content(content)

    def show_search():
        search_field = ft.TextField(
            label="Введите предмет",
            width=300,
            autofocus=True
        )

        results_text = ft.Text("", size=14)

        def do_search(e):
            query = search_field.value.lower()
            found = []

            for day, tasks in app.homeworks.items():
                for subject, task in tasks.items():
                    if task and task.strip() and query in subject.lower():
                        found.append(f"{day} | {subject}: {task}")

            if found:
                results_text.value = "\n".join(found)
            else:
                results_text.value = "Ничего не найдено"
            page.update()

        search_btn = ft.ElevatedButton("Искать", on_click=do_search)
        back_btn = ft.TextButton("<- Назад", on_click=lambda _: show_main_menu())

        content = ft.Column([
            ft.Text("Поиск домашнего задания", size=24, weight=ft.FontWeight.BOLD),
            ft.Container(height=20),
            search_field,
            search_btn,
            ft.Container(height=20),
            results_text,
            ft.Container(height=20),
            back_btn
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        update_content(content)

    def show_add_homework():
        day_dropdown = ft.Dropdown(
            label="День недели",
            width=300,
            options=[ft.dropdown.Option(day) for day in app.schedule.keys()]
        )

        subject_dropdown = ft.Dropdown(
            label="Предмет",
            width=300,
            options=[],
            disabled=True
        )

        task_field = ft.TextField(
            label="Задание",
            width=300,
            multiline=True,
            min_lines=2,
            max_lines=4
        )

        status_text = ft.Text("", size=14, color=ft.Colors.GREEN)

        def update_subjects(day):
            if day and day in app.schedule:
                subject_options = [ft.dropdown.Option(subj) for subj in app.schedule[day]]
                subject_dropdown.options = subject_options
                subject_dropdown.disabled = False
                if subject_options:
                    subject_dropdown.value = subject_options[0].key
                status_text.value = ""
            else:
                subject_dropdown.options = []
                subject_dropdown.disabled = True
                subject_dropdown.value = None
            page.update()

        def on_day_change(e):
            update_subjects(day_dropdown.value)

        day_dropdown.on_select = on_day_change

        def add_homework_action(e):
            day = day_dropdown.value
            subject = subject_dropdown.value
            task = task_field.value.strip()

            if not day:
                status_text.value = "Выберите день"
                status_text.color = ft.Colors.RED
            elif not subject:
                status_text.value = "Выберите предмет"
                status_text.color = ft.Colors.RED
            elif not task:
                status_text.value = "Введите задание"
                status_text.color = ft.Colors.RED
            else:
                if day not in app.homeworks:
                    app.homeworks[day] = {}

                app.homeworks[day][subject] = task
                app.save_data()

                status_text.value = f"Добавлено! {day} | {subject}"
                status_text.color = ft.Colors.GREEN

                task_field.value = ""
                page.update()

        add_btn = ft.ElevatedButton("Добавить", on_click=add_homework_action)
        back_btn = ft.TextButton("← Назад", on_click=lambda _: show_main_menu())

        content = ft.Column([
            ft.Text("Добавить домашнее задание", size=24, weight=ft.FontWeight.BOLD),
            ft.Container(height=20),
            day_dropdown,
            ft.Container(height=20),
            subject_dropdown,
            ft.Container(height=20),
            task_field,
            ft.Container(height=20),
            add_btn,
            status_text,
            ft.Container(height=20),
            back_btn
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        update_content(content)

    show_main_menu()


if __name__ == '__main__':
    ft.app(target=main)
