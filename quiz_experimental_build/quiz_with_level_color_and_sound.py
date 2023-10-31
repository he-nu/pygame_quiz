import json
import time
import random

import pygame as pg

import sound_effects as se

pg.init()



SCREEN_SIZE = (800, 800)
FONT_16 = pg.font.Font("PressStart2P-Regular.ttf", 16)
FONT_32 = pg.font.Font("PressStart2P-Regular.ttf", 32)
FONT_48 = pg.font.Font("PressStart2P-Regular.ttf", 48)

Q_PATH = open("questions.json", "r")
QUESTIONS = json.load(Q_PATH)


WRONG_LIMIT = 1


def get_next_question():
    """
        Generator function that yields the next question
        The questions are stored in constant QUESTIONS
        Output:
            - question: str
            - answerOptions: dict
            - correctAnswer: str
    """
    for level in QUESTIONS:
        for question in QUESTIONS[level]:
            yield (QUESTIONS[level][question]["question"], QUESTIONS[level][question]["answerOptions"], QUESTIONS[level][question]["correctAnswer"])


def shuffle_answers(current_question: tuple) -> tuple:
    """ Takes the current question and shuffles 
    the order of the answers.

    Input: Current answer from get next question tuple
    output: Answers shuffled: tuple
    """
    answer_structure: dict = current_question[1]
    correct_answer = current_question[-1]
    correct_value = answer_structure[correct_answer]
    possible_answers = [i for i in answer_structure.values()]
    shuffled_answers = possible_answers.copy()
    random.shuffle(shuffled_answers)
    # print(shuffled_answers)
    answer_keys = ['A', 'B', 'C']
    shuffled_answers_dict = {}
    for i, k in enumerate(answer_keys):
        shuffled_answers_dict[k] = shuffled_answers[i]
    key_list = list(shuffled_answers_dict.keys())
    val_list = list(shuffled_answers_dict.values())
    position = val_list.index(correct_value)
    new_correct = key_list[position]
    return current_question[0], shuffled_answers_dict, new_correct

def music_dj():
    songs = ["sounds/pokemon.mp3", "sounds/huoratron.mp3"]
    for song in songs:
        if song == "sounds/huoratron.mp3":
            pg.mixer.music.set_volume(1)
        yield song

def set_level(current_level, current_score):
    level = current_level

    if current_score == 8:
        level = 2
    elif current_score == 15:
        level = 3

    if level > current_level:
        se.level_up_sound.play()
        time.sleep(2)

    return level


def wrap(a_string, limit):
    output = []
    sentence = ""

    for word in a_string.split():
        if len(sentence) + len(word) > limit:
            output.append(sentence)
            sentence = ""
        sentence += word + " "

    output.append(sentence)

    # pad to make all equal length, smaller will be padded equally from both sides
    max_len = max([len(line) for line in output])
    for i in range(len(output)):
        if len(output[i]) < max_len:
            output[i] = output[i].center(max_len)
    return output


class Area:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pg.Rect(x, y, width, height)
        self.text = None
        self.font = FONT_16
        self.width = width
        self.height = height

    def set_font(self, font):
        self.font = font

    def set_text(self, text: str):
        self.text = text

    def set_border(self, width: int, color: tuple):
        self.border = width
        self.border_color = color

    def set_color_inside(self, color: tuple):
        self.color = color

    def set_color_border(self, color: tuple):
        self.border_color = color

    def set_pos(self, x: int, y: int):
        self.rect.x = x
        self.rect.y = y
        (self.rect.x + 10, self.rect.y + 10)

    def draw(self, screen):
        text = self.text
        pg.draw.rect(screen, self.color, self.rect)
        pg.draw.rect(screen, self.border_color, self.rect, 1)
        if text:
            text_surface = self.font.render(text, True, self.border_color)
            text_rect = text_surface.get_rect()
            text_rect.center = self.rect.center
            screen.blit(text_surface, text_rect)


class Button(Area):
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self.text_color = (0, 0, 0)
        self.color = (0, 0, 0)
        self.border_color = (0, 0, 0)

    def was_pressed(self, mouse_pos: tuple):
        if self.rect.collidepoint(mouse_pos):
            se.button_sound.play()
            return True
        return False

    def set_text_color(self, color: tuple):
        self.text_color = color

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)
        pg.draw.rect(screen, self.border_color, self.rect, 1)
        if self.text:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect()
            text_rect.center = self.rect.center
            screen.blit(text_surface, text_rect)


