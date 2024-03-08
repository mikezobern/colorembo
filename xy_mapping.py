import torch
import networkx

class xy_mapping(torch.nn.Module):
    # Конструктор функции определения расстояния
    # Инстанс принимает на вход граф подвижных точек GG
    # Возвращает тоже GG
    def __init__(self, GG, cosine_model):
        super().__init__()
        # GG -- граф подвижных точек
        # cosine_model -- модель, предсказывающая дистанции между эмбеддингами ("mrsc")


        self.GG = GG
        self.cosine_model = cosine_model
        print('self.GG.edges', self.GG.edges)
        '''
        XY_TRAIN_DATA = []
        for edge in self.GG.edges:
            node_name_A = edge[0]
            node_name_B = edge[1]
            pos_A = self.GG.nodes[node_name_A]['position']
            pos_B = self.GG.nodes[node_name_B]['position']

            emb_A = self.GG.nodes[node_name_A]['embedding']
            emb_B = self.GG.nodes[node_name_B]['embedding']
            emb_A = self.torch.tensor(data = emb_A, requires_grad= False)
            emb_B = self.torch.tensor(data=emb_B, requires_grad= False)

            target_distance_from_mask = self.cosine_model(emb_A, emb_B)
            print('--------')
            print(node_name_A, pos_A, node_name_B, pos_B, target_distance_from_mask)
            XY_TRAIN_DATA.append([node_name_A, pos_A, node_name_B, pos_B, target_distance_from_mask])
        print('XY_TRAIN_DATA',XY_TRAIN_DATA)
        '''
        # node_positions -- это текущее положение подвижных точек, определяемое как параметры модели
        # при инициализации xy_mapping в node_positions добавляются точки из GG
        # есть проблема: имена точек надо проассоциировать с индексами
        # сделаю словарь "индекс: имя" и сохраню как name_index_dot_association

        index_ = 0
        name_to_index_dot_association = dict()
        index_to_name_dot_association = dict()
        node_positions = []
        for node_name_ in self.GG.nodes:
            name_to_index_dot_association[node_name_] = index_
            index_to_name_dot_association[index_] = node_name_
            node_positions.append(self.GG.nodes[node_name_]['position'])
            index_+=1

        self.name_to_index_dot_association = name_to_index_dot_association
        self.index_to_name_dot_association = index_to_name_dot_association

        node_positions = torch.tensor(data = node_positions,dtype=float, requires_grad=False)
        self.node_positions = torch.nn.parameter.Parameter(data = node_positions,
                                                           requires_grad = True)

        self.r = lambda pos_1, pos_2: torch.sum( (pos_1 - pos_2)**2 )**0.5



    def forward(self, node_1_index, node_2_index):
        # Расчёт расстояния между двумя нодами по их индексам
        return self.r(self.node_positions[node_1_index], self.node_positions[node_2_index])


    def move(self):
        # перенести координаты точек из параметров модели на GG
        self.index_to_name_dot_association
        self.node_positions
        self.GG
        # print('===============---------------0000000000000000000000000')
        # print(self.node_positions)
        c = 0
        for node_pos in self.node_positions:
            pos = node_pos.tolist()
            pos = [int(i) for i in pos]
            # print(c,pos)
            node_name = self.index_to_name_dot_association[c]
            c+=1
            self.GG.nodes[node_name]['position'] = pos
            # print(self.GG.nodes)
        # print('===============---------------0000000000000000000000000')
        return self.GG


if __name__ == '__main__':
    pass
    '''
    node_positions = [[1, 2.], [4, 6.]]
    fnc = xy_mapping(node_positions)
    d = fnc(0,1)
    print(d)

    optimizer = torch.optim.Adam(fnc.parameters())
    loss = torch.nn.MSELoss()

    for i in range(100):
        optimizer.zero_grad()
        d_f = fnc(0,1)
        targe = torch.tensor(data=6.,requires_grad=False)
        lo = loss(d_f, targe)
        print(d_f)
        print(list(fnc.parameters()))
        print('node_positions: \n', node_positions)
        lo.backward()
        optimizer.step()
    '''