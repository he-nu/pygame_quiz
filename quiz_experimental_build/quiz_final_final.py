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

    def was_pressed(self, mouse_pos: tuple):
        if self.rect.collidepoint(mouse_pos):
            return True
        return False


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
                quit_button.set_color_inside((0, 255, 0))
                quit_button.draw(screen)
                pg.display.flip()
                pg.time.delay(250)
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


def game(screen):
    black = (0, 0, 0)
    wrong_answers = 0
    lives = WRONG_LIMIT
    right_answers = 0
    current_question = 0
    screen.fill(black)

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

    left_button.set_pos(SCREEN_SIZE[0] / 3 - 216,
                        SCREEN_SIZE[0] - SCREEN_SIZE[1] / 3 + 110)
    middle_button.set_pos(
        SCREEN_SIZE[0] / 2 - 100, SCREEN_SIZE[0] - SCREEN_SIZE[1] / 3 + 110)
    right_button.set_pos(SCREEN_SIZE[0] - (SCREEN_SIZE[0] / 3) + 15,
                         SCREEN_SIZE[0] - SCREEN_SIZE[1] / 3 + 110)

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

    # lives_text = Text(SCREEN_SIZE[0] - 200, 80, 200, 50)
    # lives_text.set_font(FONT_32)
    # lives_text.set_color_inside(black)
    # lives_text.set_border(30, neon_green)
    # lives_text.set_pos(0, 0)

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

    questions_generator = get_next_question()

    while True:
        screen.fill(black)
        if wrong_answers == WRONG_LIMIT:
            lose()
        current_question += 1

        try:
            tup = next(questions_generator)
            quest, ans, correct_ans = tup
        except StopIteration:
            win()

        question_number_text.set_one_line_text(
            f"Question: {current_question}")
        question_number_text.draw(screen)

        # lives_text.set_text(f"Lives: {lives}", 40)
        # lives_text.draw(screen)

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
                pg.quit()
                exit()
            if pg.event.get(pg.MOUSEBUTTONDOWN):

                mouse_pos = pg.mouse.get_pos()

                if left_button.was_pressed(mouse_pos):
                    left_button.set_color_inside((0, 255, 0))
                    left_button.draw(screen)
                    pg.display.flip()
                    pg.time.delay(150)
                    if correct_ans == "A":
                        print("Correct answer")

                        right_answers += 1

                        question_text_area.set_one_line_text(
                            "Correct answer!!")
                        question_text_area.draw(screen)
                        left_button.set_color_inside(dark_green)
                        left_button.draw(screen)
                        pg.display.flip()
                        se.right_answer_sound.play()
                        pg.time.delay(1500)
                        break  # Exit the loop when the correct answer is selected
                    else:
                        print("Wrong answer")
                        
                        wrong_answers += 1
                        question_text_area.set_one_line_text("Wrong answer!!")
                        question_text_area.draw(screen)
                        left_button.set_color_inside((255, 0, 0))
                        left_button.draw(screen)
                        pg.display.flip()
                        se.wrong_answer_sound.play()
                        pg.time.delay(1500)
                        question_text_area.set_text([quest], 60)
                        left_button.set_color_inside(dark_green)
                        left_button.draw(screen)
                        pg.display.flip()

                if middle_button.was_pressed(mouse_pos):
                    middle_button.set_color_inside((0, 255, 0))
                    middle_button.draw(screen)
                    pg.display.flip()
                    pg.time.delay(150)
                    if correct_ans == "B":
                        print("Correct answer")

                        right_answers += 1

                        question_text_area.set_one_line_text(
                            "Correct answer!!")
                        question_text_area.draw(screen)
                        middle_button.set_color_inside(dark_green)
                        middle_button.draw(screen)
                        pg.display.flip()
                        se.right_answer_sound.play()
                        pg.time.delay(1500)
                        break  # Exit the loop when the correct answer is selected
                    else:
                        print("Wrong answer")
                        wrong_answers += 1
                        question_text_area.set_one_line_text("Wrong answer!!")
                        question_text_area.draw(screen)
                        middle_button.set_color_inside((255, 0, 0))
                        middle_button.draw(screen)
                        pg.display.flip()
                        se.wrong_answer_sound.play()
                        pg.time.delay(1500)
                        question_text_area.set_text([quest], 60)
                        middle_button.set_color_inside(dark_green)
                        middle_button.draw(screen)
                        pg.display.flip()

                if right_button.was_pressed(mouse_pos):
                    right_button.set_color_inside((0, 255, 0))
                    right_button.draw(screen)
                    pg.display.flip()
                    pg.time.delay(150)
                    if correct_ans == "C":
                        print("Correct answer")

                        right_answers += 1

                        question_text_area.set_one_line_text(
                            "Correct answer!!")
                        question_text_area.draw(screen)
                        right_button.set_color_inside(dark_green)
                        right_button.draw(screen)
                        pg.display.flip()
                        se.right_answer_sound.play()
                        pg.time.delay(1500)
                        break  # Exit the loop when the correct answer is selected
                    else:
                        print("Wrong answer")
                        wrong_answers += 1
                        question_text_area.set_one_line_text("Wrong answer!!")
                        question_text_area.draw(screen)
                        right_button.set_color_inside((255, 0, 0))
                        right_button.draw(screen)
                        pg.display.flip()
                        se.wrong_answer_sound.play()
                        pg.time.delay(1500)
                        question_text_area.set_text([quest], 60)
                        right_button.set_color_inside(dark_green)
                        right_button.draw(screen)
                        pg.display.flip()


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