class Text(Area):
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self.clear_text()
        self.lines = None
        self.line_height = None
        self.text_pos = None
        self.font = FONT_16

    def clear_text(self):
        self.lines = None
        self.line_height = None
        self.text_pos = None

    def set_text(self, lines: list['str'], line_height: int):
        self.lines = lines
        self.line_height = line_height

    def set_one_line_text(self, text: str):
        if self.lines:
            self.lines = [text]
        self.text = text

    def _multi_line_draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)
        pg.draw.rect(screen, self.border_color, self.rect, 1)
        if self.lines:
            for i, line in enumerate(self.lines):
                text_surface = self.font.render(line, True, self.border_color)
                text_rect = text_surface.get_rect()
                text_rect.x = self.text_pos[0]
                text_rect.y = self.text_pos[1] + i * self.line_height
                screen.blit(text_surface, text_rect)

    def draw(self, screen):
        if self.lines:
            self._multi_line_draw(screen)
        else:
            super().draw(screen)

    def set_pos(self, x: int, y: int):
        self.rect.x = x
        self.rect.y = y
        self.text_pos = (self.rect.x, self.rect.y)

    def set_text_pos(self, x: int, y: int):
        self.text_pos = (self.rect.x + x, self.rect.y + y)


def intro(screen):
    pass


def options(screen):
    while True:
        global WRONG_LIMIT
        text_area = Text(0, 0, 700, 250)
        text_area.set_font(FONT_48)
        text_area.set_color_inside((0, 0, 0))
        text_area.set_border(30, (57, 255, 20))
        text_area.set_pos(SCREEN_SIZE[0] / 2 - 350, SCREEN_SIZE[1] / 2 - 375)
        text_area.set_text(["Options"], 60)
        text_area.set_text_pos(200, 85)

        max_wrong_answers = Text(0, 0, 700, 250)
        max_wrong_answers.set_color_inside((0, 0, 0))
        max_wrong_answers.set_border(30, (57, 255, 20))
        max_wrong_answers.set_pos(
            SCREEN_SIZE[0] / 2 - 350, SCREEN_SIZE[1] / 2 - 75)
        max_wrong_answers.set_text(
            [f"Max wrong answers: (Current setting: {WRONG_LIMIT})"], 60)
        max_wrong_answers.set_text_pos(35, 65)

        one_wrong = Button(0, 0, 100, 50)
        one_wrong.set_color_inside((0, 100, 0))
        one_wrong.set_border(30, (57, 255, 20))
        one_wrong.set_text("1")
        one_wrong.set_pos(SCREEN_SIZE[0] / 2 - 150, SCREEN_SIZE[1] / 2 + 60)

        two_wrong = Button(0, 0, 100, 50)
        two_wrong.set_color_inside((0, 100, 0))
        two_wrong.set_border(30, (57, 255, 20))
        two_wrong.set_text("2")
        two_wrong.set_pos(SCREEN_SIZE[0] / 2 + 50, SCREEN_SIZE[1] / 2 + 60)

        exit_button = Button(0, 0, 200, 100)
        exit_button.set_color_inside((0, 100, 0))
        exit_button.set_border(30, (57, 255, 20))
        exit_button.set_text("Exit")
        exit_button.set_pos(SCREEN_SIZE[0] / 2 - 100, SCREEN_SIZE[1] / 2 + 250)
        text_area.draw(screen)
        max_wrong_answers.draw(screen)
        one_wrong.draw(screen)
        two_wrong.draw(screen)
        exit_button.draw(screen)

        pg.display.flip()

        if pg.event.get(pg.QUIT):
            pg.quit()
            exit()
        if pg.event.get(pg.MOUSEBUTTONDOWN):
            mouse_pos = pg.mouse.get_pos()
            if one_wrong.was_pressed(mouse_pos):
                WRONG_LIMIT = 1
                max_wrong_answers.set_text(
                    [f"Max wrong answers: (Current setting: {WRONG_LIMIT})"], 60
                )
                max_wrong_answers.draw(screen)
                one_wrong.set_color_inside((0, 255, 0))
                one_wrong.draw(screen)
                pg.display.flip()
                pg.time.delay(350)

            if two_wrong.was_pressed(mouse_pos):
                WRONG_LIMIT = 2
                max_wrong_answers.set_text(
                    [f"Max wrong answers: (Current setting: {WRONG_LIMIT})"], 60
                )
                max_wrong_answers.draw(screen)
                max_wrong_answers.draw(screen)
                two_wrong.set_color_inside((0, 255, 0))
                two_wrong.draw(screen)
                pg.display.flip()
                pg.time.delay(350)

            if exit_button.was_pressed(mouse_pos):
                exit_button.set_color_inside((0, 255, 0))
                exit_button.draw(screen)
                pg.display.flip()
                pg.time.delay(250)
                break


