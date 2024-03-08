
import subprocess
class text_buffer_interface():
    # text:str, color:tuple =  text_buffer_interface.open()
    '''Файл каждый раз используется один и тот же
        Файл является временным интерфейсом
        При клике по полю при активированной кнопке "добавить ноду"
        открывается файл с разметкой для текста и цвета.
        После закрытия файла создание ноды завершается:
        текст добавляется в поле "текст", увет в поле "цвет"
        файл очищается от текста'''
    def __init__(self):
        self.notepadplusplus_path = r"C:/Program Files/Notepad++/Notepad++.exe"
        self.interface_editor = 'C:/Users/axnm/PycharmProjects/colors_emb/nodes_as_files/test.txt'
    def open(self):
        template = '== text here ==\n\n== color here=='
        with open(self.interface_editor, mode="w", encoding='utf8') as file:
            file.write(template)

        process = subprocess.Popen([self.notepadplusplus_path, self.interface_editor])
        result = process.wait()
        # print(result)
        if result == 0:
            with open(self.interface_editor, mode="r", encoding='utf8') as file:
                t = file.read()
            # print(t)
        start_index_text = t.find('== text here ==\n') + len('== text here ==\n')
        end_index_text = t.find('\n== color here==')
        start_index_color = t.find('\n== color here==\n') + len('\n== color here==\n')

        return t[start_index_text:end_index_text], eval(t[start_index_color:])

if __name__ == '__main__':
    inter = text_buffer_interface()
    result = inter.open()
    print(result)
    print(type(result[1]))