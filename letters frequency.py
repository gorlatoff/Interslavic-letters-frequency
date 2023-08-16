import matplotlib.pyplot as plt
from collections import Counter

isv_letters_lat = 'o a e t i n j s l v r d k m u y ě p g b č z ų ž h ę š å c f ŕ ć ń è ė ȯ ò ś đ ź t́ ť d́ ď ĺ ľ ј'.split(' ')
isv_letters_cyr = 'о а е т и н ј c л в р д к м у ы є п г б ч з ж х ц ф ш њ љ'.split(' ')

def count_letters_frequency(text, alphabet, title):
    text = [char for char in text if (char in alphabet)]
    frequencies = Counter(text)
    frequencies = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
    
    letters = [ i[0] for i in frequencies ]
    counts = [ i[1] for i in frequencies ]
    counts = [ i / sum(counts)*100 for i in counts]
 
    plt.bar(letters, counts)
    plt.xlabel('Litery')
    plt.ylabel('Čęstotnosť v percentah %')
    plt.title(title)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    
    for i, (count) in enumerate(counts):
        plt.annotate(f"{ round(count, 2) }", (i, count), ha='center', va='bottom', fontsize=7)

    plt.show() 


with open("isv.txt", 'r', encoding="UTF-8") as file:
    text = file.read()
    text = text.lower()

import isv_tools as isv 
text_standard_lat = isv.transliteracija(text, "isv_to_standard")
text_standard_cyr = isv.transliteracija(text, 'isv_to_cyrillic')

count_letters_frequency(text, isv_letters_lat, 'Čęstotnosť uživańja liter v tekstu, etimologičny alfabet')
count_letters_frequency(text_standard_lat, isv_letters_lat, 'Čęstotnosť uživańja liter v tekstu, latinica')
count_letters_frequency(text_standard_cyr, isv_letters_cyr, 'Čęstotnosť uživańja liter v tekstu, kirilica')