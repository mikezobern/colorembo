import networkx
import torch
class Neighbours_to_terminal():
    """Для каждой свободной точки выводит в терминал список ближайших тренировочных соседей """
    def __init__(self):
        print('Инициализация neighbours_to_terminal')
    def print_to_terminal(self,G: networkx.Graph, GG: networkx.Graph, model):
        print('model params', list(model.parameters()))
        print('Активирован метод print_to_terminal')
        # делаем словарь {имя_тренировочной_точки: G-эмбеддинг}
        # с эмбеддингами тренировочных точек на основе G.
        tren_dict = dict()
        for name in G.nodes:
            if list( networkx.neighbors(G, name) ): # Если есть соседи
                print(f'''имя тренировочной G точки {G.nodes[name]['text']}''')
                tren_dict[name] = G.nodes[name]['embedding']
        # делаем словарь свободных точек {имя_свободной_точки: GG-эмбеддинг}
        free_dict = dict()
        for name in G.nodes:
            if not list( networkx.neighbors(G, name) ): # Если нет соседей
                print(f'''имя свободной GG точки {G.nodes[name]['text']}''')
                free_dict[name] = GG.nodes[name]['embedding']
        # для каждой свобожной точки получаем
        # список пар "имя-трен-точки: расстояние"
        print(f'free_dict {free_dict.keys()}')
        print(f'tren_dict {tren_dict.keys()}')
        for free_name in free_dict:
            list_of_distances = [] # [[name, distance], [name, distance]]...
            for train_name in tren_dict:
                emb_1 = free_dict[free_name]; emb_1 = torch.tensor(data=emb_1)
                emb_2 = tren_dict[train_name]; emb_2 = torch.tensor(data=emb_2)
                d = model(emb_1, emb_2); d = float(d)
                # print(free_name, train_name, d)
                list_of_distances.append([train_name, d])
            list_of_distances.sort(key = lambda x:x[1])
            print('FREE DOT NAME:', free_name, GG.nodes[free_name]['text'])
            print('DISTANCES:')
            for item in list_of_distances:
                print(item, GG.nodes[item[0]]['text'])


if __name__ == '__main__':
    print('Тут будут тесты')