import pickle

class Model_store():
    def __init__(self):
        self.directory_path = "C:/Users/axnm/PycharmProjects/colors_emb/networkx_shit/palitres/multilan series"
        self.filename = "model_en_ru_fr_ger_ita.pkl"
        self.file_path = f"{self.directory_path}/{self.filename}"

    def get(self):
        # Load the instance from the file
        with open(self.file_path, 'rb') as file:
            loaded_instance = pickle.load(file)
        return loaded_instance

    def dump(self, model):
        # dumping
        with open(self.file_path, 'wb') as file:
            pickle.dump(model, file)
        print(f"The model stored to {self.file_path}")

