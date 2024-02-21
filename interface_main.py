import sys
import pygame; pygame.init()
import networkx as nx
class Dot():
    '''Constructor for all operations with dots: from storing to displaing'''
    def __init__(self):
        self.R = 20
        # self.links = 1
        self.G = nx.Graph() # create graph object

        self.G.add_node('test_dot_1', position = (120, 120), dragged = False, fixed = True, highlight = False)
        self.G.add_node('test_dot_2', position = (220, 230), dragged = False, fixed = True, highlight = False)
        self.G.add_node('test_dot_3', position=(500, 330), dragged=False, fixed=True, highlight = False)


        self.G.add_edge('test_dot_1','test_dot_2')
        self.G.add_edge('test_dot_2', 'test_dot_3')
        self.G.add_edge('test_dot_1', 'test_dot_3')
    def move(self, name_string, destination:tuple):
        self.G.nodes[name_string]['position'] = destination
    def get_focused(self):
        for node_name in self.G.nodes:
            if self.G.nodes[node_name]['dragged']:
                return node_name
    def focus_defocus(self,name_string):
        self.G.nodes[name_string]['dragged'] = not self.G.nodes[name_string]['dragged']
        if self.G.nodes[name_string]['dragged']:
            return name_string
    def add(self, name_string: str, xy: tuple) -> None:
        self.G.add_node(name_string, position = xy, dragged = False, fixed = True, highlight=False)
    def delete(self, name_string: str) -> None:
        '''
        delete node
        '''
        self.G.remove_node(name_string)
    def dot_name_by_xy(self, cursor_coordinates: tuple) -> None|str:
        '''Method returns the name of the dot that is overlapping with cursor;
        If there are several dots, method chooses one o them randomly.'''
        for name_string in self.G.nodes:
            pos = self.G.nodes[name_string]['position']
            if ((cursor_coordinates[0] - pos[0])**2 + (cursor_coordinates[1] - pos[1])**2 <= self.R**2): # within 10 pixels on the screen
                return name_string
        return None
    def to_surface(self, surface: pygame.surface.Surface):
        '''Method to draw all dots and edges on the screen'''
        for edge in self.G.edges:
            start_dot = self.G.nodes[edge[0]]['position']
            end_dot = self.G.nodes[edge[1]]['position']
            pygame.draw.aaline(main_screen_surface,'white',start_dot, end_dot)
        for name_string in self.G.nodes:
            if self.G.nodes[name_string]['dragged']:
                pygame.draw.circle(surface, (225, 0, 0), self.G.nodes[name_string]['position'], self.R * 1.1)
            pygame.draw.circle(surface, (150, 150, 150), self.G.nodes[name_string]['position'], self.R)

            if self.G.nodes[name_string]['highlight']:
                pygame.draw.circle(surface, (0, 255, 0), self.G.nodes[name_string]['position'], self.R * 1.1)
            pygame.draw.circle(surface, (150, 150, 150), self.G.nodes[name_string]['position'], self.R)

            font = pygame.font.Font(None, self.R)
            text = font.render(name_string, 2, (0, 255, 150))
            textpos = text.get_rect()
            textpos.centery = self.G.nodes[name_string]['position'][1]
            textpos.centerx = self.G.nodes[name_string]['position'][0]
            surface.blit(text, textpos)

    def highlight(self, dot_name):
        self.G.nodes[dot_name]['highlight'] = True
        print(dot_name, self.G.nodes[dot_name]['highlight'], ' is highlited')

    def no_highlight(self, dot_name):
        self.G.nodes[dot_name]['highlight'] = False
        print(dot_name, self.G.nodes[dot_name]['highlight'], ' is not highlited')

    def link(self,name_1,name_2):
        '''Method to link one dot to another'''
        self.G.add_edge(name_1,name_2)

    def unlink(self, name_1,name_2):
        '''Unlink two dots it they are linked'''
        try:
            self.G.remove_edge(name_1,name_2)
        except:
            pass

dot = Dot()

