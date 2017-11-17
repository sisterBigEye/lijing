#-*- coding:utf-8 -*-
import os,base64
from selenium import  webdriver
from bs4 import BeautifulSoup
import time
#暂时访问不了，多了换行符在里面

url = 'http://www.gsxt.gov.cn/%7B5B1uwDp1X3PUHiOhZCvZD_6_ghSjPwkh9zbJMj5wP7UYc5R9TbHI77ACTZ872HttKJUBSIs1lV4F8Ekm0kS7RfhDiDT3mdHlc3I8aRzSGRI3qQ8DXQt6ukBCnXfSaTcKnXtXSCAAODYq0-qOhf3Xpg-1510709952127%7D'

driver = webdriver.Chrome()

driver.get(url)
time.sleep(10)
driver.execute_script("window.scrollBy(0,3000)")
time.sleep(10)
driver.execute_script("window.scrollBy(0,3000)")
time.sleep(5)
driver.execute_script("window.scrollBy(0,3000)")
time.sleep(5)
a=driver.page_source

print a

soup = BeautifulSoup(a)
print soup.prettify()

list = soup.select('li.branchInfo-list a span span img')
print list

href = list[0]['src']#获取src属性值
print href

imgData2 = base64.b64decode(href.replace('data:image/png;base64,',''))
ingimg2 = open('imgout2.png','wb')
ingimg2.write(imgData2)
ingimg2.close()
# ingstr = "iVBORw0KGgoAAAANSUhEUgAAAJEAAAANCAYAAACpfIwbAAAEEklEQVR42u1YQWScQRT+rbUiVqiItWqFPVTUilAreqgIsSoqeokVUREhKnqI6qUqqir0EFWRS+QQK2IvK6oqQkVVVYWoiKgqlUNURMghasUK6Zv4JibPzPwz+0sj9PGx/857/7x573szb/4gOC+DhAphiTAe6KWJMEO4FZglTZgj5OvQuUNYJLwjPCc0ePoQ1X4YftnWNwidDs3YG0vscrBTMeqZA+HfmOH901i/SS+POdvZ/1nCS8wp4lYmPCLEfWM7SdjDxA8JuwiIlFbCBOGAcELosQR5FjpFT50CoUZ4SnhA2EFAXX2Iai+khLGKwe8Y3it07muSVANaNLb9hD8WEoXlQPq3ZPDtkDBi0EvjfXMaUgp/PxGewZ95rDHpEdvTCY6hKKUb/6XxLCp3DTo2&#10;EnXA2aqFRCadLVSElC7MddPRh6j2MvhbWHtGMy4C+BPjnEQzqOJdwy4yRFi27MxhOaiXRI2Edc3c&#10;vYjDiKFY4h6xDfrwR4y9qIbqCZStK2lJgLDfRKAPDSQy6bTivfyIOEK1hPkQ1V5NUhlBm9SMf0M1&#10;8p0ojvWIeE1hjVyeWHY4lxzUS6IKSJRk+j+w64SJS2zPWJVVFBKogmFmaEuACPoHZUFFDx1TEL/i&#10;6AvzIao9J5HY1vcRB7UnqOKo4iSSRRFDz6ELuvDjC3TFulOayg7LgS+JXuDoSTHdNszX60Aip9iK&#10;wW0kN4sJy6iCEccEdKPXuG4hkU2niPm4vNec4zofotpzEsXRn6g9y1vCaySXk2iVzbOJRleVcSRW&#10;4Dcqud8zByUQ60iDE0aibUPvJuQexlosjX/eN7aCmRt4sTB4jIQPOiSgFVXbx6qi6KHTj+BwWXYk&#10;QVR7TqIAVbzBtvQbGhJl8FzAWAJH3oGmetXCLSm7l2sOhM1n+M5R1exEFRA2ZeiH2pT/2mFXYpce&#10;n9iene2yqRKGnQ4JWEfVqiyuoTqnHXXkovi1cQfBDPMhqr2ORCn42IU+Z0U5ZlQSTeBZhwHLMZGD&#10;Tt4jB77HWQNiz3sieSQPGd6lksgntudkFEqBQwJe4WaiooagTznqNGpuPCnMddvBh6j2OhIFaDwX&#10;sYt2GUj0C+tLMKwq/Z9OejRHSlgO6mms0yhgfjsTvn03fEtTSeQc25yyrRYQtAFHEpkWVPTUWUAv&#10;0QxfFnAld/Uhqr2ORB3Q3WINryRRN37nDFd69VNBQUlYFje9Fc8c1PudqBN90yz7yLgHP9Sj+K7m&#10;G55TbMtKw7aPj13BPybRNcJHxY81pQl38SGqvY5EAT7EjRlING+4zku9Ko47edU+xgfHYzw3e+ag&#10;XhLJG+QJO4Iyil/yCD7C7pupI7anwU0Fly9NcPqy7C9SktgVEpbxy8hBDPMmr3Bs/8tVlb86KNo2&#10;gQyUkAAAAABJRU5ErkJggg=="
#
# leniystr = "iVBORw0KGgoAAAANSUhEUgAAACwAAAAOCAYAAABU4P48AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAAGYktHRAD/AP8A/6C9p5MAAAF6SURBVEhL1ZY9coMwEIWfchZIkckJxAmAhoojiNJu3KV0lwZK+xRU6ATmBJkUEXdRVj8MmGFsk9ge+5vReFlb2of0diymCTwRL0CHKmJgjKGQPnszJAqqw1iEqvOphZDgexJjRweq9QGrwKcWcmfB/+cCwf0xDiMan2dXIZp870ZBM6ecsIQs7Lzx2rLwa428ekawKZBgTxEvFbQqwSlu1+G830VDx61Qmh/RrO0So8YZBH2060//ohK1KUyILHYBcVqwrK1YgxHJwjVa//z1MxUj0OzMwgFe311mGTEyo5gq1kZxX5uX2Ax6L/QwTVK2WYZxmHYNf0Pow78SO8XYk2Lpt5fnKW3BwGWC228oH8756mrEG2enfYLEbS/y9HhjTgvuF6DDSaIKHTXYdsZX1yNAmtuCDp5jovfcDgdYHTQa1w0IrYc5SqVh7XoDgjS3jW0QH6sjO1jMX/NDoUpNgum6IHTjU2MeSLDSZD9zr7FDzKklnuzyA/wCcpDKoLig94YAAAAASUVORK5CYII="
# # imgData = base64.b64decode(leniystr)
# ingimg = open('imgout.png','wb')
# ingimg.write(imgData)
# ingimg.close()
# ingstr=ingstr.replace('&#10;','')
# imgData1 = base64.b64decode(ingstr)
# ingimg1 = open('imgout1.png','wb')
# ingimg1.write(imgData1)
# ingimg1.close()
driver.close()