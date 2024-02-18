import sys
import pygame
pygame.init()
main_screen_surface = pygame.display.set_mode((1000,1000))
class Dot():
    '''Constructor for all operations with dots: from storing to displaing'''
    def __init__(self):
        self.points = {'test_dot_1':[(150,150),False],'test_dot_2':[(500,500),False]}
        self.R = 20
        self.links = 
    def move(self, name_string, destination:tuple):
        self.points[name_string][0] = destination
    def get_focused(self):
        for name in self.points:
            if self.points[name][1]:
                return name
    def focus_defocus(self,name_string):
        self.points[name_string][1] = not self.points[name_string][1]
        if self.points[name_string][1]:
            return name_string
    def add(self, name_string: str, xy: tuple) -> None:
        self.points[name_string] = [(150,150),False]
        self.points[name_string][0] = xy
    def delete(self, name_string: str) -> None:
        del self.points[name_string]
    def dot_name_by_xy(self, cursor_coordinates: tuple) -> None|str:
        '''Method returns the name of the dot that is overlapping with cursor;
        If there are several dots, method chooses one o them randomly.'''
        for name_string, xy_and_state in self.points.items():
            if ((cursor_coordinates[0] - xy_and_state[0][0])**2 + (cursor_coordinates[1] - xy_and_state[0][1])**2 <= self.R**2): # within 10 pixels on the screen
                return name_string
        return None
    def to_surface(self, surface: pygame.surface.Surface):
        '''Method to draw all dots on the screen'''
        for name_string, xy_and_state in self.points.items():
            if xy_and_state[1]:
                pygame.draw.circle(surface, (225, 0, 0), xy_and_state[0], self.R*1.1)
            pygame.draw.circle(surface,(150,150,150),xy_and_state[0],self.R)
            font = pygame.font.Font(None, self.R)
            text = font.render(name_string, 2, (0, 255, 150))
            textpos = text.get_rect()
            textpos.centery = xy_and_state[0][1]
            textpos.centerx = xy_and_state[0][0]
            surface.blit(text, textpos)
    def link(self,name_1,name_2):
        '''Method to link one dot to another'''




dot = Dot()

dot.add('FOXY',(230,230))



while 1:
    main_screen_surface.fill('black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            dot_name = dot.dot_name_by_xy(event.pos)
            if dot_name:
                focused_name = dot.focus_defocus(dot_name)
        if event.type == pygame.MOUSEBUTTONUP:
            if focused_name:
                dot.move(focused_name,event.pos)
                dot.focus_defocus(focused_name)
        if event.type == pygame.MOUSEMOTION:
            focused_name = dot.get_focused()
            if focused_name:
                dot.move(focused_name,event.pos)

    pygame.draw.aaline(main_screen_surface, (255,150,50), (100,100), (500,250))
    dot.to_surface(main_screen_surface)
    pygame.display.flip()