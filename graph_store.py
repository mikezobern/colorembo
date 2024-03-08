import networkx
import pickle

class Store():
    def __init__(self):
        # G = networkx.Graph()
        self.directory_path = "C:/Users/axnm/PycharmProjects/colors_emb/networkx_shit"
        self.filename = "2902240437.pkl"
        self.file_path = f"{self.directory_path}/{self.filename}"

    def get(self):
        # Load the instance from the file
        with open(self.file_path, 'rb') as file:
            loaded_instance = pickle.load(file)
        print(type(loaded_instance))
        print(f"Instance loaded: {loaded_instance}")
        return loaded_instance

    def dump(self, G):
        # dumping
        with open(self.file_path, 'wb') as file:
            pickle.dump(G, file)
        print(f"Graph stored to {self.file_path}")



if __name__ == '__main__':
    store = Store()
    G = store.get()
    print(type(G))
    '''
    G = networkx.Graph()
    G.add_node('1',
                    position = (120, 120),
                    dragged = False,
                    fixed = True,
                    highlight = False,
                    text = 'Test node 1!',
                    color = (255,250,150))

    G.add_node('2',
                    position = (220, 230),
                    dragged = False,
                    fixed = True,
                    highlight = False,
                    text = 'Test node 2!!',
                    color = (255,250,150))

    G.add_node('3',
                    position=(500, 330),
                    dragged=False,
                    fixed=True,
                    highlight = False,
                    text = 'Test node 3!!',
                    color = (255,250,150))
    G.add_edge('1','2')
    G.add_edge('1', '3')
    G.add_edge('2', '3')

    store.dump(G)
    print(store.get())
    '''