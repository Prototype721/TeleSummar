import asyncio
import hashlib
from transformers import BartTokenizer, BartForConditionalGeneration

MAX_LENGTH_SUM = 40
MIN_LENGTH_SUM = 5

class ModelV1:
    def __init__(self):
        self._tokenizer = BartTokenizer.from_pretrained("./my_bart_model")
        self._model = BartForConditionalGeneration.from_pretrained("./my_bart_model")
        self.set_length()

    def set_length(self, max_length=MAX_LENGTH_SUM, min_length=MIN_LENGTH_SUM):
        self._max_length = max_length
        self._min_length = min_length

    def set_data(self, **kwargs): # for adding other data
        pass

    async def immediately_summary(self, input_text):
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


def generate_unique_id(input_string):
    encoded_input = input_string.encode()
    sha256_hash = hashlib.sha256()
    sha256_hash.update(encoded_input)
    return sha256_hash.hexdigest()


def Use_model(ver=None):
    if ver == "V1":
        Parent = ModelV1
    else:
        raise ValueError("Unexpected model")

    class Model(Parent):
        def __init__(self):
            super().__init__()
            self.queue = asyncio.Queue()
            self.summaries = {}  # Dictionary to store summaries by unique ID

        async def update(self):  # Create summary of data
            try:
                unique_id, data = await self.queue.get() # deletes data after requesting
                summary = await self.immediately_summary(input_text=data)
                self.summaries[unique_id] = summary  # Store summary in dictionary
            except Exception as e:
                print(f"Error during update: {e}")


        async def add_to_queue(self, data=None):
            unique_id = generate_unique_id(data)
            await self.queue.put((unique_id, data))
            return unique_id


        async def find_summary_by_id(self, unique_id):
            summary = self.summaries.get(unique_id)
            if summary:
                return True, summary
            return False, None

    return Model()
