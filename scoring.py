"""Модуль принимает на вход пайторчевую модель, обращается в GGG --- и возвращает скор."""
import networkx
import torch.nn


class Score():
    '''GGG -- Networkx-граф, который служит как проверочная палитра.
    Проверочная палитра нужна, чтобы оценивать качество модели.
    Связанные точки на проверочной палитре рассматриваются как опорные,
    или якорные -- это, например, основные цвета.
    Расположенная на проверочной палитре точка соответствует ближайшей якорной.
    Класс составляет два словаря: проверочный и предсказанный.
    В обоих свободным точкам сопоставлены якорные.
    Проверочный словарь составляется на основе проверочной палитры.
    Предсказанный словарь же рассчитывается на основе можели,
    которую функция gimme_score принимает в качестве аргумента.
    '''
    def __init__(self):
        pass
        # print('Импортировал скор')
    def gimme_score(self, GGG: networkx.Graph, model: torch.nn.Module):
        ankers = ['red', 'orange', 'yellow', 'green', 'blue', 'violet']
        # получить GGG_test_dict =  {'Текст свободной точки':'Текст ближайшейанкерной точки'}
        GGG_test_dict = dict()
        ankers_coordinates = {GGG.nodes[dot_name]['text']:GGG.nodes[dot_name]['position'] for dot_name in GGG.nodes if GGG.nodes[dot_name]['text'] in ankers}
        for dot_name in GGG.nodes:
            if not list(GGG.neighbors(dot_name)): # свободная точка
                free_dot_text = GGG.nodes[dot_name]['text']
                free_dot_pos = GGG.nodes[dot_name]['position']
                list_of_distances = []
                for anker_text in ankers_coordinates:
                    anker_position = ankers_coordinates[anker_text]
                    d = (free_dot_pos[0] - anker_position[0])**2 + (free_dot_pos[1] - anker_position[1])**2; d = d**0.5
                    list_of_distances.append([anker_text, d])
                list_of_distances = sorted(list_of_distances, key = lambda x:x[1])
                GGG_test_dict[free_dot_text] = list_of_distances[0][0]
        # print(GGG_test_dict)
        # Получить model_predicted_dict = {'Текст свободной точки':'Текст анкерной точки'}
        # Перебираем все свободные точки

        model_predicted_dict = dict()
        ankers_embeddings = {GGG.nodes[dot_name]['text']:GGG.nodes[dot_name]['embedding'] for dot_name in GGG.nodes if GGG.nodes[dot_name]['text'] in ankers}
        for dot_name in GGG.nodes:
            if not list(GGG.neighbors(dot_name)): # свободная точка
                free_dot_text = GGG.nodes[dot_name]['text']
                free_dot_emb = GGG.nodes[dot_name]['embedding']; free_dot_emb = torch.tensor(data = free_dot_emb)
                list_of_distances = []
                for anker_text in ankers_coordinates:
                    anker_emb = ankers_embeddings[anker_text]; anker_emb = torch.tensor(data = anker_emb)
                    d = model(free_dot_emb,anker_emb); d = float(d)
                    list_of_distances.append([anker_text, d])
                list_of_distances = sorted(list_of_distances, key=lambda x: x[1])
                model_predicted_dict[free_dot_text] = list_of_distances[0][0]
        # print(model_predicted_dict)
        # Сравнение проверочных данных и данных на основе модели:
        numerator = 0
        denominator = 0
        for key in GGG_test_dict:
            denominator+=1
            if GGG_test_dict[key] == model_predicted_dict[key]:
                numerator+=1
        # print('Score, рассчитанный на основе тестового графа GGG', numerator/denominator)
        return numerator/denominator


if __name__ == '__main__':
    from graph_store import Store; GGG = Store().get()
    from mrsc import mrsc; model = mrsc()
    Score().gimme_score(GGG,model)

