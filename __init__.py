from transformers import BartTokenizer, BartForConditionalGeneration

# Загрузка токенизатора и модели
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

# Сохранение в локальную папку
tokenizer.save_pretrained('./my_bart_model')
model.save_pretrained('./my_bart_model')