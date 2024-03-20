import torch

class Aligner_model(torch.nn.Module):
    """Модель оптимизации положения облака подвижных точек GG
        У модели всего 3 параметра: phi, x, y, по умолчанию равны 0
        При инициализации конструктор принимает движущиеся
        точки в виде [[x1, y1],[x2, y2],[x3, y3], ... ]"""
    def __init__(self):
        super().__init__()
        phi = torch.tensor(data=[0.])
        self.phi = torch.nn.parameter.Parameter(phi)
        xy_trans = torch.tensor(data=[0.,0.])
        self.xy_trans = torch.nn.parameter.Parameter(xy_trans)
    def forward(self, moving_dots):
        '''Функция просто поворачивает точки из moving_dots и прибавляет к результату x_transб y_trans'''

        rotation_matrix = torch.tensor( [[torch.cos(self.phi/100), -torch.sin(self.phi/100)],
                                             [torch.sin(self.phi/100), torch.cos(self.phi/100)] ],
                                        requires_grad=True,
                                        dtype=torch.float)
        ans =  moving_dots@rotation_matrix + self.xy_trans
        # print('self.phi,self.xy_trans',self.phi,self.xy_trans)
        return ans

if __name__ == '__main__':
     m = Aligner_model()
     t = torch.tensor([[0,0.],[1,1.],[2,2.]])
     print(m(t))
     print('=============')
     pararams = m.named_parameters()
     for name, tensor in pararams:
         print(name)
         print(tensor)
         print('------------')
