# Модуль, принимающий на вход L = [[v_1, v_2, d], [v_1, v_3, d], [ ... ], ...]
# Делает шаг обучения маски и печатает лосс
# Важно: эта штука должна сохранять состояние параметров модели между вызовами...
# Модель будет создаваться и добавляться в пространство имён основного интерфейса при импорте модуля, так что всё ок
# По сути код в этом скрипте -- просто кусок кода, вырезанный из interface_main
import torch
import pygame

class Trainer():
    def __init__(self, L, G):
        self.L = L
        import torch; from mrsc import mrsc
        from itertools import count
        from random import randint
        import networkx; self.networkx = networkx
        from xy_mapping import xy_mapping
        import pygame
        self.pygame = pygame
        self.xy_mapping = xy_mapping
        self.G = G

        self.randint = randint
        self.count = count()
        self.torch = torch
        self.model = mrsc()
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=0.00001, momentum=0.9)
        self.loss = torch.nn.MSELoss()

        from copy import deepcopy as dc
        self.GG = dc(G)
        ne = networkx.non_edges(self.GG)
        self.GG.add_edges_from(ne)
    def mask_step(self):
        # print(f'========== {next(self.count)} ===========')

        self.optimizer.zero_grad()

        upper_bound = len(self.L)
        index = self.randint(0,upper_bound - 1)
        x_1 = self.L[index][0]; x_1 = self.torch.tensor(data=x_1, requires_grad=False)
        x_2 = self.L[index][1]; x_2 = self.torch.tensor(data=x_2, requires_grad=False)
        d = self.L[index][2]; d = self.torch.tensor(data=d, requires_grad=False).view(1,)

        self.d_pred = self.model.forward(x_1, x_2)
        # print('d_pred: ', self.d_pred)
        # print('d_target: ', d)

        lo = self.loss(self.d_pred,d)
        # print('loss: ', lo)
        # print(list(self.model.named_parameters()))
        # print(f'>>>>>>>>>>===={lo}====<<<<<<<<<<<')
        lo.backward()
        self.optimizer.step()
    def xy_fact_step(self):
        from xy_mapping import xy_mapping

        # xy_map -- модель оптимизации координат точек
        xy_map = xy_mapping(self.GG,self.model) # подвижные точки и маска как аргумент

        optimizer = self.torch.optim.SGD(xy_map.parameters(), lr = 0.01)
        loss = self.torch.nn.MSELoss()

        number_of_dots = len  (list(self.GG.nodes))
        # print('number_of_dots', number_of_dots)
        name_to_index_dot_association = xy_map.name_to_index_dot_association

        for i in range(1):
            for edge in self.GG.edges:
                dot_name_0 = edge[0]
                dot_name_1 = edge[1]
                index_0 = name_to_index_dot_association[dot_name_0]
                index_1 = name_to_index_dot_association[dot_name_1]
                emb_0 = self.GG.nodes[dot_name_0]['embedding']
                emb_1 = self.GG.nodes[dot_name_1]['embedding']
                emb_0 = self.torch.tensor(data = emb_0, dtype=self.torch.float64, requires_grad= False)
                emb_1 = self.torch.tensor(data=emb_1, dtype=self.torch.float64, requires_grad= False)
                d_p = self.model(emb_0,emb_1)
                d_p = torch.tensor(data=d_p,dtype=torch.float64,requires_grad=False)
                d_f = xy_map(index_0, index_1).view(1,)
                # print('d_f ', d_f, d_f.shape)
                # print('d_p', d_p, d_p.shape)
                optimizer.zero_grad()
                lo = loss(d_f, d_p)
                lo.backward()
                optimizer.step()
        self.GG = xy_map.move()
    def to_center(self):
        '''Устаревший метод -- заменём '''
        coords = []
        for node_name in self.GG.nodes:
            coords.append( self.GG.nodes[node_name]['position'] )
        x_c = [pos[0] for pos in coords]
        y_c = [pos[1] for pos in coords]
        x_c = int( sum(x_c)/len(x_c))
        y_c = int( sum(y_c) / len(y_c))
        dx = 500 - x_c
        dy = 500 - y_c

        for node_name in self.GG.nodes:
            pos = self.GG.nodes[node_name]['position']
            self.GG.nodes[node_name]['position'] = pos[0]+dx,pos[1]+dy
    def align(self):
        """Метод алайнмента облака подвижных точек к связанным тренировочным точкам (без алайнмента к свободным тренировочным).
        Этапы операции:
        1. Определить имена связанных тренировочных точек, используя self.G
        2. Создать словари соответствия имён и индексов name_to_index_alig и index_to_name_alig
        3. Задать модель оптимизации с параметрами-координатами в модуле alignment
        4. Изменить self.GG"""

        # names of the linked dots
        linked_names = []
        for name in self.G.nodes:
            # print('node_name', name)
            nhb = list( self.networkx.neighbors(self.G, name) )
            # print('self.networkx.neighbors(self.GG, n)', nhb, 'name: ',  name)
            if nhb!=[]:
                linked_names.append(name)

        # name <-> index
        name_to_index = dict()
        index_to_name = dict()
        c = 0
        for name in linked_names:
            name_to_index[name] = c
            index_to_name[c] = name
            c+=1

        # определение центра кластера
        XX = []
        YY = []
        for name in linked_names:
            xi = self.GG.nodes[name]['position'][0]
            yi = self.GG.nodes[name]['position'][1]
            XX.append(xi)
            YY.append(yi)
        x_c = (min(XX) + max(XX))/2
        y_c = (min(XX) + max(XX))/2

        # создаине тензора moving_dots
        dato = []
        for index in range(len(linked_names)):
            dato.append(self.GG.nodes[index_to_name[index]]['position'])
        moving_dots = torch.tensor(dato, requires_grad=False)
        # print('moving_dots', moving_dots)

        # преобрзование координат к центру кластера.
        delta_tensor = torch.tensor(data = [x_c, y_c], requires_grad=False)
        moving_dots = moving_dots - delta_tensor


        # получение координат целевых точек
        dato_t = []
        for index in range(len(linked_names)):
            dato_t.append(self.G.nodes[index_to_name[index]]['position'])
        target_dots = torch.tensor(dato_t, requires_grad=False)
        # print('target_dots', target_dots)
        target_dots = target_dots - delta_tensor

        target_dots = torch.tensor(target_dots,requires_grad=False, dtype=torch.float)
        moving_dots = torch.tensor(moving_dots,requires_grad=False, dtype=torch.float)
        # оптимизация угла поворота и xy-cмещения
        from aligner_model import Aligner_model
        ali_mod = Aligner_model()

        optimiz = torch.optim.SGD(ali_mod.parameters(), lr = 0.1)
        lo = torch.nn.MSELoss()
        for stp in range(10):
            optimiz.zero_grad()
            m_d = ali_mod(moving_dots)
            losss = lo(target_dots, m_d)
            losss.backward()
            optimiz.step()

        # возвращение к старым координатам.
        gg_dots_rotated = ali_mod(moving_dots)
        gg_dots_rotated = gg_dots_rotated + delta_tensor

        # обновление GG-графа.
        for index in index_to_name:
            torchindex = torch.tensor(index,dtype=torch.int)
            xxx = gg_dots_rotated[torchindex][0]
            yyy = gg_dots_rotated[torchindex][1]


            self.GG.nodes[index_to_name[index]]['position'] = xxx,yyy
    def to_surface(self, main_surface):
        pygame = self.pygame
        for node_name in self.GG.nodes:
            # print('self.GG.nodes[node_name][position]',self.GG.nodes[node_name]['position'])
            color = self.GG.nodes[node_name]['color']
            popo = self.GG.nodes[node_name]['position']
            popo = int(popo[0]), int(popo[1])

            pygame.draw.circle(main_surface, color, popo, 10)

            font = pygame.font.Font(None, 30)


            node_text = self.GG.nodes[node_name]['text']

            text = font.render(node_text, 2, (0, 0, 0))
            textpos = text.get_rect()
            textpos.centery = self.GG.nodes[node_name]['position'][1]
            textpos.centerx = self.GG.nodes[node_name]['position'][0]
            main_surface.blit(text, textpos)

            font = pygame.font.Font(None, 30)
            text = font.render(node_text, 2, (255, 255, 255))
            textpos = text.get_rect()
            textpos.centery = self.GG.nodes[node_name]['position'][1]
            textpos.centerx = self.GG.nodes[node_name]['position'][0]
            main_surface.blit(text, textpos)
    def get_GG(self):
        return self.GG
    def get_model(self):
        return self.model