def menu(screen):
    start_button = Button(0, 0, 200, 100)
    start_button.set_color_inside((0, 100, 0))
    start_button.set_border(30, (57, 255, 20))
    start_button.set_text("Start")
    start_button.set_pos(SCREEN_SIZE[0] / 2 - 100, SCREEN_SIZE[1] / 2 - 250)

    options_button = Button(0, 0, 200, 100)
    options_button.set_color_inside((0, 100, 0))
    options_button.set_border(30, (57, 255, 20))
    options_button.set_text("Options")
    options_button.set_pos(SCREEN_SIZE[0] / 2 - 100, SCREEN_SIZE[1] / 2 - 50)

    quit_button = Button(0, 0, 200, 100)
    quit_button.set_color_inside((0, 100, 0))
    quit_button.set_border(30, (57, 255, 20))
    quit_button.set_text("Quit")
    quit_button.set_pos(SCREEN_SIZE[0] / 2 - 100, SCREEN_SIZE[1] / 2 + 150)

    start_button.draw(screen)
    quit_button.draw(screen)
    options_button.draw(screen)
    pg.display.flip()
    while True:
        if pg.event.get(pg.QUIT):
            se.button_sound.play()
            time.sleep(1)
            pg.quit()
            exit()
        if pg.event.get(pg.MOUSEBUTTONDOWN):
            mouse_pos = pg.mouse.get_pos()
            if start_button.was_pressed(mouse_pos):
                start_button.set_color_inside((0, 255, 0))
                start_button.draw(screen)
                pg.display.flip()
                pg.time.delay(250)
                game(screen)
            if quit_button.was_pressed(mouse_pos):
                pg.mixer.music.pause()
                quit_button.set_color_inside((0, 255, 0))
                quit_button.draw(screen)
                pg.display.flip()
                pg.time.delay(250)
                time.sleep(1)
                pg.quit()
                exit()

            if options_button.was_pressed(mouse_pos):
                options_button.draw(screen)
                pg.display.flip()
                pg.time.delay(250)
                screen = pg.display.set_mode(SCREEN_SIZE)
                options(screen)
                screen = pg.display.set_mode(SCREEN_SIZE)
                menu(screen)


def initialize_buttons():
    neon_green = (57, 255, 20)
    dark_green = (0, 100, 0)

    left_button = Button(0, 0, 200, 100)
    middle_button = Button(0, 0, 200, 100)
    right_button = Button(0, 0, 200, 100)

    left_button.set_color_inside(dark_green)
    middle_button.set_color_inside(dark_green)
    right_button.set_color_inside(dark_green)

    left_button.set_border(30, neon_green)
    middle_button.set_border(30, neon_green)
    right_button.set_border(30, neon_green)

    left_button.set_text("A")
    middle_button.set_text("B")
    right_button.set_text("C")

    left_button.set_pos(SCREEN_SIZE[0] / 3 - 220,
                        SCREEN_SIZE[0] - SCREEN_SIZE[1] / 3 + 100)
    middle_button.set_pos(
        SCREEN_SIZE[0] / 2 - 100, SCREEN_SIZE[0] - SCREEN_SIZE[1] / 3 + 100)
    right_button.set_pos(SCREEN_SIZE[0] - (SCREEN_SIZE[0] / 3) + 20,
                         SCREEN_SIZE[0] - SCREEN_SIZE[1] / 3 + 100)

    return left_button, middle_button, right_button


