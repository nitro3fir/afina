import json
from datetime import datetime, timedelta
import database_manipulator
from accessify import private
from accessify import protected

# TODO Поля наставника: Балл за ведущий предмет, Сумма балл место поступления, направление, платка/бюджет, возраст, курс, город, регион

DB_ROLES = {0:"creator", 1:"school_leader", 2:"group_leader", 3:"student", 4:"undifined"}
PROGRAM_ROLES = {"creator":0, "school_leader":1, "group_leader":2, "student":3, "undifined":4}

class User:
    def __init__(self, vk_id):
        user = database_manipulator.db.output("SELECT role, directory, db_id, region " \
                                              "FROM users " \
                                             f"WHERE vk_id = {vk_id}")
        if user:
            self.__vk_id = vk_id
            self.__role = DB_ROLES.get(user[0][0])
            self.__directory = user[0][1].split("/")
            self.__db_id = user[0][2]
            self.__region = user[0][3]
        else:
            self.__vk_id = vk_id
            self.__role = "undifined"
            self.__directory = "main"
            self.__db_id = 0
            self.__region = 0

    def get_directory(self):
        return self.__directory

    def get_role(self):
        return self.__role

    def get_vk_id(self):
        return self.__vk_id 

    def get_db_id(self):
        return self.__db_id

    def get_region(self):
        return self.__region

    def region_str_to_num(self, region_str):
        if len(region_str) > 50 or len(region_str) < 3:
            return -1
        with open("regions::str_to_num.json", "r") as readfile:
            data = json.loads(readfile.read())
        region_str = region_str.lower().split()
        if "республика" in region_str:
            subject = "республика"
            region_str = "".join(list(set(region_str) - set(["республика"])))
        elif "область" in region_str:
            subject = "область"
            region_str = "".join(list(set(region_str) - set(["область"])))
        elif "край" in region_str:
            subject = "край"
            region_str = "".join(list(set(region_str) - set(["край"])))
        elif "округ" in region_str:
            subject = "округ"
            region_str = "".join(list(set(region_str) - set(["округ", "автономный"])))
        else:
            subject = "другое"
            region_str = "".join(region_str)
        finded = False
        
        if len(region_str) == 0:
            return -2

        if subject != "другое":
            while region_str != region_str[0]:
                region_str = region_str[0:-1]
                for region_st in data[subject]:
                    if region_st.find(region_str) != -1 and not finded:
                        finded = True
                        finded_region_num = data[subject][region_st]
                if finded:
                    break
        else:
            while region_str != region_str[0]:
                region_str = region_str[0:-1]
                for sub in data:
                    for region_st in data[sub]:
                        if region_st.find(region_str) != -1 and not finded:
                            finded = True
                            finded_region_num = data[sub][region_st]
                if finded:
                    break
        if finded:
            return finded_region_num
        else:
            return -2

    def region_num_to_str(self, region_num):
        with open("regions::num_to_str.json", "r") as readfile:
            data = json.loads(readfile.read())
        return data.get(region_num)

    def append_directory(self, update):
        self.__directory.append(update)

    def pop_directory(self):
        self.__directory.pop()

    def set_default_directory(self):
        self.__directory = ['main']

    def change_region(self, region):
        self.__region = int(region)

    def __del__(self):
        self.__directory = "/".join(self.__directory)
        database_manipulator.db.input("UPDATE users " \
                                     f"SET role = {PROGRAM_ROLES.get(self.__role)}, directory = '{self.__directory}', db_id = {self.__db_id}, region = {self.__region} " \
                                     f"WHERE vk_id = {self.__vk_id}")

