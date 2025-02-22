import asyncio
import hashlib
from transformers import BartTokenizer, BartForConditionalGeneration


MAX_LENGTH_SUM = 40
MIN_LENGTH_SUM = 5



#--------------------------------------Модели для сокращения текста--------------------------------------------
# Для корректной работы необходимо наличие immediately_summary(входной текст) -> выходное сокращение


# add some new models

class ModelV1:
    def __init__(self):
        self._tokenizer = BartTokenizer.from_pretrained("./my_bart_model")
        self._model = BartForConditionalGeneration.from_pretrained("./my_bart_model")
        self._max_length = MAX_LENGTH_SUM
        self._min_length = MIN_LENGTH_SUM


    def set_length(self, max_length:int=MAX_LENGTH_SUM, min_length:int=MIN_LENGTH_SUM):
        self._max_length = max_length
        self._min_length = min_length
        return None

    # Для добавления новых параметров в будущем
    """
    def set_data(self, **kwargs):
        pass
        return None
    """

    async def immediately_summary(self, input_text:str) -> str:
        inputs = self._tokenizer([input_text], return_tensors="pt")

        summary_ids = self._model.generate(
            inputs["input_ids"],
            max_length=self._max_length,
            min_length=self._min_length,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True,
        )

        summary = self._tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary


class MovelV2:
    def __init__(self):
        pass
    
    
    async def immediately_summary(self, input_text:str) -> str:
        pass
        return input_text
    # TODO Add workflow




# Создание уникальных id на основе входящего текста
# Нужда для реализации Хэш-таблицы (словаря с уникальными ключами для каждого значения)
def generate_unique_id(input_string):
    encoded_input = input_string.encode()
    sha256_hash = hashlib.sha256()
    sha256_hash.update(encoded_input)
    return sha256_hash.hexdigest()




#----------------------------------------------------------------------------------------------------------



# Функция для выбора модели.
# Добавляет в выбранный класс необходимы функции для работы с очередью
def Use_model(ver=None):
    # Можно добавить новые версии для других моделей

    if ver == "V1":
        Parent = ModelV1    # Родитель, которому будут добавлены функции
    elif ver == "V2":
        Parent = MovelV2
    else:
        raise ValueError("Unexpected model")


    class Model(Parent):
        def __init__(self):
            super().__init__()
            self.queue = asyncio.Queue()    # Связный список для работы с запросами обработки
            self.summaries = {}             # Словарь/хеш-таблица для хранения результатов обработки

        async def update(self):  #
            # функция обработки одного запроса из очереди

            try:
                unique_id, data = await self.queue.get()    # Взятие значений с удалением в очереди                     # TODO: 2) Добавить защиту от прерывания, чтобы знаечния удалялись только после обработки
                summary = await self.immediately_summary(input_text=data)   # Обработка текста нейросетью
                self.summaries[unique_id] = summary     # Сохранение результата в словаре с обработанными значениями
            except Exception as e:
                print(f"Error during update: {e}")


        async def add_to_queue(self, data:str="Empty") -> str:
            # Добавление текста в связный список запросов с генерацией уникального ID для каждого текста

            unique_id = generate_unique_id(data)
            await self.queue.put((unique_id, data))
            return unique_id


        async def find_summary_by_id(self, unique_id:str) -> (bool, str):
            # Поиск результата в словаре обработанных значений

            summary = self.summaries.get(unique_id)
            if summary:
                return True, summary
            return False, "Empty"          # не нашли


    return Model()     # Возвращаем "обёрнутую" модель для работы
