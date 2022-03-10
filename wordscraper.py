import requests
from bs4 import BeautifulSoup as bs
import enchant

#word generator, gets list of words that are possible by checking against us dictionary from a scrabble website
for i in range(4,19):
    r = requests.get(f'https://www.litscape.com/words/length/{str(i)}_letters/{str(i)}_letter_words.html')
    soup = bs(r.content, 'html.parser')
    div = soup.find('div', {'id': 'wordlistdisplay'})

    dictionary = enchant.Dict('en_US')

    list = div.text.split(" ")
    new_list = []
    for item in list:
        if dictionary.check(item):
            new_item = item + "\n"
            new_list.append(new_item)
    f = open(f'words/{i}.txt', "w+")
    f.writelines(new_list)
