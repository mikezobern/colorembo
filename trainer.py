# Модуль, принимающий на вход L = [[v_1, v_2, d], [v_1, v_3, d], [ ... ], ...]
# Делает шаг обучения маски и печатает лосс
# Важно: эта штука должна сохранять состояние параметров модели между вызовами...
# Модель будет создаваться и добавляться в пространство имён основного интерфейса при импорте модуля, так что всё ок
# По сути код в этом скрипте -- просто кусок кода, вырезанный из interface_main
import torch


class Trainer():
    def __init__(self, L, G):
        self.L = L
        import torch; from mrsc import mrsc
        from itertools import count
        from random import randint
        import networkx
        from xy_mapping import xy_mapping
        import pygame
        self.pygame = pygame
        self.xy_mapping = xy_mapping


        self.randint = randint
        self.count = count()
        self.torch = torch
        self.model = mrsc()
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=0.0001, momentum=0.9)
        self.loss = torch.nn.MSELoss()

        from copy import deepcopy as dc
        self.GG = dc(G)
        ne = networkx.non_edges(self.GG)
        self.GG.add_edges_from(ne)

    def mask_step(self):
        print(f'========== {next(self.count)} ===========')

        self.optimizer.zero_grad()

        upper_bound = len(self.L)
        index = self.randint(0,upper_bound - 1)
        x_1 = self.L[index][0]; x_1 = self.torch.tensor(data=x_1, requires_grad=False)
        x_2 = self.L[index][1]; x_2 = self.torch.tensor(data=x_2, requires_grad=False)
        d = self.L[index][2]; d = self.torch.tensor(data=d, requires_grad=False)

        self.d_pred = self.model.forward(x_1, x_2)
        print('d_pred: ', self.d_pred)
        print('d_target: ', d)

        lo = self.loss(self.d_pred,d)
        # print('loss: ', lo)
        # print(list(self.model.named_parameters()))
        print(f'>>>>>>>>>>===={lo}====<<<<<<<<<<<')
        lo.backward()
        self.optimizer.step()

    def xy_fact_step(self):
        from xy_mapping import xy_mapping

        # xy_map -- модель оптимизации координат точек
        xy_map = xy_mapping(self.GG,self.model)

        optimizer = self.torch.optim.Adam(xy_map.parameters())
        loss = self.torch.nn.MSELoss()

        number_of_dots = len  (list(self.GG.nodes))
        print('number_of_dots', number_of_dots)
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
                d_f = xy_map(index_0, index_1)
                optimizer.zero_grad()
                lo = loss(d_f, d_p)
                lo.backward()
                optimizer.step()

        self.GG = xy_map.move()
        '''
        for node in self.GG.nodes:
            po = self.GG.nodes[node]['position']
            print(f'name {node}, pos {po}')
        '''

    def to_center(self):
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

    def to_surface(self, main_surface):
        pygame = self.pygame
        for node_name in self.GG.nodes:
            print('self.GG.nodes[node_name][position]',self.GG.nodes[node_name]['position'])
            color = self.GG.nodes[node_name]['color']
            pygame.draw.circle(main_surface, color, self.GG.nodes[node_name]['position'], 10)



