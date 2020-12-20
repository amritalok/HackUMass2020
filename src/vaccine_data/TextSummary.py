import torch
import json
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config
model = T5ForConditionalGeneration.from_pretrained('t5-small')
tokenizer = T5Tokenizer.from_pretrained('t5-small')
device = torch.device('cpu')
review = "On October 26th, my wife and two kids went to get hair cuts and colors.  The stylist (also the manager) was very polite and nice.  My daughter has wanted to get purple tips for a long time, so we indulged her.  My wife got her haircut and dyed and my other daughter just got a hair cut.  Everything looked great and everyone loved their hair.  It was a little expensive ($353.00) with the haircuts, tips bleached and dyed, a color, shampoo and conditioner for dyed hair, and a tip, but we loved the way everyone looked.Four days go by and my daughters tips were starting to lighten.  We didn't think much of it, because the color will mellow out after a few days.  By day nine, her tips had faded to a light blue.  We called the shop that evening to ask if they could do anything about her tips.  We were told that they didn't use a permanent or semi permanent dye, but a fashion dye which only lasts a couple of weeks. When we went to the shop, we asked for a permanent dye, due to the costs being so high.  We were told that what they were using was a permanent dye.  I told the stylist on the phone this and she said supercuts only has a 7 day color guarantee, but we could come in and they would dye her hair again for the same cost.  I asked to speak to the manager and was told she wasn't in the store at the time, but they would call me bac Updated 11/30/20. After talking to the manager and the owner, they made this right and fixed my daughter's hair.  We're very pleased with the results, and I'd like to thank Victoria (the manager) and the owner for their quick and courteous service.  While I was there I also got a quick buzz from one of the other stylist and she did a great job."
preprocess_text = review.strip().replace('\n','')
t5_prepared_Text = "summarize: " + preprocess_text
print ('original text preprocessed: \n', preprocess_text)
tokenized_text = tokenizer.encode(t5_prepared_Text, return_tensors='pt').to(device)
# summmarize
summary_ids = model.generate(tokenized_text,
                                    num_beams=4,
                                    no_repeat_ngram_size=2,
                                    min_length=30,
                                    max_length=100,
                                    early_stopping=True)
output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
print ('\n\nSummarized text: \n',output)