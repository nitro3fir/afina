from vk import change_keyboard

def search_in_tree(tree, directory):
    copied_tree = tree
    for head in directory:
        copied_tree = copied_tree[head]
    return copied_tree

class StudentActions:

    @staticmethod
    def to_profile(student):
        student.append_directory('profile')
        return student.get_profile()

    @staticmethod
    def to_results(student):
        student.append_directory('results')

    @staticmethod
    def set_default_directory(student):
        student.set_default_directory()

    @staticmethod
    def pop_directory(student):
        student.pop_directory()

    class Profile:

        @staticmethod
        def to_region(student):
            student.append_directory('region')

        @staticmethod
        def determinate_region(student, reg_name):
            region_num = student.region_str_to_num(reg_name)
            if region_num == -1:
                answer = '\n\nСлишком много или мало символов'
            elif region_num == -2:
                answer = '\n\nНе удалось определить регион'
            else:
                student.append_directory(region_num)
                answer = 'Ваш регион: ' + student.region_num_to_str(region_num) + '?'
            return answer

        @staticmethod
        def region_agreed(student):
            student.change_region(user_directory[-1])
            actions_f.StudentActions.pop_directory(student)
            actions_f.StudentActions.pop_directory(student)

        @staticmethod
        def region_disagreed():
            actions_f.StudentActions.pop_directory(student)

    class Results:

        @staticmethod
        def keyboard_of_selected_subject(student, keyboard): 
            for index, subject in enumerate(student.get_subjects()):
                change_keyboard(keyboard, ("white", student.subject_short_name_to_full(subject)))
                if index % 2 == 1:
                    change_keyboard(keyboard, "add_line")

        @staticmethod
        def add_subject():
            student.append_directory("addsub")

        @staticmethod
        def remove_subject():
            student.append_directory("dropsub")

        class AddSub:

            @staticmethod
            def technical():
                student.append_directory("tech")

            @staticmethod
            def humanitarian():
                student.append_directory("humn")

            @staticmethod
            def natural():
                student.append_directory("ests")

            @staticmethod
            def languages():
                student.append_directory("lang")

            @staticmethod
            def subjects_keyboard(student, keyboard, sphere_of_activity):
                for tech_subject in enumerate({
                                              "tech": ('matp', 'matb', 'phys', 'infa'),
                                              "humn": ('obsh', 'litr', 'hist'),
                                              "ests": ('biol', 'chem', 'geog'),
                                              "lang": ('rusl')
                                              }.get(sphere_of_activity)):
                    if tech_subject not in student.get_subjects():
                        change_keyboard(keyboard, (tech_subject, "white"))
                        change_keyboard(keyboard, "add_line")
                

            @staticmethod
            def add_subject(student, sub_name):
                student.add_subject(sub_name)

        class DropSub:

            @staticmethod
            def subjects_keyboard(student, keyboard):
                for index, subject in enumerate(student.get_subjects()):
                    change_keyboard(keyboard, ("white", student.subject_short_name_to_full(subject)))
                    if index % 2 == 1:
                        change_keyboard(keyboard, "add_line")

            @staticmethod
            def drop_subject(student, sub_name):
                student.drop_subject(sub_name)

        class Subject:

            @staticmethod
            def get_selected_subject(student, sub_name):
                return student.subject_short_name_to_full(sub_name)

            @staticmethod
            def drop_last():
                student.append_directory('drop')

            @staticmethod
            def get_last():
                student.append_directory('see')

            @staticmethod
            def change_last():
                student.append_directory('change')

            @staticmethod
            def get_all():
                student.append_directory('seeall')

            @staticmethod
            def add():
                student.append_directory('add')

            class Add:

                @staticmethod
                def adding():
                    error = student.add_result(user_directory[2], event.text)
                    if error == -1:
                        error_message = 'Слишком мало или слишком много символов в результате'
                    elif error == -2:
                        error_message = 'В результате присутствуют посторонние символы'
                    elif error == -3:
                        error_message = 'Есть балл за задание, превышающий возможный'
                    elif error == -4:
                        error_message = 'Неверный формат времени выполнения'
                    elif error == -5:
                        error_message = 'Некорректное время выполнения: в часах, минутах или секундах более двух цифр'
                    elif error == -6:
                        error_message = 'Во времени выполнения присутствуют посторонние символы'
                    elif error == -7:
                        error_message = 'Указанное значение минут или секунд больше 60 или указанное значение часов больше 24'
                    elif error == -8:
                        error_message = 'Неверный формат пробника(возможно присутствуют лишние пробелы)'
                    else:
                        answer = 'Пробник успешно добавлен'
                        actions_f.StudentActions.pop_directory(student)

                @staticmethod
                def get_max_score():
                    answer = student.get_max_score(sub_name)

            class See:

                @staticmethod
                def see():
                    result = student.get_last_result(user_directory[2])
                    if result == -1:
                        error_message = 'Пробники отсутствуют'
                        user_directory = user_directory[0:-1]
                    else:
                        answer = result

            class SeeAll:

                @staticmethod
                def see():
                    result = student.get_all_results(user_directory[2])
                    if result == -1:
                        error_message = 'Пробники отсутствуют'
                        user_directory = user_directory[0:-1]
                    else:
                        answer = result

            #class Change:

            class Drop:

                @staticmethod
                def show_last():
                    answer = student.get_last_result(sub_name)

                @staticmethod
                def agreed():
                    student.drop_last_result(sub_name)

                @staticmethod
                def disagreed():
                    actions_f.StudentActions.pop_directory(student)