class Undifined(User): #_User__role
    def __init__(self, user):
        self._User__vk_id = user.get_vk_id()
        self._User__role = "undifined"
        self._User__directory = "main"
        self._User__db_id = 0
        self._User__region = user.get_region()

    def change_role(self, role):
        self._User__role = role

    def __del__(self):
        PROGRAM_ROLES = {"creator":0, "school_leader":1, "group_leader":2, "student":3, "undifined":4}
        if self._User__role == "undifined":
            database_manipulator.db.input("INSERT INTO users (vk_id, role, directory, db_id, region) " \
                                         f"VALUES ({self._User__vk_id}, {PROGRAM_ROLES.get(self._User__role)}, 'main', 0, 0)" )
        else:
            if self._User__role == "student":
                database_manipulator.db.input("INSERT INTO students (subjects)" \
                                             f"VALUES (NULL)")
                self._User__db_id = database_manipulator.db.output("SELECT MAX(id) FROM students")[0][0]
            super().__del__()

class Student(User):
    #Сделать функцию статистики по всем предметам суммарно
    def __init__(self, user):
        self._User__vk_id = user.get_vk_id()
        self._User__role = "student"
        self._User__directory = user.get_directory()
        self._User__db_id = user.get_db_id()
        self._User__region = user.get_region()
        self._Student__subjects = database_manipulator.db.output(f"SELECT subjects FROM students WHERE id = {self._User__db_id}")[0][0]
        if not self._Student__subjects:
            self._Student__subjects = []

    def add_subject(subject):
        if subject not in self._Student__subjects:
            self._Student__subjects.append(subject)

    def drop_subject(subject):
        if subject in self._Student__subjects:
            self._Student__subjects.remove(subject)

    def get_max_score(subject):
        with open("subjects::short_to_max_score.json", "r") as readfile:
            data = json.loads(readfile.read())
        return data.get(subject)

    def get_subjects(self):
        return self._Student__subjects

    def add_result(self, subject, result_and_exam_duration):
        if len(result_and_exam_duration.split()) != 2:
            return -8
        result = result_and_exam_duration.split()[0]
        exam_duration = result_and_exam_duration.split()[1]
        digits = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
        with open("subjects::short_to_max_score.json", "r") as readfile:
            data = json.loads(readfile.read())

        if len(result) != len(data.get(subject)): #Проверка длины входного результата
            return -1

        for char in result: #Проверка результата на отсутствие посторонних символов
            if char not in digits:
                return -2

        for index, char in enumerate(result): #Проверка цифр результата на корректность для конкретного предмета
            if int(char) > int(data.get(subject)[index]):
                return -3

        exam_duration = exam_duration.split(":") 
        if len(exam_duration) != 3: #Неверный формат времени
            return -4

        if len(exam_duration[0]) > 2 or len(exam_duration[1]) > 2 or len(exam_duration[2]) > 2: #Проверка на количество цифр между двоеточиями
            return -5

        for time in exam_duration: #Проверка времени на отсутствие посторонних символов
            for char in time:
                if char not in digits:
                    return -6

        if int(exam_duration[1][0]) > 5 or int(exam_duration[2][0]) > 5 or int(exam_duration[0]) > 23: #Проверка секунд и минут на то, чтобы они были менее 60
            return -7
        
        exam_duration = ":".join(exam_duration)
        database_manipulator.db.input(f"INSERT INTO results_{subject} (datetime, student_id, result, duration) " \
                                      f"VALUES ('{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}', {self._User__db_id}, '{result}', '{exam_duration}')") #Отбрасывает миллисекунды от нынешнего времени 

    def get_last_result(self, subject):
        result = database_manipulator.db.output(f"SELECT datetime, result, duration FROM results_{subject} " \
                                                f"WHERE student_id = {self._User__db_id} " \
                                                f"ORDER BY datetime DESC " \
                                                f"LIMIT 1")
        if not result:
            return -1
        else:
            result = result[0]
        with open("regions::num_to_dtime.json", "r") as readfile:
            data = json.loads(readfile.read())
        dtime = int(data.get(str(self._User__region)))
        result_time = result[0] + timedelta(hours=dtime)
        date, time = str(result_time).split()
        date_temp = date.split('-')
        date_temp.reverse()
        date = '.'.join(date_temp)
        time = time[0:-3]
        with open("subjects::primary_to_secondary.json", "r") as readfile:
            data = json.loads(readfile.read())
        primary = sum(map(int, result[1]))
        return f"{date} {time}: {result[1]} {result[2]}\nВторичные {data[subject][primary]}\nПервичные {primary}"

    def change_last_result(self, subject, result_and_exam_duration):
        #Сделать проверку результата и времени выполнения 
        #with open("subjects.json", "r") as readfile:
        #   data = json.loads(readfile.read())
        if len(result_and_exam_duration.split()) != 2:
            return -8
        result = result_and_exam_duration.split()[0]
        exam_duration = result_and_exam_duration.split()[1]
        digits = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
        with open("subjects::short_to_max_score.json", "r") as readfile:
            data = json.loads(readfile.read())

        if len(result) != len(data.get(subject)): #Проверка длины входного результата
            return -1

        for char in result: #Проверка результата на отсутствие посторонних символов
            if char not in digits:
                return -2

        for index, char in enumerate(result): #Проверка цифр результата на корректность для конкретного предмета
            if int(char) > int(data.get(subject)[index]):
                return -3

        exam_duration = exam_duration.split(":") 
        if len(exam_duration) != 3: #Неверный формат времени
            return -4

        if len(exam_duration[0]) > 2 or len(exam_duration[1]) > 2 or len(exam_duration[2]) > 2: #Проверка на количество цифр между двоеточиями
            return -5

        for time in exam_duration: #Проверка времени на отсутствие посторонних символов
            for char in time:
                if char not in digits:
                    return -6

        if int(exam_duration[1][0]) > 5 or int(exam_duration[2][0]) > 5 or int(exam_duration[0]) > 23: #Проверка секунд и минут на то, чтобы они были менее 60
            return -7
        
        exam_duration = ":".join(exam_duration)
        database_manipulator.db.input(f"UPDATE results_{subject} SET result = '{result}', duration = '{exam_duration}' "
                                      f"WHERE student_id = {self._User__db_id} AND datetime = "
                                      f"(SELECT datetime FROM results_{subject} WHERE student_id = {self._User__db_id} ORDER BY datetime DESC LIMIT 1)")

    def drop_last_result(self, subject):
        database_manipulator.db.input(f"DELETE FROM results_{subject} " \
                                      f"WHERE student_id = {self._User__db_id} AND datetime = " \
                                      f"(SELECT datetime FROM results_{subject} WHERE student_id = {self._User__db_id} ORDER BY datetime DESC LIMIT 1)")
        
    def get_profile(self):
        with open("regions::num_to_str.json", "r") as readfile:
            data = json.loads(readfile.read())
        region_str = "-"
        if self._User__region != 0:
            region_str = data.get(str(self._User__region))
        with open("subjects::short_to_full.json", "r") as readfile:
            data = json.loads(readfile.read())
        subjects = ""
        for subject_short_name in self._Student__subjects:
            subjects += data.get(subject_short_name) + ", "
        if subjects == "":
            subjects = "-"
        else:
            subjects = subjects[0:len(subjects)-2]
        return f"Страница: https://vk.com/id{self._User__vk_id}\n" \
                "Роль: Ученик\n" \
               f"Регион: {region_str}\n" \
               f"Предметы: {subjects}"

    def get_all_results(self, subject):
        #Добавить разницу по времени + оформить в строку
        results = database_manipulator.db.output(f"SELECT datetime, result, duration FROM results_{subject} " \
                                              f"WHERE student_id = {self._User__db_id} " \
                                              f"ORDER BY datetime DESC")
        if not results:
            return -1
        with open("regions::num_to_dtime.json", "r") as readfile:
            data = json.loads(readfile.read())
        dtime = int(data.get(str(self._User__region)))
        results_str = ""
        with open("subjects::primary_to_secondary.json", "r") as readfile:
            data = json.loads(readfile.read())
        for result in results:
            result_time = result[0] + timedelta(hours=dtime)
            date = str(result_time).split()[0]
            date_temp = date.split('-')
            date_temp.reverse()
            date = '.'.join(date_temp)
            primary = sum(map(int, result[1]))
            results_str += f"{date}: {data[subject][primary]}(в), {primary}(п)\n"
        return results_str[0:-1]

    def subject_short_name_to_full(self, shortname):
        with open("subjects::short_to_full.json", "r") as readfile:
            data = json.loads(readfile.read())
        return data.get(shortname)

    def __del__(self):
        if self._Student__subjects:
            subjects_db_formated = "{" + ", ".join(['"' + subject + '"' for subject in self._Student__subjects]) + "}"
            database_manipulator.db.input(f"UPDATE students SET subjects = '{subjects_db_formated}'")
        super().__del__()

    # Добавить функцию редактирования и удаления профиля
    """
    def get_lead_information(self):
        information = database_manipulator.db.output("SELECT first_name, last_name, vk_id, exam_score, score_average, " \
                                                     "university, education_locality, faculty_num, year_of_admission, graduation_year, " \
                                                     "budget_form, birth_day, native_locality, native_region "
                                                     "FROM groups_leaders " \
                                                     "WHERE leader_id = (" \
                                                     "SELECT groups_leaders.leader_id " \
                                                     "FROM students AS s " \
                                                     "JOIN students_groups AS sg ON s.student_id = sg.student_id " \
                                                     "JOIN groups AS g ON sg.group_id = g.group_id " \
                                                     "JOIN groups_leaders AS gl ON g.leader_id = gl.leader_id " \
                                                    f"WHERE s.student_id = {self.id})")[0]
        print(f"Наставник: {information[0]} {information[1]}\n" \
              f"Страница ВК: @{information[2]}\n" \
              f"Балл за преподаваемый предмет | Среднее арифм. по баллам поступления: {information[3]} | {information[4]}\n" \
              f"ВУЗ: {information[5]}, {information[6]}\n" \
              f"Факультет: {information[7]}, {information[8]}-{information[9]}, {information[10]}\n" \
              f"День рождения: {information[11]}\n" \
              f"Родной город: {information[12]}, {information[13]}\n") #Изменить отображение бюджета, день рождения(на возраст), специальность, региона
    
class School:
    def __init__(self, vk_id):
        self.id, self.vk_id = database_manipulator.db.output("SELECT id, vk_id "\
                                                            "FROM school_leaders "\
                                                            f"WHERE vk_id = '{vk_id}'")[0]
    def get_groups_list(self):
        groups = database_manipulator.db.output("SELECT g.name "\
                                            "FROM school_leaders AS sl "\
                                            "JOIN schools AS s ON s.id = sl.school_id "\
                                            "JOIN groups AS g ON s.id = g.school_id "\
                                            f"WHERE sl.vk_id = '{self.vk_id}'")[0]
        line = ""
        for num, group_name in enumerate(groups):
            line += f"{num+1}. {group_name}\n"
        return line
"""
"""
class Group:
    Абстрактный класс 'Группа', который регулирует работу с базой 
    Атрибуты: 
        data - Dict(str : Dict(str : str))

    def __init__(self, filename: str):
        with open(f"{filename}.json", "r") as readfile:
            self.data = json.loads(readfile.read())

    def add_result(self, username: str, result: str):
        if username not in self.data.keys():  # если это новый пользователь, то на нем создается словарь
            self.data[username] = dict()
        utc_now: datetime = datetime.utcnow()  # В базу данных ложится формат UTC
        to_base_time: datetime = datetime(utc_now.year, utc_now.month, utc_now.day, utc_now.hour, utc_now.minute, utc_now.second)
        self.data[username][str(to_base_time)] = result

    def save_file(self, filename: str):
        with open(f"{filename}.json", "w") as readfile:
            json.dump(self.data, readfile, indent=4, ensure_ascii=False, sort_keys=True)

    def remove_user(self, username: str):
        del self.data[username]

    def remove_result(self, username: str, start_date: str, end_date: str):
        for base_date in [agreed_date for agreed_date in self.data[username] 
        if self.string_to_datetime(start_date) < self.string_to_datetime(agreed_date) < self.string_to_datetime(end_date)]:
            del self.data[username][base_date]

    def display_group(self):
        for username in self.data:
            print("Ученик: ", username)
            for date in self.data[username]:
                print(date, ":", self.data[username][date], self.get_primary_score(self.data[username][date]))

    def display_user(self, username: str):
        print("Ученик: ", username)
        for base_date in self.data[username]:
            print(base_date, ":", self.data[username][base_date], self.get_primary_score(self.data[username][base_date]))

    def display_by_date(self, start_date: str, end_date: str):
        for username in self.data:
            print("Ученик: ", username)
            for base_date in self.data[username]:
                if self.string_to_datetime(start_date) < self.string_to_datetime(base_date) < self.string_to_datetime(end_date):
                    print(base_date, ":", self.data[username][base_date], self.get_primary_score(self.data[username][date]))

    def display_user_by_date(self, username: str, start_date: str, end_date: str):
        print("Ученик: ", username)
        for base_date in self.data[username]:
            if self.string_to_datetime(start_date) < self.string_to_datetime(base_date) < self.string_to_datetime(end_date):
                print(base_date, ": ", self.data[username][base_date], self.get_primary_score(self.data[username][base_date]))

    def string_to_datetime(self, stringdate: str) -> datetime:
        parsed = list(map(int, (' '.join((' '.join(stringdate.split('-'))).split(':'))).split(' '))) #Превращает дату в лист чисел
        return datetime(parsed[0], parsed[1], parsed[2], parsed[3], parsed[4], parsed[5])

    def get_primary_score(self, results: str) -> int:
        return sum(list(map(int, list(results))))

    def get_primary_average_stat(self, username: str, start_date: str, end_date: str) -> List[Tuple[str, float, int]]:
        agreed_dates: List[str] = [agreed_date for agreed_date in self.data[username] 
            if self.string_to_datetime(start_date) < self.string_to_datetime(agreed_date) < self.string_to_datetime(end_date)]
        stats: List[Tuple[str, float, int]] = list()
        for i in range(len(agreed_dates)):
            stats.append((agreed_dates[i], round(sum(map(self.get_primary_score, list(map(self.data[username].get, 
                agreed_dates[0:i+1]))))/(i+1), 2), self.get_primary_score(self.data[username][agreed_dates[i]])))
        return stats

    def get_mistakes(self, username: str, start_date: str, end_date: str) -> List[float]:
        most_mistakes = []
        list_with_results = []
        for base_date in self.data[username]:
            if self.string_to_datetime(start_date) < self.string_to_datetime(base_date) < self.string_to_datetime(end_date):
                list_with_results.append(tuple(map(int, list(self.data[username][base_date]))))
        for zadanie in zip(*list_with_results):
            most_mistakes.append(sum(zadanie))
        most_mistakes.append(len(list_with_results))
        return most_mistakes



    @abstractmethod
    def get_secondary_stat():
        pass

class BioGroupEGE(Group):

    def __init__(self, filename: str):
        self.primary_to_secondary = {0: 0, 1: 3, 2: 5, 3: 7, 4: 9, 5: 12, 6: 14,
                                     7: 16, 8: 18, 9: 21, 10: 23, 11: 25, 12: 27, 
                                     13: 30, 14: 32, 15: 34, 16: 36, 17: 38, 18: 39, 
                                     19: 40, 20: 42, 21: 43, 22: 44, 23: 46, 24: 47, 
                                     25: 48, 26: 50, 27: 51, 28: 52, 29: 53, 30: 55, 
                                     31: 56, 32: 57, 33: 59, 34: 60, 35: 61, 36: 63, 
                                     37: 64, 38: 65, 39: 66, 40: 68, 41: 69, 42: 70, 
                                     43: 72, 44: 73, 45: 74, 46: 76, 47: 77, 48: 78, 
                                     49: 79, 50: 82, 51: 84, 52: 86, 53: 89, 54: 91, 
                                     55: 93, 56: 96, 57: 98, 58: 100}
        self.groups = {"Общая биология": (1, 2, 19, 20, 21, 22, 23, 24, 25),
                       "Анатомия": (12, 13, 14),
                       "Цитология": (4, 5, 27),
                       "Генетика": (3, 6, 28),
                       "Селекция": (7, 8),
                       "Многообразие организмов": (9, 10, 11),
                       "Эволюция": (15, 16),
                       "Экосистемы": (17, 18)}
        self.max_score = (1, 1, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3)
        super().__init__(filename) # Конструктор базового класса

    def get_secondary_score(self, results: str) -> int:
        return self.primary_to_secondary.get(self.get_primary_score(results))

    def get_secondary_average_stat(self, username: str, start_date: str, end_date: str) -> List[Tuple[str, float, int]]:
        agreed_dates: List[str] = [agreed_date for agreed_date in self.data[username] 
            if self.string_to_datetime(start_date) < self.string_to_datetime(agreed_date) < self.string_to_datetime(end_date)]
        stats: List[Tuple[str, float, int]] = list()
        for i in range(len(agreed_dates)):
            stats.append((agreed_dates[i], round(sum(map(self.get_secondary_score, list(map(self.data[username].get, 
                agreed_dates[0:i+1]))))/(i+1), 2), self.get_secondary_score(self.data[username][agreed_dates[i]])))
        return stats

    def group_mistakes(self, username: str, start_date: str, end_date: str) -> DefaultDict[str, Tuple[int]]:
        group_mistakes = dict()
        mistakes = self.get_mistakes(username, start_date, end_date)
        for group in self.groups:
            group_mistakes[group] = list()
            for zadanie in self.groups[group]:
                group_mistakes[group].append(round(mistakes[zadanie-1]*100/(self.max_score[zadanie-1]*mistakes[-1])))
        return group_mistakes

    def group_mistakes_averages(self, username: str, start_date: str, end_date: str) -> DefaultDict[str, int]:
        group_mistakes = self.group_mistakes(username, start_date, end_date)
        for group in group_mistakes:
            group_mistakes[group] = round(sum(group_mistakes[group])/len(group_mistakes[group]))
        return group_mistakes

    def mistakes(self, username: str, start_date: str, end_date: str) -> List[int]:
        mistakes = self.get_mistakes(username, start_date, end_date)
        for zadanie_ind in range(len(mistakes)-1):
            mistakes[zadanie_ind] = round(mistakes[zadanie_ind]*100/(self.max_score[zadanie_ind]*mistakes[-1]))
        return mistakes[:-1]

    def mistakes_sorted(self, username: str, start_date: str, end_date: str) -> List[Tuple[int, int]]:
        pairs = []
        mistakes = self.mistakes(username, start_date, end_date)
        while mistakes != []:
            pairs.append((mistakes.index(min(mistakes))+1, min(mistakes)))
            del mistakes[mistakes.index(min(mistakes))]
        return pairs

class MathGroupEGE(Group):
    Производный класс от 'Группы', который заточен под математику

    def __init__(self, filename: str):
        self.primary_to_secondary = {0: 0, 1: 5, 2: 9, 3: 14, 4: 18, 5: 23, 6: 27, 7: 33, 8: 39, 9: 45, 10: 50, 11: 56,
                                12: 62, 13: 68, 14: 70, 15: 72, 16: 74, 17: 76, 18: 78, 19: 80, 20: 82, 21: 84, 22: 86,
                                23: 88, 24: 90, 25: 92, 26: 94, 27: 96, 28: 98, 29: 99, 30: 100, 31: 100, 32: 100}
        super().__init__(filename) # Конструктор базового класса


    def get_secondary_score(self, username: str, date: str) -> int:
        return self.primary_to_secondary.get(self.get_primary_score(username, date))
"""

def main():
    ch = "2+2"
    while ch != "q":
        eval(ch)
        ch = input('Enter the command(enter "q" to quit): ')


if __name__ == "__main__":
    main()
