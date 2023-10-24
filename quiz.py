import pygame as pg
import json

pg.init()

SCREEN_SIZE = (800, 800)
FONT = pg.font.Font("Arial", 30)

def get_questions(path:str):
    """
        Returns a dictionary with the question and the answers.
        THIS IS JUST A GUESS, I DON'T KNOW HOW THE JSON FILE IS STRUCTURED
    """
    return json.load(open(path))
    

class Area:
    def __init__(self, x:int, y:int, width:int, height:int):
        self.rect = pg.Rect(x, y, width, height)

    def set_border(self, width:int, color:tuple):
        self.border = width
        self.border_color = color
    
    def set_color_inside(self, color:tuple):
        self.color = color
    
    def set_color_border(self, color:tuple):
        self.border_color = color
    
    def set_text(self, text:str):
        self.text = text
    
    def set_pos(self, x:int, y:int):
        self.rect.x = x
        self.rect.y = y
    
    def draw(self, screen, text:str=None):
        pg.draw.rect(screen, self.color, self.rect)
        pg.draw.rect(screen, self.border_color, self.rect, 1)
        if text:
            global FONT
            text_surface = FONT.render(text, True, self.border_color)
            text_rect = text_surface.get_rect()
            text_rect.center = self.rect.center
            screen.blit(text_surface, text_rect)

class Button(Area):
    def __init__(self, x, y, width:int, height:int):
        super().__init__(x, y, width, height)
    
    def was_pressed(self, mouse_pos:tuple):
        if self.rect.collidepoint(mouse_pos):
            return True
        return False
    
class Text(Area):
    def __init__(self, x, y, width:int, height:int):
        super().__init__(x, y, width, height)
          

def intro(screen):
    pass

def menu(screen):
    pass

def game(screen):
    dark_gray = (50, 50, 50)
    screen.fill(dark_gray)
    
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

    left_button.set_pos(SCREEN_SIZE[0] / 3 - 230, SCREEN_SIZE[0] - SCREEN_SIZE[1] / 3 + 100) # bottom left corner
    middle_button.set_pos(SCREEN_SIZE[0] / 2 - 100, SCREEN_SIZE[0] - SCREEN_SIZE[1] / 3 + 100) # bottom middle corner
    right_button.set_pos(SCREEN_SIZE[0] - (SCREEN_SIZE[0]  / 3) + 30, SCREEN_SIZE[0] - SCREEN_SIZE[1] / 3 + 100) # bottom right corner

    question_text_area = Text(0, 0, 600, 200)
    question_text_area.set_color_inside(dark_gray)
    question_text_area.set_border(30, neon_green)
    question_text_area.set_pos(SCREEN_SIZE[0] / 2 - 300, SCREEN_SIZE[1] / 2 - 100)

    """
        Implement the logic of the game here
        Initial idea:
            - Get the question from the json file
            - Display the question
            - Display the answers
            - Check if the user clicked on the right answer
            - If the user clicked on the right answer, display the next question
            - If the user clicked on the wrong answer, display the game over screen
    """
    
    #questions_dict = get_questions("questions.json") ####### don't know how the json file is structured, so this is just a guess
    #amount_of_questions = len(questions_dict.keys())
    current_question = 0

    while True:
        #question_text_area.set_text(questions_dict[current_question]["question"])
        
        question_text_area.set_text("This is a question")

        question_text_area.draw(screen, question_text_area.text)
        left_button.draw(screen)
        middle_button.draw(screen)
        right_button.draw(screen)
        
        if pg.event.get(pg.MOUSEBUTTONDOWN):
            mouse_pos = pg.mouse.get_pos()
            if left_button.was_pressed(mouse_pos):
                left_button.set_color_inside((0, 255, 0))
                print("Left button was pressed")
            elif middle_button.was_pressed(mouse_pos):
                middle_button.set_color_inside((0, 255, 0))
                print("Middle button was pressed")
            elif right_button.was_pressed(mouse_pos):
                right_button.set_color_inside((0, 255, 0))
                print("Right button was pressed")
            else:
                print("No button was pressed")
        
        current_question += 1
        pg.display.update()


def main():
    """
        Game parts added to a list in order of execution
        a new screen is created for each part to clear the previous screen
    """
    parts = [intro, menu, game]
    pg.init()
    for part in parts:
        screen = pg.display.set_mode(SCREEN_SIZE)
        part(screen)
        pg.display.update()

if __name__ == "__main__": 
    main()