def initialize_text_areas():
    black = (0, 0, 0)
    neon_green = (57, 255, 20)

    question_text_area = Text(0, 0, 700, 250)
    question_text_area.set_font(FONT_32)
    question_text_area.set_color_inside(black)
    question_text_area.set_border(30, neon_green)
    question_text_area.set_pos(
        SCREEN_SIZE[0] / 2 - 350, SCREEN_SIZE[1] / 2 - 320)
    question_text_area.set_text_pos(35, 50)

    question_option_area = Text(0, 0, 700, 250)
    question_option_area.set_color_inside(black)
    question_option_area.set_border(30, neon_green)
    question_option_area.set_pos(
        SCREEN_SIZE[0] / 2 - 350, SCREEN_SIZE[1] / 2 - 45)
    question_option_area.set_text_pos(75, 65)

    question_number_text = Text(SCREEN_SIZE[0] - 200, 20, 200, 50)
    question_number_text.set_font(FONT_16)
    question_number_text.set_color_inside(black)
    question_number_text.set_border(30, neon_green)
    question_number_text.set_pos(50, 15)

    correct_answers_text = Text(SCREEN_SIZE[0] - 200, 140, 350, 50)
    correct_answers_text.set_font(FONT_16)
    correct_answers_text.set_color_inside(black)
    correct_answers_text.set_border(0, neon_green)
    correct_answers_text.set_pos(400, 15)

    return question_text_area, question_option_area, question_number_text, correct_answers_text


def initialize_game(screen):
    screen.fill((0, 0, 0))
    wrong_answers = 0
    lives = WRONG_LIMIT
    right_answers = 0
    current_question = 0
    level = 1

    left_button, middle_button, right_button = initialize_buttons()
    question_text_area, question_option_area, question_number_text, correct_answers_text = initialize_text_areas()

    questions_generator = get_next_question()

    objects = {"left_button": left_button, "middle_button": middle_button, "right_button": right_button, "question_text_area": question_text_area,
               "question_option_area": question_option_area, "question_number_text": question_number_text, "correct_answers_text": correct_answers_text}

    return screen, wrong_answers, lives, right_answers, current_question, level, left_button, middle_button, right_button, question_text_area, question_option_area, question_number_text, correct_answers_text, questions_generator, objects


def set_colors_for_level(level, objects):
    neon_green = (57, 255, 20)
    dark_green = (0, 100, 0)
    neon_orange = (255, 165, 0)
    dark_orange = (100, 50, 0)
    neon_red = (255, 0, 0)
    dark_red = (100, 0, 0)
    if level == 1:
        set_button_colors(dark_green, neon_green, objects)
    elif level == 2:
        set_button_colors(dark_orange, neon_orange, objects)
    elif level == 3:
        set_button_colors(dark_red, neon_red, objects)


def set_button_colors(dark_inside, neon_border, objects):
    left_button = objects["left_button"]
    middle_button = objects["middle_button"]
    right_button = objects["right_button"]
    question_text_area = objects["question_text_area"]
    question_option_area = objects["question_option_area"]
    question_number_text = objects["question_number_text"]
    correct_answers_text = objects["correct_answers_text"]

    left_button.set_color_inside(dark_inside)
    middle_button.set_color_inside(dark_inside)
    right_button.set_color_inside(dark_inside)
    question_text_area.set_color_border(neon_border)
    question_option_area.set_color_border(neon_border)
    question_number_text.set_color_border(neon_border)
    correct_answers_text.set_color_border(neon_border)
    left_button.set_color_border(neon_border)
    middle_button.set_color_border(neon_border)
    right_button.set_color_border(neon_border)


