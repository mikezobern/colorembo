import sys
import pygame; pygame.init()
import networkx as nx
class Dot():
    '''Constructor for all operations with dots: from storing to displaing'''
    def __init__(self):
        self.R = 20
        # self.links = 1
        self.G = nx.Graph() # create graph object
        self.G.add_node('test_dot_1', position = (120, 120), dragged = False, fixed = True)
        self.G.add_node('test_dot_2', position = (220, 230), dragged = False, fixed = True)
        self.G.add_node('test_dot_3', position=(500, 330), dragged=False, fixed=True)
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
        self.G.add_node(name_string, position = xy, dragged = False, fixed = True)
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
            print(' ----------> EDGE: ', edge)
            print('self.G.nodes[edge[0]]: ', self.G.nodes[edge[0]])
            start_dot = self.G.nodes[edge[0]]['position']
            print(' ----------> start_dot: ', start_dot)
            end_dot = self.G.nodes[edge[1]]['position']
            print(' ----------> end_dot: ', end_dot)
            pygame.draw.aaline(main_screen_surface,'white',start_dot, end_dot)
        for name_string in self.G.nodes:
            if self.G.nodes[name_string]['dragged']:
                pygame.draw.circle(surface, (225, 0, 0), self.G.nodes[name_string]['position'], self.R * 1.1)
            pygame.draw.circle(surface, (150, 150, 150), self.G.nodes[name_string]['position'], self.R)

            font = pygame.font.Font(None, self.R)
            text = font.render(name_string, 2, (0, 255, 150))
            textpos = text.get_rect()
            textpos.centery = self.G.nodes[name_string]['position'][1]
            textpos.centerx = self.G.nodes[name_string]['position'][0]
            surface.blit(text, textpos)
    def link(self,name_1,name_2):
        '''Method to link one dot to another'''
        self.G.add_edge(name_1,name_2)

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
        '''Returns the full activated button. If several buttons are activated,
        method returns the first activated button in list'''
        for button_dict in self.buttons:
            if button_dict['activated']:
                return button_dict['name']
        return None
button = Button()

main_screen_surface = pygame.display.set_mode((1000,1000))

awaiting_state = None # 'APP IS AWAITING DOT_NAME_1', 'APP IS AWAITING DOT_NAME_2'
dot_to_link_1 = None
dot_to_link_2 = None

while 1:
    main_screen_surface.fill('black')
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            dot_name = dot.dot_name_by_xy(event.pos)


            # It node is clicked, but there are no button activated, so I change do state... What a fuck! It is gibberish!
            if dot_name and button.get_activated() == None:
                dot.focus_defocus(dot_name)

            button_name = button.button_name_by_xy(event.pos)
            if button_name:
                activation_result = button.activate_desactivate_by_name(button_name)

            dot_to_action = dot.dot_name_by_xy(event.pos) # mouse has clicked to the node
            activated_button = button.get_activated()
            if activated_button and dot_to_action:
                if activated_button == 'the_delete_node_button':
                    dot.delete(dot_to_action)
            if activated_button == 'the_add_node_button':
                import random
                name = str(random.randint(1000000,20000000))
                dot.add(name, (500,500))

            if awaiting_state == 'APP IS AWAITING DOT_NAME_2' and dot_name and dot_to_link_1:
                print(3)
                dot.link(dot_to_link_1, dot_name)
                awaiting_state = None
                dot_to_link_1 = None
                dot_to_link_2 = None

            if awaiting_state=='APP IS AWAITING DOT_NAME_1' and dot_name and dot_to_link_2==None:
                awaiting_state = 'APP IS AWAITING DOT_NAME_2'
                dot_to_link_1 = dot_name
                dot_to_link_2 = None
                print(2)

            if activated_button == 'the_add_edge_button' and awaiting_state == None:
                print('waiting for click to a node...')
                awaiting_state = 'APP IS AWAITING DOT_NAME_1'
                dot_to_link_1 = None
                dot_to_link_2 = None







        if event.type == pygame.MOUSEBUTTONUP:
            if focused_name:
                dot.move(focused_name,event.pos)
                dot.focus_defocus(focused_name)

        if event.type == pygame.MOUSEMOTION:
            focused_name = dot.get_focused()
            if focused_name:
                dot.move(focused_name,event.pos)



    button.to_surface(main_screen_surface)

    dot.to_surface(main_screen_surface)
    pygame.display.flip()