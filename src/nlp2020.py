# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request, urllib.error
import re
from sudachipy import tokenizer
from sudachipy import dictionary
import collections

tokenizer_obj = dictionary.Dictionary().create()
mode = tokenizer.Tokenizer.SplitMode.B
p = re.compile('\n\s+')

def main():
    url="https://www.anlp.jp/nlp2020/program.html"
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
    papers = soup.find_all("span", class_="title")[6:] # 招待論文除く
    whole_words = []
    whole_bigram = []
    for paper in papers:
        title = p.sub(" ", paper.text)
        words = [m.surface() for m in tokenizer_obj.tokenize(title, mode) if m.part_of_speech()[0] == "名詞"]
        whole_words.extend(words)
        whole_bigram.extend(ngram(words, 2))
    
    c_uni = collections.Counter(whole_words)
    c_bi = collections.Counter(whole_bigram)
    print("unigram")
    print(c_uni.most_common(50))
    print()
    print("bigram")
    print(c_bi.most_common(30))

def ngram(words, n):
    return ["+".join(words[i:i+n]) for i in range(len(words)-1)]
    #return list(zip(*(words[i:] for i in range(n))))
    #return list(zip(*(words[i:] for i in range(n))))

if __name__ == "__main__":
    main()