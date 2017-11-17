from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import string
from collections import OrderedDict
# def ngrams(input,n):
#     input = input.split(' ')
#     output = []
#     for i in range(len(input)-n+1):
#         output.append(input[i:i+n])
#     return output
# def ngrams(input,n):
#     input = re.sub('\n+'," ",input)
#     input = re.sub(' +'," ",input)
#     input = bytes(input,"UTF-8")
#     input = input.decode("ascii","ignore")
#     print(input)
#     input = input.split(' ')
#     output = []
#     for i in range(len(input)-n+1):
#         output.append(input[i:i+n])
#         output.append(input[i:i+n])
#     return output

def cleanInput(input):
    input = re.sub('\n+'," ",input)
    input = re.sub('\[[0-9]*\]]','',input)
    input = re.sub(' +'," ",input)
    input = bytes(input,"UTF-8")
    input = input.decode("ascii","ignore")
    input = input.upper()
    cleanInput = []
    input = input.split(' ')
    for item in input:
        item = item.strip(string.punctuation)
        if len(item) > 1 or (item.lower()=='a' or item.lower() =='i'):
            cleanInput.append(item)
    return cleanInput

# def ngrams(input,n):
#     input = cleanInput(input)
#     print (input)
#     output = []
#     for i in range(len(input)-n+1):
#         output.append(input[i:i+n])
#     return output

def getNgrams(input,n):
    input = cleanInput(input)
    output = dict()
    for i in range(len(input)-n+1):
        newNGram = ' '.join(input[i:i+n])
        if newNGram in output:
            output[newNGram] +=1
        else:
            output[newNGram] =1
    print (output)
    return output



html = urlopen("http://en.wikipedia.org/wiki/Python_(programming_language)")
bsObj = BeautifulSoup(html)
content = bsObj.find("div",{"id":"mw-content-text"}).get_text()
print (content)

ngrams = getNgrams(content,2)
ngrams = OrderedDict(sorted(ngrams.items(),key = lambda t : t[1],reverse = True))
print (ngrams)
print("now_2-grams count is" +str(len(ngrams)))