TREE = {
    "student": {
        "main": {
            "action": {
                "Пробники📊": "actions_f.StudentActions.to_results(student)",
                "Профиль🗿": "actions_f.StudentActions.to_profile(student)"
            },
            "answer": {
                "keyboard": [
                    [
                        "white",
                        "Профиль🗿"
                    ],
                    [
                        "white",
                        "Пробники📊"
                    ]
                ],
                "text": "Выберите раздел"
            },
            "profile": {
                "action": {
                    "Изменить регион🌍": "actions_f.StudentActions.Profile.to_region()",
                    "На главную 🏠": "actions_f.StudentActions.set_default_directory(student)",
                    "Назад ↩": "actions_f.StudentActions.pop_directory(student)"
                },
                "answer": {
                    "keyboard": [
                        [
                            "white",
                            "Изменить регион🌍"
                        ],
                        "add_line",
                        [
                            "blue",
                            "На главную 🏠"
                        ],
                        [
                            "blue",
                            "Назад ↩"
                        ]
                    ],
                    "text": ""
                },
                "region": {
                    "action": {
                        "any": "actions_f.StudentActions.Profile.determinate_region(student, event.text)",
                        "На главную 🏠": "actions_f.StudentActions.set_default_directory(student)",
                        "Назад ↩": "actions_f.StudentActions.pop_directory(student)"
                    },
                    "answer": {
                        "keyboard": [
                            [
                                "blue",
                                "На главную 🏠"
                            ],
                            [
                                "blue",
                                "Назад ↩"
                            ]
                        ],
                        "text": "Введите название региона"
                    },
                    "region_num": {
                        "action": {
                            "Да": "actions_f.StudentActions.Profile.region_agreed(student)",
                            "На главную 🏠": "actions_f.StudentActions.set_default_directory(student)",
                            "Назад ↩": "actions_f.StudentActions.pop_directory(student)",
                            "Нет": "actions_f.StudentActions.Profile.region_disagreed()"
                        },
                        "answer": {
                            "keyboard": [
                                [
                                    "red",
                                    "Нет"
                                ],
                                [
                                    "green",
                                    "Да"
                                ],
                                "add_line",
                                [
                                    "blue",
                                    "На главную 🏠"
                                ],
                                [
                                    "blue",
                                    "Назад ↩"
                                ]
                            ],
                            "text": ""
                        }
                    }
                }
            },
            "results": {
                "action": {
                    "default": "actions_f.StudentActions.Results.keyboard_of_selected_subject(student, keyboard)",
                    "Добавить предмет": "actions_f.StudentActions.Results.add_subject()",
                    "На главную 🏠": "actions_f.StudentActions.set_default_directory(student)",
                    "Назад ↩": "actions_f.StudentActions.pop_directory(student)",
                    "Удалить предмет": "actions_f.StudentActions.Results.remove_subject()"
                },
                "addsub": {
                    "action": {
                        "Гуманитарные науки📚": "actions_f.StudentActions.Results.AddSub.humanitarian()",
                        "Естественные науки🌍": "actions_f.StudentActions.Results.AddSub.natural()",
                        "На главную 🏠": "actions_f.StudentActions.set_default_directory(student)",
                        "Назад ↩": "actions_f.StudentActions.pop_directory(student)",
                        "Точные науки🔩": "actions_f.StudentActions.Results.AddSub.technical()",
                        "Языки✒": "actions_f.StudentActions.Results.AddSub.languages()"
                    },
                    "answer": {
                        "keyboard": [
                            [
                                "white",
                                "Точные науки🔩"
                            ],
                            [
                                "white",
                                "Гуманитарные науки📚"
                            ],
                            "add_line",
                            [
                                "white",
                                "Естественные науки🌍"
                            ],
                            [
                                "white",
                                "Языки✒"
                            ],
                            "add_line",
                            [
                                "blue",
                                "На главную 🏠"
                            ],
                            [
                                "blue",
                                "Назад ↩"
                            ]
                        ],
                        "text": "Выберите область для добавления предмета"
                    },
                    "ests": {
                        "action": {
                            "default": "actions_f.StudentActions.Results.AddSub.subjects_keyboard(student, keyboard, 'ests')",
                            "Биология🧬": "actions_f.StudentActions.Results.AddSub.add_subject(student, 'biol')",
                            "География🌍": "actions_f.StudentActions.Results.AddSub.add_subject(student, 'geog')",
                            "На главную 🏠": "actions_f.StudentActions.set_default_directory(student)",
                            "Назад ↩": "actions_f.StudentActions.pop_directory(student)",
                            "Химия🧪": "actions_f.StudentActions.Results.AddSub.add_subject(student, 'chem')"
                        },
                        "answer": {
                            "keyboard": [
                                [
                                    "blue",
                                    "На главную 🏠"
                                ],
                                [
                                    "blue",
                                    "Назад ↩"
                                ]
                            ],
                            "text": "Выберите предмет для добавления"
                        }
                    },
                    "humn": {
                        "action": {
                            "default": "actions_f.StudentActions.Results.AddSub.subjects_keyboard(student, keyboard, 'humn')",
                            "История📜": "actions_f.StudentActions.Results.AddSub.add_subject(student, 'hist')",
                            "Литература📚": "actions_f.StudentActions.Results.AddSub.add_subject(student, 'litr')",
                            "На главную 🏠": "actions_f.StudentActions.set_default_directory(student)",
                            "Назад ↩": "actions_f.StudentActions.pop_directory(student)",
                            "Обществознание💸": "actions_f.StudentActions.Results.AddSub.add_subject(student, 'obsh')"
                        },
                        "answer": {
                            "keyboard": [
                                [
                                    "white",
                                    "Обществознание💸"
                                ],
                                "add_line",
                                [
                                    "white",
                                    "Литература📚"
                                ],
                                [
                                    "white",
                                    "История📜"
                                ],
                                "add_line",
                                [
                                    "blue",
                                    "На главную 🏠"
                                ],
                                [
                                    "blue",
                                    "Назад ↩"
                                ]
                            ],
                            "text": "Выберите предмет для добавления"
                        }
                    },
                    "lang": {
                        "action": {
                            "default": "actions_f.StudentActions.Results.AddSub.subjects_keyboard(student, keyboard, 'lang')",
                            "На главную 🏠": "actions_f.StudentActions.set_default_directory(student)",
                            "Назад ↩": "actions_f.StudentActions.pop_directory(student)",
                            "Русский язык✒": "actions_f.StudentActions.Results.AddSub.add_subject(student, 'rusl')"
                        },
                        "answer": {
                            "keyboard": [
                                [
                                    "white",
                                    "Русский язык✒"
                                ],
                                "add_line",
                                [
                                    "blue",
                                    "На главную 🏠"
                                ],
                                [
                                    "blue",
                                    "Назад ↩"
                                ]
                            ],
                            "text": "Выберите предмет для добавления"
                        }
                    },
                    "tech": {
                        "action": {
                            "default": "actions_f.StudentActions.Results.AddSub.subjects_keyboard(student, keyboard, 'tech')",
                            "Информатика💻": "actions_f.StudentActions.Results.AddSub.add_subject(student, 'infa')",
                            "Математика база📏": "actions_f.StudentActions.Results.AddSub.add_subject(student, 'matb')",
                            "Математика профиль📐": "actions_f.StudentActions.Results.AddSub.add_subject(student, 'matp')",
                            "На главную 🏠": "actions_f.StudentActions.set_default_directory(student)",
                            "Назад ↩": "actions_f.StudentActions.pop_directory(student)",
                            "Физика🔩": "actions_f.StudentActions.Results.AddSub.add_subject(student, 'phys')"
                        },
                        "answer": {
                            "keyboard": [
                                [
                                    "blue",
                                    "На главную 🏠"
                                ],
                                [
                                    "blue",
                                    "Назад ↩"
                                ]
                            ],
                            "text": "Выберите предмет для добавления"
                        }
                    }
                },
                "answer": {
                    "keyboard": [
                        [
                            "red",
                            "Удалить предмет"
                        ],
                        [
                            "green",
                            "Добавить предмет"
                        ],
                        "add_line",
                        [
                            "blue",
                            "На главную 🏠"
                        ],
                        [
                            "blue",
                            "Назад ↩"
                        ]
                    ],
                    "text": "Выберите предмет"
                },
                "dropsub": {
                    "action": {
                        "default": "actions_f.StudentActions.Results.DropSub.subjects_keyboard(student, keyboard)",
                        "Биология🧬": "actions_f.StudentActions.Results.DropSub.drop_subject(student, 'biol')",
                        "География🌍": "actions_f.StudentActions.Results.DropSub.drop_subject(student, 'geog')",
                        "Информатика💻": "actions_f.StudentActions.Results.DropSub.drop_subject(student, 'infa')",
                        "История📜": "actions_f.StudentActions.Results.DropSub.drop_subject(student, 'hist')",
                        "Литература📚": "actions_f.StudentActions.Results.DropSub.drop_subject(student, 'litr')",
                        "Математика база📏": "actions_f.StudentActions.Results.DropSub.drop_subject(student, 'matb')",
                        "Математика профиль📐": "actions_f.StudentActions.Results.DropSub.drop_subject(student, 'matp')",
                        "На главную 🏠": "actions_f.StudentActions.set_default_directory(student)",
                        "Назад ↩": "actions_f.StudentActions.pop_directory(student)",
                        "Обществознание💸": "actions_f.StudentActions.Results.DropSub.drop_subject(student, 'obsh')",
                        "Русский язык✒": "actions_f.StudentActions.Results.DropSub.drop_subject(student, 'rusl')",
                        "Физика🔩": "actions_f.StudentActions.Results.DropSub.drop_subject(student, 'phys')",
                        "Химия🧪": "actions_f.StudentActions.Results.DropSub.drop_subject(student, 'chem')"
                    },
                    "answer": {
                        "keyboard": [
                            [
                                "blue",
                                "На главную 🏠"
                            ],
                            [
                                "blue",
                                "Назад ↩"
                            ]
                        ],
                        "text": "Выберите предмет для удаления"
                    }
                },
                "subname": {
                    "action": {
                        "default": "actions_f.StudentActions.Results.Subject.get_selected_subject(student, sub_name)",
                        "Добавить": "actions_f.StudentActions.Results.Subject.add()",
                        "Изменить последний": "actions_f.StudentActions.Results.Subject.change_last()",
                        "На главную 🏠": "actions_f.StudentActions.set_default_directory(student)",
                        "Назад ↩": "actions_f.StudentActions.pop_directory(student)",
                        "Показать все": "actions_f.StudentActions.Results.Subject.get_all()",
                        "Посмотреть последний": "actions_f.StudentActions.Results.Subject.get_last()",
                        "Удалить последний": "actions_f.StudentActions.Results.Subject.drop_last()"
                    },
                    "add": {
                        "action": {
                            "any": "actions_f.StudentActions.Results.Subject.Add.adding()",
                            "default": "actions_f.StudentActions.Results.Subject.Add.get_max_score()",
                            "На главную 🏠": "actions_f.StudentActions.set_default_directory(student)",
                            "Назад ↩": "actions_f.StudentActions.pop_directory(student)"
                        },
                        "answer": {
                            "keyboard": [
                                [
                                    "blue",
                                    "На главную 🏠"
                                ],
                                [
                                    "blue",
                                    "Назад ↩"
                                ]
                            ],
                            "text": "Введите пробник в следующем формате: балл за каждое задание или критерий без пробелов, пробел, время выполнения\n\nПример: 4:20:00 (0:00:00, если время выполнения неизвестно)"
                        }
                    },
                    "answer": {
                        "keyboard": [
                            [
                                "red",
                                "Удалить последний"
                            ],
                            [
                                "white",
                                "Посмотреть последний"
                            ],
                            "add_line",
                            [
                                "white",
                                "Изменить последний"
                            ],
                            [
                                "white",
                                "Показать все"
                            ],
                            "add_line",
                            [
                                "green",
                                "Добавить"
                            ],
                            "add_line",
                            [
                                "blue",
                                "На главную 🏠"
                            ],
                            [
                                "blue",
                                "Назад ↩"
                            ]
                        ],
                        "text": "Выбранный предмет: "
                    },
                    "change": {
                        "action": {
                            "default": "answer = student.get_last_result(sub_name)",
                            "result": "error = student.add_result(user_directory[2], event.text)\nif error == -1\n\t:error_message = 'Слишком мало или слишком много символов в результате'\nelif error == -2:\n\terror_message = 'В результате присутствуют посторонние символы'\nelif error == -3:\n\terror_message = 'Есть балл за задание, превышающий возможный'\nelif error == -4:\n\terror_message = 'Неверный формат времени выполнения'\nelif error == -5:\n\terror_message = 'Некорректное время выполнения: в часах, минутах или секундах более двух цифр'\nelif error == -6:\n\terror_message = 'Во времени выполнения присутствуют посторонние символы'\nelif error == -7:\n\terror_message = 'Указанное значение минут или секунд больше 60 или указанное значение часов больше 24'\nelif error == -8:\n\terror_message = 'Неверный формат пробника(возможно присутствуют лишние пробелы)'\nelse:\n\tanswer = 'Пробник успешно изменен'\n\tuser_directory = user_directory[0:-1]",
                            "На главную 🏠": "actions_f.StudentActions.set_default_directory(student)",
                            "Назад ↩": "actions_f.StudentActions.pop_directory(student)"
                        },
                        "answer": {
                            "keyboard": [
                                [
                                    "blue",
                                    "На главную 🏠"
                                ],
                                [
                                    "blue",
                                    "Назад ↩"
                                ]
                            ],
                            "text": "Введите пробник в таком же формате, как и в 'Добавить'\n\nВаш прошлый пробник: "
                        }
                    },
                    "drop": {
                        "action": {
                            "default": "actions_f.StudentActions.Results.Subject.Drop.show_last()",
                            "Да": "actions_f.StudentActions.Results.Subject.Drop.agreed()",
                            "На главную 🏠": "actions_f.StudentActions.set_default_directory(student)",
                            "Назад ↩": "actions_f.StudentActions.pop_directory(student)",
                            "Нет": "actions_f.StudentActions.Results.Subject.Drop.disagreed()"
                        },
                        "answer": {
                            "keyboard": [
                                [
                                    "green",
                                    "Нет"
                                ],
                                [
                                    "red",
                                    "Да"
                                ],
                                "add_line",
                                [
                                    "blue",
                                    "На главную 🏠"
                                ],
                                [
                                    "blue",
                                    "Назад ↩"
                                ]
                            ],
                            "text": "Введите пробник в таком же формате, как и в 'Добавить'\n\nВаш прошлый пробник: "
                        }
                    },
                    "see": {
                        "action": {
                            "default": "actions_f.StudentActions.Results.Subject.See.see()",
                            "На главную 🏠": "actions_f.StudentActions.set_default_directory(student)",
                            "Назад ↩": "actions_f.StudentActions.pop_directory(student)"
                        },
                        "answer": {
                            "keyboard": [
                                [
                                    "blue",
                                    "На главную 🏠"
                                ],
                                [
                                    "blue",
                                    "Назад ↩"
                                ]
                            ],
                            "text": ""
                        }
                    },
                    "seeall": {
                        "action": {
                            "default": "actions_f.StudentActions.Results.Subject.SeeAll.see()",
                            "На главную 🏠": "actions_f.StudentActions.set_default_directory(student)",
                            "Назад ↩": "actions_f.StudentActions.pop_directory(student)"
                        },
                        "answer": {
                            "keyboard": [
                                [
                                    "blue",
                                    "На главную 🏠"
                                ],
                                [
                                    "blue",
                                    "Назад ↩"
                                ]
                            ],
                            "text": ""
                        }
                    }
                }
            }
        }
    }
}