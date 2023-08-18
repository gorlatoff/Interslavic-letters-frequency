import plotly.graph_objects as go
from collections import Counter

isv_letters_lat = 'o a e t i n j s l v r d k m u y ě p g b č z ų ž h ę š å c f ŕ ć ń è ė ȯ ò ś đ ź t́ ť d́ ď ĺ ľ ј'.split(' ')
isv_letters_cyr = 'о а е т и н ј c л в р д к м у ы є п г б ч з ж х ц ф ш њ љ'.split(' ')

import plotly.io as pio
pio.templates.default = "plotly_dark"


def count_letters_frequency(text, alphabet, title):
    text = [char for char in text if (char in alphabet)]
    frequencies = Counter(text)
    frequencies = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
  
    letters = [ i[0] for i in frequencies ]
    counts = [ i[1] for i in frequencies ]
    counts = [ i / sum(counts) * 100 for i in counts]
    
    fig = go.Figure(go.Bar(
        x=letters,
        y=counts,
        text=[f"{round(count, 2)}" for count in counts], #anotacije
        textposition='outside',
        textfont=dict( size=13),           
    ))

    fig.update_layout(
        title=dict(text=title, font=dict(size=24), x=0.5, y=0.85, xref="paper"),
        yaxis_title='procenty %',
        xaxis_title='Litery',
        font=dict(size=22),
        yaxis={'visible': True, 'showticklabels': False}
    )
   
    fig.show()


with open("isv.txt", 'r', encoding="UTF-8") as file:
    text = file.read()
    text = text.lower()

import isv_tools as isv 
text_standard_lat = isv.transliteracija(text, "isv_to_standard")
text_standard_cyr = isv.transliteracija(text, 'isv_to_cyrillic')

count_letters_frequency(text, isv_letters_lat, 'Čęstotnosť uživańja liter v tekstu, etimologičny alfabet')
count_letters_frequency(text_standard_lat, isv_letters_lat, 'Čęstotnosť uživańja liter v tekstu, latinica')
count_letters_frequency(text_standard_cyr, isv_letters_cyr, 'Čęstotnosť uživańja liter v tekstu, kirilica')


















from collections import Counter

with open("isv.txt", 'r', encoding="UTF-8") as file:
    text = file.read()
    text = text.lower()

from nltk import ngrams
frequencies = ngrams(text, 2)
frequencies = [''.join(ngram) for ngram in frequencies]
frequencies = [ngram for ngram in frequencies if ngram.isalpha()]
frequencies = Counter(frequencies)
frequencies = sorted(frequencies.items(), key=lambda x: x[1], reverse=False)
frequencies = [i for i in frequencies if i[1] > 580]

import pprint
pprint.pprint(frequencies)