import matplotlib.pyplot as plt
from collections import Counter

def count_letters_frequency(text):
    text = text.lower()
    isv_letters = 'o a e t i n j s l v r d k m u y ě p g b č z ų ž h ę š å c f ŕ ć ń è ė ȯ ò ś đ ź t́ ť d́ ď ĺ ľ ј'.split(' ')
    text = [char for char in text if (char in isv_letters)]
    frequencies = Counter(text)
    frequencies = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
    
    letters = [ i[0] for i in frequencies ]
    counts = [ i[1] for i in frequencies ]
    counts = [ i / sum(counts)*100 for i in counts]
    
    plt.bar(letters, counts)
    plt.xlabel('Litery')
    plt.ylabel('Čęstotnosť v percentah %')
    plt.title('Čęstotnosť uživańja liter v tekstu (percenty %)')

    for i, (count) in enumerate(counts):
        plt.annotate(f"{ round(count, 2) }", (i, count), ha='center', va='bottom', fontsize=8)
        
    plt.show() 

with open("isv.txt", 'r', encoding="UTF-8") as file:
    text = file.read()
    text = file.lower()

len(text) 
set(text)


import isv_tools as isv 
text_standard = isv.transliteracija(text, "isv_to_standard")

count_letters_frequency(text)
count_letters_frequency(text_standard)


