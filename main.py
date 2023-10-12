import pygame as pg

SCREEN_SIZE = (800, 800)

class Area:
    def __init__(self, x:int, y:int, width:int, height:int):
        self.rect = pg.Rect(x, y, width, height)
    
    def set_color_inside(self, color):
        self.color = color
    
    def set_color_border(self, color):
        self.border_color = color
    
    def set_text(self, text):
        self.text = text
    
    def draw(self, screen, text=None):
        pg.draw.rect(screen, self.color, self.rect)
        pg.draw.rect(screen, self.border_color, self.rect, 1)
        if text:
            screen.blit(text, self.rect)
    

class Button(Area):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
    
        

def intro(screen):
    pass

def menu(screen):
    start_button = pg.Rect(0, 0, 200, 75)
    start_button_text = pg.font.SysFont('Arial', 20).render('Start', True, (140, 0, 0))
    exit_button = pg.Rect(0, 0, 200, 75)
    exit_button_text = pg.font.SysFont('Arial', 20).render('Exit', True, (140, 0, 0))
    
    def _register_button_press(button, event):
        if (event.type == pg.MOUSEBUTTONDOWN and
            button.collidepoint(event.pos)):
                return True
        return False
    
    def _draw_button(screen, button, button_text, pos):
        print("Button drawn")
        button.center = pos
        screen.blit(button_text, button)
        pg.draw.rect(screen, (50, 20, 50), button, 1)
        pg.display.update()
        
    
    print("Drawing Buttons")
    
    _draw_button(screen, start_button, start_button_text, (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2))
    _draw_button(screen, exit_button, exit_button_text, (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 + 100))
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if _register_button_press(start_button, event):
                return "start"
            if _register_button_press(exit_button, event):
                return "exit"
            
def game(screen):
    question_area = pg.Rect(0, 0, 200, 800)
    answer_options_area = pg.Rect(0, 0, 300, 800)
    answer_buttons_area = pg.Rect(0, 0, 200, 800)                
    pg.draw.rect(screen, (180, 0, 0), question_area)
    pg.draw.rect(screen, (180, 0, 0), answer_options_area)
    pg.draw.rect(screen, (180, 0, 0), answer_buttons_area)
    
def main():
    running = True
    screen = pg.display.set_mode(SCREEN_SIZE)
    pg.init()
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        pg.display.update()
        pg.display.set_caption("Quiz Game")
        intro(screen)
        print("starting menu")
        
        menu_state = menu(screen)
        if menu_state == "exit":
            exit(0)

        game(screen)
        
        
        
main()