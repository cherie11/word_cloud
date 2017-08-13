from nltk.corpus import stopwords
import nltk
import matplotlib.pyplot as plt 
import numpy as np
from os import path
import pandas as pd
import re
import requests
from scipy.misc import imread 
import time
from wordcloud import WordCloud,ImageColorGenerator


def get_news(PAGE_num):
	pattern= re.compile('.htm" target="_blank">(.*?)</a></h4>\n\n<b>(.*)</b></span></div>')
	url="http://www.chinadaily.com.cn/opinion/topdiscusstion"
	tail=".html"
	with open('subjects.txt','w',encoding='utf-8') as f:
		list1=['_'+str(i) for i in range(2,PAGE_num+1)]
		list1.insert(0,'')
		for i in range(len(list1)):
			r=requests.get(url+str(list1[i])+tail)
			data=r.text
			res=re.findall(pattern,data)
			for ele in res:
				f.write(ele[0]+'\n')
			print('GET PAGE %d'%i)
			time.sleep(5)
		f.close()

def process_word():
	pos= ['NN','NNS','NNP','NNPS']#choose nouns
	news_kword=""
	with open('subjects.txt','r',encoding='utf-8') as f:
		news_text = f.readlines()
	for text in news_text:
		news_list=nltk.word_tokenize(text)
		#remove the stopword
		filtered=[w for w in news_list if w not in stopwords.words('english')]
		re_filtered=nltk.pos_tag(filtered)
		tmp=[word for word,flag in re_filtered if flag in pos]
		news_kword+= r' '.join(tmp)   #防止字符转义
	return news_kword


if __name__ == "__main__":
	get_news(10)    #pass the amount of page
	d = path.dirname('.')
	#d = path.dirname(__file__)
	text = process_word()
	# read the mask / color image
	back_pic = imread(path.join(d, "./1.jpg"))
	wc = WordCloud( font_path="./cabin-sketch.bold.ttf",
	                background_color="white", #backgroud color
	                max_words=200,#max_amount of words
	                mask=back_pic,#set background
	                max_font_size=100, 
	                random_state=42,
	                )
	
	wc.generate(text)
	image_colors = ImageColorGenerator(back_pic)
	plt.figure()
	#show the pic
	plt.imshow(wc)
	plt.axis("off")
	plt.show()

