# Черновик
class Node:

    def __init__(self, data = None, id = None):
        self.id = id
        self.data = data
        self.next = None



class Linked_list:

    def __init__(self):
        self.head = None
        self.len = 0

    def get_length_through_check(self):
        if self.head is None:
            return 0

        counter = 0
        lastNode = self.head
        while lastNode is not None:
            lastNode = lastNode.next
            counter+=1

        return counter


    def get_length(self):
        return self.len


    def add_Node_to_end(self, data = None, id = None):
        newNode = Node(data=data, id=id)
        self.len += 1
        if self.head is None:
            self.head = newNode
            return

        lastNode = self.head

        while lastNode.next is not None:
            lastNode = lastNode.next

        lastNode.next = newNode
        return


    def get_first_Node(self, is_delete = False):
        if self.head is None:
            return False, 0, 0

        data = self.head.data
        data = self.head.data

        if is_delete:
            self.head = self.head.next
            self.len -= 1

        return True, id, data


def test():
    ln = Linked_list()

    print('init_len(0) = ', ln.get_length())
    print('init_head(False) = ', ln.get_first_Node())

    ln.add_Node_to_end(data='alpha')

    print('1_len(1) = ', ln.get_length())
    print('1_head(alpha) = ', ln.get_first_Node())

    ln.add_Node_to_end('beta')

    print('2_len(2) = ', ln.get_length())
    print('2_head(alpha) = ', ln.get_first_Node(is_delete=True))

    print('2d_len(1) = ', ln.get_length())
    print('2d_head(beta) = ', ln.get_first_Node(is_delete=True))

    print('3d_len(0) = ', ln.get_length())
    print('3d_head(False = ', ln.get_first_Node(is_delete=True))

#test()

#---------------------------------My_models

import hashlib
from transformers import BartTokenizer, BartForConditionalGeneration
from Narabotki import Linked_list
import asyncio


MAX_LENGTH_SUM = 40
MIN_LENGTH_SUM = 5

class ModelV1:
    def __init__(self):
        self._tokenizer = BartTokenizer.from_pretrained('./my_bart_model')
        self._model = BartForConditionalGeneration.from_pretrained('./my_bart_model')
        self.set_length()
        return

    def set_length(self, max_length = MAX_LENGTH_SUM, min_length = MIN_LENGTH_SUM):
        self._max_length = max_length
        self._min_length = min_length
        return

    async def immediately_summary(self, input_text):
        inputs = self._tokenizer([input_text],
                                   return_tensors='pt')

        summary_ids = self._model.generate(inputs['input_ids'],
                                     max_length = 150, min_length = 20,
                                     length_penalty = 2.0, num_beams = 4,
                                     early_stopping = True)

        summary = self._tokenizer.decode(summary_ids[0],
                                   skip_special_tokens=True)

        return summary



def generate_unique_id(input_string):
    # Encode the input string
    encoded_input = input_string.encode()
    # Create a SHA-256 hash object
    sha256_hash = hashlib.sha256()
    # Update the hash object with the bytes-like object
    sha256_hash.update(encoded_input)
    # Return the hexadecimal representation of the hash
    return sha256_hash.hexdigest()



def Use_model(ver = None):
    if ver == "V1":
        Parent = ModelV1
    else:
        raise "Unexpected model"

    class Model(Parent):

        def __init__(self):

            Parent.__init__(self)
            self.Queue_list = Linked_list()
            self.Answer_list = Linked_list()

        def update(self):  # create summary of data
            status, unique_id, data = self.Queue_list.get_first_Node(is_delete=True)
            if not status:
                return False, 0

            summary = self.immediately_summary(input_text=data)
            self.Answer_list.add_Node_to_end(data=summary, id=unique_id)
            return True, unique_id

        def add_to_Queue_list(self, data=None):
            unique_id = generate_unique_id(data)
            self.Queue_list.add_Node_to_end(data=data, id=unique_id)
            return unique_id

        def get_first_response(self, is_delete=True):
            status, unique_id, data = self.Answer_list.get_first_Node(is_delete=is_delete)
            if status:
                return True, unique_id, data

            return False, 0, 0

    return Model()





"""
    print('Commands:',
          '\n - "R" to read a text and add to the queue.',
          '\n - "W" to write summary by unique ID.',
          '\n - "STOP" to stop the update worker.',
          '\n - "START" to restart the update worker.',
          '\n - "EXIT" to terminate the program.')
"""

#---------------------------------for file reading-----------------------------------
#
# import aiofiles
#     async with aiofiles.open("inputs.txt", "r", encoding="UTF8") as file:
#     texts = await file.readlines()