import torch

class xy_mapping(torch.nn.Module):
    '''Превращаем предсказанные дистанции в фактические положения точек'''
    def __init__(self, GG, cosine_model):
        super().__init__()
        # GG -- граф подвижных точек
        # cosine_model -- модель, предсказывающая дистанции между эмбеддингами ("mrsc")
        self.GG = GG
        self.cosine_model = cosine_model

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
        c = 0
        for node_pos in self.node_positions:
            pos = node_pos.tolist()
            node_name = self.index_to_name_dot_association[c]
            c+=1
            self.GG.nodes[node_name]['position'] = pos
        return self.GG