def game(screen):

    song = music_dj()

    screen, wrong_answers, lives, right_answers, current_question, level, left_button, middle_button, right_button, question_text_area, question_option_area, question_number_text, correct_answers_text, questions_generator, objects = initialize_game(
        screen)
    
    pg.mixer.music.unload()
    pg.mixer.music.load("sounds/finlandia.mp3")
    pg.mixer.music.play(-1)

    while True:
        if wrong_answers == WRONG_LIMIT:
            lose()
        current_question += 1

        level_check = level
        level = set_level(level, right_answers)


        # Set song based on level
        if level_check < level:
            pg.mixer.music.unload()
            pg.mixer.music.load(next(song))
            pg.mixer.music.play(-1)
            

        try:
            tup = next(questions_generator)
            quest, ans, correct_ans = shuffle_answers(tup)
        except StopIteration:
            win()

        set_colors_for_level(level, objects)

        question_number_text.set_one_line_text(f"Question: {current_question}")
        question_number_text.draw(screen)
        correct_answers_text.set_one_line_text(
            f"Right:{right_answers} | Wrong:{wrong_answers}")
        correct_answers_text.draw(screen)
        question_text_area.set_text(wrap(quest, 20), 38)

        text_lines = [
            f'A: {ans["A"]}',
            f'B: {ans["B"]}',
            f'C: {ans["C"]}'
        ]
        question_option_area.set_text(text_lines, 60)
        question_text_area.draw(screen)
        question_option_area.draw(screen)
        left_button.draw(screen)
        middle_button.draw(screen)
        right_button.draw(screen)
        pg.display.flip()

        while wrong_answers < WRONG_LIMIT:
            if pg.event.get(pg.QUIT):
                se.button_sound.play()
                time.sleep(1)

                pg.quit()
                exit()
            if pg.event.get(pg.MOUSEBUTTONDOWN):
                mouse_pos = pg.mouse.get_pos()
                result = handle_button_click(
                    screen, left_button, middle_button, right_button, mouse_pos, correct_ans, question_text_area)
                if result == "correct":
                    se.right_answer_sound.play()
                    right_answers += 1
                    break
                elif result == "wrong":
                    se.wrong_answer_sound.play()
                    wrong_answers += 1
                    break


def button_correct_animation(screen, button: Button, feedback_element: Text, correct=True):
    neon_green = (57, 255, 20)
    red = (255, 0, 0)
    org_color = button.color
    org_border = button.border_color
    if correct:
        button.set_color_inside(neon_green)
        button.set_color_border(neon_green)
    else:
        button.set_color_inside(red)
        button.set_color_border(red)
    button.draw(screen)
    org_text = feedback_element.text
    feedback_element.set_one_line_text(
        "Correct answer!!" if correct else "Wrong answer!!")
    feedback_element.draw(screen)

    pg.display.flip()
    pg.time.delay(1200)

    button.set_color_inside(org_color)
    button.set_color_border(org_border)
    button.draw(screen)

    feedback_element.set_one_line_text(org_text)
    feedback_element.draw(screen)

    pg.display.flip()


def handle_button_click(screen, left_button, middle_button, right_button, mouse_pos, correct_ans, feedback_element: Text):
    if left_button.was_pressed(mouse_pos):
        if correct_ans == 'A':
            button_correct_animation(
                screen, left_button, feedback_element,  True)
            return "correct"
        else:
            button_correct_animation(
                screen, left_button, feedback_element,  False)
            return "wrong"
    elif middle_button.was_pressed(mouse_pos):
        if correct_ans == 'B':
            button_correct_animation(
                screen, middle_button, feedback_element, True)
            return "correct"
        else:
            button_correct_animation(
                screen, middle_button, feedback_element,  False)
            return "wrong"
    elif right_button.was_pressed(mouse_pos):
        if correct_ans == 'C':
            button_correct_animation(
                screen, right_button, feedback_element, True)
            return "correct"
        else:
            button_correct_animation(
                screen, right_button, feedback_element, False)
            return "wrong"


def lose():
    screen = pg.display.set_mode(SCREEN_SIZE)
    screen.fill((0, 0, 0))
    text = FONT_48.render("You lost!", True, (57, 255, 20))
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)
    screen.blit(text, text_rect)
    pg.display.flip()
    time.sleep(2)
    main()


def win():
    se.win_sound.play()
    screen = pg.display.set_mode(SCREEN_SIZE)
    screen.fill((0, 0, 0))
    text = FONT_48.render("You wín!", True, (57, 255, 20))
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)
    screen.blit(text, text_rect)
    pg.display.flip()
    time.sleep(2)
    main()


def main():

    pg.mixer.music.set_volume(0.3)
    pg.mixer.music.load("sounds/zelda.mp3")
    pg.mixer.music.play(-1)
    first = True
    while True:
        pg.display.set_caption("Quiz")
        screen = pg.display.set_mode(SCREEN_SIZE)
        # pg.display.set_icon(pg.image.load("icon.png"))
        intro(screen) if first else None
        menu(screen)
        first = False


if __name__ == "__main__":
    main()
