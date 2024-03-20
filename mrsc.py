'''mask reducible soft cosine'''

import torch
class mrsc(torch.nn.Module):
    def __init__(self, embedding_size = 1536, mask_width = 0):
        super(mrsc,self).__init__()

        mask = torch.ones(embedding_size,)
        self.mask = torch.nn.parameter.Parameter(data = mask, requires_grad = True)

        scale = 1*torch.ones(1,)
        self.scale = torch.nn.parameter.Parameter(data=scale, requires_grad=True)

        self.masked_cosine = lambda x,y: self.scale*(torch.sum( (x*y*self.mask) ))

    def forward(self, x_1, x_2):
        # print('self.scale',self.scale)
        return self.masked_cosine(x_1, x_2).reshape(1,)



if __name__=='__main__':
    m = mrsc(30)
    print('mask: ', m.mask)
    print('m.scale: ', m.scale)
    print(m.parameters().__next__(), m.parameters().__next__())




