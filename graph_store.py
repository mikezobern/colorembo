import networkx
import pickle

class Store():
    def __init__(self, validation = False):
        # G = networkx.Graph()
        self.validation = validation
        if not validation:
            self.directory_path = "C:/Users/axnm/PycharmProjects/colors_emb/networkx_shit/palitres/multilan series"
            self.filename = "en_ru_fr_ger_ita.pkl"
            self.file_path = f"{self.directory_path}/{self.filename}"
        else:
            self.directory_path = "C:/Users/axnm/PycharmProjects/colors_emb/networkx_shit/palitres/test_palitres"
            self.filename = "the_bigger_test_base.pkl"
            self.file_path = f"{self.directory_path}/{self.filename}"

    def get(self):
        # Load the instance from the file
        validation = self.validation
        with open(self.file_path, 'rb') as file:
            loaded_instance = pickle.load(file)
        if 1 or not validation:
            print(type(loaded_instance))
            print(f"Instance loaded, валидационный граф: {validation}: {loaded_instance}")
        return loaded_instance

    def dump(self, G):
        # dumping
        with open(self.file_path, 'wb') as file:
            pickle.dump(G, file)
        print(f"Graph stored to {self.file_path}")