class Button():
    '''The fasade for the collections of buttons;
    activated like Dot class.'''
    def __init__(self):
        '''initialize buttons'''
        the_add_node_button = { 'color': (255,255,255),
                                'rect': pygame.Rect(10,10,50,50),
                                'text': 'o+',
                                'name': 'the_add_node_button',
                                'activated': False
                                }

        the_delete_node_button = { 'color': (255,255,255),
                                'rect': pygame.Rect(10,70,50,50),
                                'text': 'o-',
                                'name': 'the_delete_node_button',
                                'activated': False
                                }

        the_add_edge_button = { 'color': (255,255,255),
                                'rect': pygame.Rect(10,130,50,50),
                                'text': '/+',
                                'name': 'the_add_edge_button',
                                'activated': False
                                }

        the_delete_edge_button = { 'color': (255,255,255),
                                'rect': pygame.Rect(10,190,50,50),
                                'text': '/-',
                                'name': 'the_delete_edge_button',
                                'activated': False
                                }
        self.buttons = [the_add_node_button,
                        the_delete_node_button,
                        the_add_edge_button,
                        the_delete_edge_button]



    def button_name_by_xy(self,xy):
        '''Returns name of the button, if cursor coordinates xy
        is laying inside the button's rectangle'''
        for button_dict in self.buttons:
            rect = button_dict['rect']
            cursor_rect = pygame.Rect(xy[0], xy[1], 1, 1)
            is_inside = rect.contains(cursor_rect)
            if is_inside:
                button_name = button_dict['name']
                return button_name
        return None

    def activate_desactivate_by_name(self, button_name):
        '''Activate and desactivate focus at the given
        button by the button_name'''
        for button in self.buttons:
            if button['name'] == button_name:
                button['activated'] = not button['activated']

    def activate_by_name(self, button_name):
        '''Activate focus at the given
        button by the button_name'''
        for button in self.buttons:
            if button['name'] == button_name:
                button['activated'] = True

    def desactivate_by_name(self, button_name):
        '''DesActivate focus at the given
        button by the button_name'''
        for button in self.buttons:
            if button['name'] == button_name:
                button['activated'] = False


    def to_surface(self, surface):
        '''Method for visualising all buttons on the screen'''
        for button_dict in self.buttons:
            if button_dict['activated']:
                underlying_red_rect = button_dict['rect'].scale_by(1.1, 1.1)
                underlying_red_rect.centerx = button_dict['rect'].centerx
                underlying_red_rect.centery = button_dict['rect'].centery
                pygame.draw.rect(surface,'red', underlying_red_rect,border_radius = 5)

            pygame.draw.rect(main_screen_surface, 'white', button_dict['rect'], width = 3, border_radius = 5)
            font = pygame.font.Font(None, 50)
            text = font.render(button_dict['text'], 1, 'white')
            textpos = text.get_rect()
            textpos.centerx = button_dict['rect'].centerx
            textpos.centery = button_dict['rect'].centery
            main_screen_surface.blit(text, textpos)

    def get_activated(self):
        '''Returns the name of the first activated button in list'''
        for button_dict in self.buttons:
            if button_dict['activated']:
                return button_dict['name']
        return None
button = Button()


main_screen_surface = pygame.display.set_mode((1000,1000))

app_state = None
first_dot_to_edge_delete = None
node_dragging = None

