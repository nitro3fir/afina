import vk_api
import main
from json import loads
import requests
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
import actions_f

COLOR_MAP = {"white": VkKeyboardColor.SECONDARY,
             "red": VkKeyboardColor.NEGATIVE,
             "green": VkKeyboardColor.POSITIVE,
             "blue": VkKeyboardColor.PRIMARY}

def auth():
    with open("run_config.json", "r") as readfile:
        config = loads(readfile.read())
        return vk_api.VkApi(token=config.get("vk_token")) #Авторизация

def text_proccessing(user, text):

    answer = None

    if user.get_role() == "student":
        student = main.Student(user)
        actions = actions_f.search_in_tree(actions_f.TREE["student"], user.get_directory())["action"]
        if "any" in actions.keys():
            answer = eval(actions["any"])
        elif text in actions.keys():
            answer = eval(actions[text])

    elif user.get_role() == "undifined":
        undifined = main.Undifined(user)
        if event.text == "Ученик😎":
            undifined.change_role("student")
        del undifined

    if not answer:
        answer = "..."
    
    return answer

def text_answering(user, answer, keyboard, vk, user_id):
    if user.get_role() == "student":
        student = main.Student(user)
        answers = actions_f.search_in_tree(actions_f.TREE["student"], user.get_directory())["answer"]
        for button in answers["keyboard"]:
            change_keyboard(keyboard, button)
        if answers["text"] != "" and answer == "...":
            answer = ""
        vk.messages.send(
                        user_id=user_id,
                        message=answer+answers["text"],
                        random_id=get_random_id(),
                        keyboard=keyboard.get_keyboard()
                        )
    elif user.get_role() == "undifined":
        change_keyboard(keyboard, ("Ученик😎", "green"))
        vk.messages.send(
                        user_id=user_id,
                        message="Войти как:",
                        random_id=get_random_id(),
                        keyboard=keyboard.get_keyboard()
                        )
        del student 
              
def dynamic_keyboard_buttons_add(user, keyboard):
    if user.get_role() == "student":
        student = main.Student(user)
        actions = actions_f.search_in_tree(actions_f.TREE["student"], user.get_directory())["action"]
        if "default" in actions.keys():
            eval(actions["default"])

def change_keyboard(keyboard, button, COLOR_MAP=COLOR_MAP):
    if button == "add_line":
        keyboard.add_line()
    else:
        keyboard.add_button(button[1], color=COLOR_MAP.get(button[0]))
        
#student_help = {"student":}
def main_loop():
    while True:
        try:
            vk_session = auth()
            longpoll = VkLongPoll(vk_session)
            vk = vk_session.get_api()
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                    user = main.User(event.user_id)
                    answer = text_proccessing(user, event.text)
                    keyboard = VkKeyboard(one_time=True)
                    dynamic_keyboard_buttons_add(user, keyboard)
                    text_answering(user, answer, keyboard, vk, event.user_id)

        except requests.exceptions.ReadTimeout:
            time.sleep(1)
        except requests.exceptions.ConnectionError:
            time.sleep(1)
        except Exception as e:
            keyboard = VkKeyboard()
            keyboard.add_button("На главную 🏠", color=VkKeyboardColor.PRIMARY)
            vk.messages.send(
                            user_id=event.user_id,
                            message="Отловлена неизвестная ошибка\nОтчет отправлен разработчикам",
                            random_id=get_random_id(),
                            keyboard=keyboard.get_keyboard()
                            )
            try:
                vk.messages.send(
                                user_id=73419670,
                                message=f"Роль:{user.get_role()}\nПользователь: {event.user_id}\nДиректория: {user.get_directory()}\nСообщение пользователя: {event.text}\nТекст ошибки: {e}",
                                random_id=get_random_id(),
                                keyboard=keyboard.get_keyboard()
                                )
            except Exception as e1:
                vk.messages.send(
                                user_id=73419670,
                                message=f"Не удалось получить данные о пользователе\nТекст основной ошибки: {e}\nТекст вторичной ошибки: {e1}",
                                random_id=get_random_id(),
                                keyboard=keyboard.get_keyboard()
                                )

if __name__ == "__main__":
    main_loop()