while 1:
    main_screen_surface.fill('black')
    for event in pygame.event.get():

        internal_actions = 0

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos

            # АКТИВИРОВАТЬ КНОПКУ "ДОБАВИТЬ НОДУ":
            # Если никакие кнопки не активированы
            # И если клик пришелся на кнопку "добавить"
            # То активировать кнопку и перевести программу в состояние "ЖДУ КЛИКА ДЛЯ ДОБАВЛЕНИЯ ТОЧКИ
            if button.get_activated()==None \
                    and button.button_name_by_xy(pos)=='the_add_node_button':
                print('АКТИВИРОВАТЬ КНОПКУ "ДОБАВИТЬ НОДУ"')
                button.activate_by_name('the_add_node_button')
                app_state = 'AWAITING DOT ADDING'
                internal_actions += 1

            # ДЕЗАКТИВИРОВАТЬ КНОПКУ "ДОБАВИТЬ НОДУ"
            if button.button_name_by_xy(pos)=='the_add_node_button' \
                    and app_state == 'AWAITING DOT ADDING' \
                    and internal_actions == 0:
                print('ДЕЗАКТИВИРОВАТЬ КНОПКУ @ДОБАВИТЬ НОДУ@')
                button.desactivate_by_name('the_add_node_button')
                internal_actions = 1
                app_state = None


            # ДОБАВИТЬ НОВУЮ НОДУ
            # если уже активирована кнопка "добавить",
            # после активации кнопки "добавить" юзер никуда не кликал и если сейчас мышка опустилась на поле,
            # то нужно в эту точку добавить новую ноду
            if button.get_activated()=='the_add_node_button' \
                    and app_state == 'AWAITING DOT ADDING' \
                    and internal_actions == 0:
                print('ДОБАВИТЬ НОВУЮ НОДУ')
                dot.add('svsvsvsvsvsv',pos)
                internal_actions = 1
                button.desactivate_by_name('the_add_node_button')
                app_state = None

            # Активировать кнопку "удалить ноду"
            but_name = button.button_name_by_xy(pos)
            if but_name=='the_delete_node_button' \
                    and app_state == None \
                    and internal_actions == 0:
                print('Активировать кнопку "удалить ноду"')
                button.activate_by_name(but_name)
                internal_actions += 1
                app_state = 'AWAITING DOT DELETING'

            # Обработать клик удаления удаление ноды
            dot_name = dot.dot_name_by_xy(event.pos)
            if dot_name \
                    and internal_actions == 0 \
                    and app_state == 'AWAITING DOT DELETING':
                print('Обработать клик удаления удаление ноды')
                dot.delete(dot_name)
                internal_actions += 1
                button.desactivate_by_name('the_delete_node_button')
                app_state = None

            # дезактивировать кнопку "удалить ноду"
            if internal_actions == 0 \
                    and app_state == 'AWAITING DOT DELETING' \
                    and button.button_name_by_xy(pos) =='the_delete_node_button':
                print('Дезактивая кнопки удаления ноды')
                app_state = None
                internal_actions += 1
                button.desactivate_by_name('the_delete_node_button')

            # Активировать кнопку "добавить ребро"
            if internal_actions == 0 \
                    and app_state == None \
                    and button.button_name_by_xy(pos) == 'the_add_edge_button' \
                    and button.get_activated()!='the_add_edge_button':
                print('Активирована кнопка ДОБАВИТЬ РЕБРО')
                internal_actions = 1
                button.activate_by_name('the_add_edge_button')
                app_state = 'AWAITING EDGE ADDING NODE 1'

            # Дезактивировать кнопку "добавить ребро"
            if internal_actions == 0 \
                    and (app_state == 'AWAITING EDGE ADDING NODE 1' or app_state == 'AWAITING EDGE ADDING NODE 2')\
                    and button.get_activated()=='the_add_edge_button' \
                    and button.button_name_by_xy(pos)=='the_add_edge_button':
                button.desactivate_by_name('the_add_edge_button')
                internal_actions = 1
                app_state = None

            # Обработать первый клик после активации кнопки "добавить ребро"
            if internal_actions == 0 \
                    and (app_state == 'AWAITING EDGE ADDING NODE 1')\
                    and button.get_activated()=='the_add_edge_button' \
                    and dot.dot_name_by_xy(pos):
                print('Обработать первый клик после активации кнопки "добавить ребро"')
                internal_actions = 1
                app_state = 'AWAITING EDGE ADDING NODE 2'
                linking_node_1 = dot.dot_name_by_xy(pos)
                dot.highlight(linking_node_1)

            # Обработать второй клик после активации кнопки "добавить ребро"
            if internal_actions == 0 \
                    and (app_state == 'AWAITING EDGE ADDING NODE 2')\
                    and button.get_activated()=='the_add_edge_button' \
                    and dot.dot_name_by_xy(pos)\
                    and linking_node_1 != dot.dot_name_by_xy(pos):
                print('Обработать второй клик после активации кнопки "добавить ребро"')
                internal_actions = 1
                app_state = None
                dot.link(linking_node_1,dot.dot_name_by_xy(pos))
                button.desactivate_by_name('the_add_edge_button')
                dot.no_highlight(linking_node_1)

            # Активировать кнопку "удалить ребро"
            if internal_actions == 0 \
                    and app_state == None \
                    and button.get_activated()==None \
                    and button.button_name_by_xy(pos) == 'the_delete_edge_button':
                print('Активировать кнопку "удалить ребро"')
                button.activate_by_name('the_delete_edge_button')
                internal_actions = 1
                app_state = 'AWAITING FIRST NODE TO EDGE DELETION'

            # Дезактивировать кнопку "удалить ребро"
            if internal_actions == 0 \
                    and app_state == 'AWAITING FIRST NODE TO EDGE DELETION' \
                    and button.get_activated()== 'the_delete_edge_button' \
                    and button.button_name_by_xy(pos) == 'the_delete_edge_button':
                print('Дезактивировать кнопку "удалить ребро"')
                button.desactivate_by_name('the_delete_edge_button')
                internal_actions = 1
                app_state = None

            # Обработать 1 клик после активации кнопки "удалить ребро"

            if internal_actions == 0 \
                    and app_state == 'AWAITING FIRST NODE TO EDGE DELETION' \
                    and button.get_activated() == 'the_delete_edge_button' \
                    and dot.dot_name_by_xy(pos) \
                    and first_dot_to_edge_delete == None:
                print('Обработать 1 клик после активации кнопки "удалить ребро"')
                internal_actions = 1

                dot.highlight(dot.dot_name_by_xy(pos))
                first_dot_to_edge_delete = dot.dot_name_by_xy(pos)
                app_state = 'AWAITING SECOND NODE TO EDGE DELETION'

            # Обработать 2 клик после активации кнопки "удалить ребро"
            if internal_actions == 0 \
                    and app_state == 'AWAITING SECOND NODE TO EDGE DELETION' \
                    and button.get_activated() == 'the_delete_edge_button' \
                    and dot.dot_name_by_xy(pos) \
                    and first_dot_to_edge_delete != None:
                print('Обработать 2 клик после активации кнопки "удалить ребро"')
                internal_actions = 1
                app_state = None
                dot.no_highlight(first_dot_to_edge_delete)
                button.desactivate_by_name('the_delete_edge_button')
                dot.unlink(first_dot_to_edge_delete, dot.dot_name_by_xy(pos))
                first_dot_to_edge_delete = None


        if event.type == pygame.MOUSEMOTION:
            if dot.dot_name_by_xy(event.pos) \
                    and event.buttons[0] \
                    and app_state == None:
                print('pos', event.pos)
                print('but', event.buttons)
                dot.move(dot.dot_name_by_xy(event.pos), event.pos)

        if event.type == pygame.MOUSEBUTTONUP:
            pass


    button.to_surface(main_screen_surface)
    dot.to_surface(main_screen_surface)
    pygame.display.flip()