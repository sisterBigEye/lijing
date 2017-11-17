#-*-coding:utf-8 -*-
from selenium import webdriver
import time
import re
import MySQLdb
import pandas as pd
import sys
import csv
import codecs

reload(sys)
sys.setdefaultencoding('utf-8')


#把获取基本信息封装在类里，使得访问一次网页可以获得总的信息，不用分几次访问

class getIC_INFO:


    def __init__(self,url,driver):
        self.url=url
        self.drive=driver


    #获取股东信息的函数
    def Shareholder_investment_info(self):

        total=[]
        more=[]
        jitichuzhi=[]#具体出资

        t=['sort_n','sh_name','sh_type','certif_type','certif_num','invest_detail(10K)','social_unique_code']
        # driver[k%len(driver)].get(url[k])

        for h in range(3,8):
            try:
                num = driver.find_element_by_xpath('//*[@id="shareholderInfo_paginate"]/ul/li[%d]/a' %h).text
                # print "页数是："
                # print num
            #num字符数转化成整数
                if int(num)>=1 and int(num)<10:
                    driver.find_element_by_xpath('//*[@id="shareholderInfo_paginate"]/ul/li[%d]/a' %h).click()
                    time.sleep(10)
                else:break
            except:
                break
            #取得所有原始列表数据
            for i in range(1,6):
                result={'sort_n':'null','sh_name':'null','sh_type':'null','certif_type':'null','certif_num':'null','invest_detail(10K)':'null','social_unique_code':'null'}
                for j in range(1,7):
                    try:
                        #多行的情况
                        result[t[j-1]] =driver.find_element_by_xpath('//*[@id="shareholderInfo"]/tbody/tr[%d]/td[%d]'%(i,j)).text
                    except:

                        break
                if result=={'sort_n':'null','sh_name':'null','sh_type':'null','certif_type':'null','certif_num':'null','invest_detail(10K)':'null','social_unique_code':'null'}:break
                result[t[6]]=driver.find_element_by_xpath('/html/body/div[5]/div[4]/div[2]/div[15]/div[2]/div[1]/span[1]/span').text
                total.append(result)
            #向右滚动
            driver.execute_script('window.scrollBy(1000,0)')
            #取出每一行第五个字段中的扰乱符
            for i in range(1,6):
                try:
                    huhao=driver.find_element_by_xpath('//*[@id="shareholderInfo"]/tbody/tr[%d]/td[5]/div[1]'% i).text
                except:
                    try:
                        huhao=driver.find_element_by_xpath('//*[@id="shareholderInfo"]/tbody/tr[%d]/td[5]/span[1]'% i).text
                    except:
                            #非公示项令huhao为空
                            #多行
                        try:
                            driver.find_element_by_xpath('//*[@id="shareholderInfo"]/tbody/tr[%d]/td[5]' %i)
                            huhao=''

                        except:
                            break
                # print "打印每次的符号:"
                # print huhao
                #把提取到的扰乱符追加到列表里
                more.append(huhao)
            #点击详情查看
            for i in range(1,6):
                try:
                    #不能做两次点击，这个扰乱符和前一次点击的结果不一致，导致无法匹配
                    #多行的情况
                    driver.find_element_by_xpath('//*[@id="shareholderInfo"]/tbody/tr[%d]/td[6]/span'%i).click()
                    time.sleep(20)
                    try:
                        #有认缴徼用实徼
                        detail =driver.find_element_by_xpath('//*[@id="shareholders_details"]/div[2]/table[2]/tbody/tr[3]').text
                    except:
                        try:
                            #无认缴徼用实徼
                            detail =driver.find_element_by_xpath('//*[@id="shareholders_details"]/div[2]/table[3]/tbody/tr[3]').text
                        except:
                            #认和实信息都没有
                            detail=''
                    driver.find_element_by_xpath('//*[@id="closeColumn"]/p[1]/img').click()
                    time.sleep(3)
                except:
                    try:
                        driver.find_element_by_xpath('//*[@id="shareholderInfo"]/tbody/tr[%d]/td[6]'%i)
                        detail =''
                    except:
                        break
                jitichuzhi.append(detail)

        # print jitichuzhi
        #从第二行开始，股东出资的3位置要提取中文，5位置要提取数字
        with codecs.open('sii_dicw.csv','a+','utf-8') as csvfile:
            writer=csv.DictWriter(csvfile,fieldnames=t)

            for i in range(len(total)):
                try:
                    (total[i])[t[2]]=''.join(re.findall(ur'[\u4e00-\u9fa5]',(total[i])[t[2]],re.M))
                    #清理注册码中的杂数
                except:
                    pass
                try:
                    #把结果内的扰乱符替换成''
                    (total[i])[t[4]]=(total[i])[t[4]].replace(more[i],'')
                    #按行读取，取出注册号，把\n\t等去掉,非公示项要直接打印出来

                    (total[i])[t[4]] =''.join(re.findall(r'\S+',(total[i])[t[4]],re.M))
                    #详情的查看
                    #重写详情
                    (total[i])[t[5]]=jitichuzhi[i]
                    # print (total[i])[5]
                    # print (total[i])[6]
                except:
                    pass
                writer.writerow(total[i])
            print total
        return total




  #获取营业执照信息
    def business_licence_info(self):
        rowname={u'统一社会信用代码':'social_ucode',u'注册号':'social_ucode',u'类型':'type',u'企业名称':'name',u'名称':'name',u'投资人':'investor',u'经营者':'investor',u'法定代表人':'investor',
        u'登记机关':'reg_oran',u'登记状态':'reg_state',u'经营场所':'place',u'住所':'place',u'经营范围':'scope',u'注册日期':'begin_date',u'成立日期':'begin_date',
        u'核准日期':'pess_date',u'注册资本':'invest_money',u'营业期限自':'run_from_date',u'营业期限至':'run_end_data'}

        #营业执照信息
        name=['social_ucode','type','name','investor','reg_oran','reg_state','place','scope','begin_date','pess_date','invest_money','run_from_date','run_end_data']
        result={'social_ucode':'null','type':'null','name':'null','investor':'null','reg_oran':'null','reg_state':'null','place':'null','scope':'null','begin_date':'null','pess_date':'null','invest_money':'null','run_from_date':'null','run_end_data':'null'}

        info=[]
        with codecs.open('bli_dicw.csv','a+','utf-8') as csvfile:
            writer=csv.DictWriter(csvfile,fieldnames=name)
        #营业执照信息
            for i in range(1,14):
                # result={'social_ucode':'null','type':'null','name':'null','investor':'null','reg_oran':'null','reg_state':'null','place':'null','scope':'null','begin_date':'null','pess_date':'null','invest_money':'null','run_from_date':'null','run_end_data':'null'}

                try:
                    t=driver.find_element_by_xpath('//*[@id="primaryInfo"]/div/div[2]/dl[%d]/dt'%i).text
                    t1=t.replace('：','')
                    print t1
                    if t1 in rowname.keys():
                        print "yes"
                        print rowname[t1]
                        print "no"
                        result[rowname[t1]] = driver.find_element_by_xpath('//*[@id="primaryInfo"]/div/div[2]/dl[%d]/dd'% i).text
                    else:
                        pass
                except:
                    print "hihi"
                    break
            writer.writerow(result)
            info.append(result)
        return info

    #获取主要人员信息
    def Key_person_info(self):


        #职位和URI对照的字典
        zhiweibiao={'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB0AAAAOCAYAAADT0Rc6AAABaUlEQVR42mNgwA7SgNgUiV8OxEoMxAN7II4lRmERENtC2cuBOBzKlgbiL0DMg0VPIhDPxoIPAvE1HHJpyAYsRLII2dIuIH4MFUPGWUCsB8ReWPAEIN6CQ86AkKXyQPwBiP2waNZD0rsJagkMXwLi+2hi27AFLzZLdwNxLdTyHUAsiyNqPqHxk4F4CprYD2IsrYS6jgkqVgDE74DYEYelhHyK1VKQywKwxCky8IHGLxeSmCU0pQYg4SlQByOLgdSIY7OYDYpBhmsh8ZExH5qeLKglyHgvEF9BE7sLTQsoAJQl/gPxayjGx4ZlH0do/KHjhVCLkcXOQVO1G7qln3BE/A+0+ONBCtpwLHgmNOEhi50E4g6ksoBsSxmgrl+Iho8C8Q00sYe4gpccS62B2AUN90HzLrLYNiiNUgSuAeJfSCXOHxzsX1C1RWiO5oOm0HCoT3MIlbvGOIosfNgYzQxQfl4MdVgPjrIaDAC5foW6ShoocQAAAABJRU5ErkJggg==':'监事',

        'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB0AAAAOCAYAAADT0Rc6AAABdklEQVR42qWUMUgDQRBFDwsrsbGwEBEsLIJIOpEgIkgQK7tUV4iQIoiFnYi9hcgVQZBUYmEnInIIIQQLEUFSiIgIIiGlnVVKZ+EffL4TTnHhkezfnZ3d2b8XRX7bMIrUL0L7bVsy4rxJNaNBvBlN6jeh8ZwaNtJwuDVeBoxVs6RzxgqRGvvU3zUu8H/VKCMmsOaQGNcDxriC0R6S3RgfoGd8Gm0sErh0Sn1F44EnxLOWankLctKMAyzojRUo/kvW2zTqovU1aYxJSrjL5wFjsSTNO2nfM9OIcS7cw0Cqz1LcAjawTtRRTtbCnHFNOma0jGEi3N2xaCnKy87XKrScCr3DSD+S9sTebcf6XUq6jPtTTpGYtQ5cXf5v0lDaisMJXgFrDzDmot7pDn4zqliAtW1jhuISnIy5M15F63rlnccHgHnEXaheoriS85yOnKemXogmxGkZiePCjEnZ9CgcWsFJt/K+vVMI+AvTssaQcYYndYircNs3bFSWiVYudnIAAAAASUVORK5CYII=':'董事',

        'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACsAAAAOCAYAAAC2POVFAAAB/0lEQVR42rWVQUSDYRjHJ5MOiUw6TCJJJtltMpmYyQ7pNh12SOwwSbol6dClQ7LDRHaaDpEkySdmpkMS0yFJIpkOHbqlw+xSz5v/x9Pj+fZ+O/Tys33P+z7f+7zP+3+eLxDQxyIRZc9R2PyOBJH1sS5CFC1rgtKQJ0qMZ6LCniuw8TV5HKCkcEU8eszl2L5J4sMjyH6iTBzLiUk4ujjEJnteJ07xf5ZIwceQVigQFx5zUR/BLhHvxAkxoJ1kA0FeEq/gDS+rYXPDmSKJczZvuIc/tznKnjzYbtyWucEnHMxTO0mFHQSizUWY/6eSGanFZptg+4gvok4s2ISexcslRqsPHnNZEawts01LZoc6KOBAL3EkuMG1SPsE85tC4POMIq6d28yaQfiYwvnukD83FSKq0I6L0ea+sDnICO8kMutV5UZeFB3KAssiQdYRQkHxNlNTWlCDBTsDfUrKCJjb7tAlUm2C7cJ+uf8I1kggo3CArsJttyjYaUvrikHfSZtm1/DrksPG3LZCjDG/AjLJuUb74baGDxmME2EcrgWJqSOGxs+pQ2vSHmd+caWt7Sktz1Gy5QabwHyLfTTSmDPymeNOYVG5LgWlql1kq+lDgWSQ2WUfdbKKSjdBbSlfqxCKswUJ/Y5hbNQJI+LFpjgO0dp2IRnbGCW2iR7LOtPygj81EMiFCWOxNQAAAABJRU5ErkJggg==':'董事长',

        'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFUAAAAOCAYAAABevFBuAAAEC0lEQVR42r2YcUScYRzHXzknk8hkMnNkJjkTk5NkYjL3RyaSzEkikzmTyJzM/hhnTjInkiRJZDKZjHPOzElMf0xm4uTkTCIzk/tjtN/L95nv/fY819myh4973+d5n+d9nu/z+/2e33ueZy+jQgfdd6Cu1nJXiNX47C1hWNU1CFMX9LspPLLUx9FmK03CjPefyoSwSBwIGbrPoI6fmYDQixbeC58dbeNCQAiCkHAitFHdsvCa7oPow6VZKKkN6RGOhWuOdT4T1nD9UCg76FbGYfD7jAjfHZT4ZbeFe8Q2dtTcPxU2cX1f6EMfn6iFOeGto823+gQ2ylAU9nG9B2EyigTN14yVFF7QfUGYpXttpcfYRK+K6Hm69w0gDaEXsK4x1Jl5bOI6CGErSgJivhMOwRGsKAeRfN5YQsEWtft8Qn+u266ymDSFC56oq5wLG8K6gw08wyUlPMfifYEaVfsUvLHZ8r4ThCQPos5jnH7oEUR7hajtylINSQhma2un/nqHeDdNKav7ebiLz5lwiutT3JcIm6jBKqIHlagRCFYP48mq+L2M56cd42lRjcHsCl/JaCp0iEEETQZuaWuLKVEvstTyX1pq+RJEXcY4/jy/IQTUwb1LiPWdEGYfIa6aqDW7f4PFjXaww7o+TP26IMgDIo0Jcl2MDpA4JmPwY+FHXOexUNP2E7/TStRBNT4zqEStA1lkDGFYWB6HG5cBvN8PFa8g1Dl+DyGqOS9MDI4iFPwh6lW8lE/cUYofhm24P2cO2oqzFgsv0OFRj000LMBqGrCoLWor47f+H2NqQnlARM2BaQEuS/0irGCdRVyvukQ9UulPzpIaFUnUXrxEY17IdXs4PfvUyZqmkz8NKyhQm839o7A843Y7KsbXwVpN6YfFryFVW0ddyRHHX1Zx/wBtsA5VDZchqu/6QxYWkEVw3S4OPuNudzCpEQiXIpc6p9RoQ81zCRsSxQaYM+EAaZOHMOOL00r55hI8L4q16jNlvUqMZlHjpIXJlFifNh1TJ5UbjEMgrovjK8iUOVgmkycXMRQtuWMLYmleHVQ5bMKYev4KLCqkRPUQA0PwhCnMvUBCsxV3kaXXKuowQmEPGUoS82TjqfjwiKjDYxMLLljqu6lftyXdmrWkYjoW98C6eh2nfxMsIUvWPYk681zGIsA0Fu/B3WchYgpj/bDkzC5R/c35gNCRUx8gF+bU1x2n6JzlFDfcUGM0YnJDsLzHVXZ+BoK21ZBSjSMsJTB2F835DF5gXG8JX02d5H0BHH5PEHKMAfHX2j6yAa6Lw1MGKIaOKu/jg8rwO0sJqW/cWmi1uNUqdjxlC9pUQnBlU5IQzIM1r1jGDjj+jNHxPFzDfx1NsP5qtFr6hR2f3kzkF9n7lseFpaXKAAAAAElFTkSuQmCC':'董事长兼总经理',

        'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADkAAAAOCAYAAACVZ7SQAAACqElEQVR42r2WUYSUURTHx1irh8RKkqzoIVlj7dsaayWykmRfMg9ZSezDyDysXpL00EvWWvMwljWStTIkSdaItVZW1rL2IUkiWaOHLMk+jQx1Tn43Z447830zDx1+Zu65937f/d97zrlfJtNui8IR0x4Qqpl0dkWYyPRnt4Qx0x7Dl9YuCDNpBx8IR017UGilmHdC+C4UaK90QTeuyOYFPgvrpr2Oz44pIrwa4a3wsUPfbBqRzQSBOn5HWDa+QheywqhwyVAXHpj2PeEl/y8LU8wZJWI8ZWGtQ9+/CFlFzG9+n4P1NU1fsOPCO+EV7VM9hNh9xL0RvkKDjd5k0Ws824fua9OvvGe+9dXThOsAIg45UeU6OxzsEaJ17G1hN6XAEXeSgccIiPWNmPmH7nn67orzNdPmZE74YdrTTuSQOcEDCk+JF3aiRJGI9WkufujQN+NEJp1kV5G6Y+Psqi5o24msuTlZwusZ7ZjIFmEXRIZcrjm2KTjenzPvyyN42lAhPK1Px5z0JfgJ6rVK3mUx2t5KEFkjbytdwlOfM+l8mgobJhUGyb0l56sTrsGKkU3ciETAFwpPWxF4SBjYcF0yQocjIheEPfKyH5ENV+43I1fBvhF5kfzzrCDU+vaoulNJOamhcxUBWuKvkZNZ7sY8i63+J5H5DtfSMlXa+nZIucluIlXQNwTZrxoNn/MsMFg/IvU9c/wGZlmw9WnanDPzypEPDL3GPjnfvg9XL3KIQSXXr+J+cpW86EFkK/LJN05UWHbJJe+3cyci18ti5Orxufx3l28IvwjDLUInZg1OuJQgUqvtU17WoogEO+0qYaAcqZKBYff8Y1TQAid5J+lyvskRz9GeN3egtxwCB4yvRNWzNo/wMrlk7QwL7IWzkatrlUK44GpJm/0B+H4BqS3ysBwAAAAASUVORK5CYII=':'执行董事',

        'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADkAAAAOCAYAAACVZ7SQAAACg0lEQVR42rWXQWScQRTHR0SsWqGH6qFWyaGihypRqyKixB6qokJEVFWUVTlUDyGicqheqodaVbmsHKJiiYiIiBA5VA97yaGqclh66KGqQtUe6hNL+qZ+H5PJ++abrfbxY/b73nwz/5k3780ac9puCFWTbVV8NHsoXPKeTQvDJt4GhVHzn21KaATeN/DxrV84Fga853XEx9qSsBrhV2e8dga/8Dll94UjHBLaGgk+R/RJ7bGwR/urUPxLkW+FN5EiQ36zmsheJvZAWKetsY5PkT6ptYQx2m1P5IIwIdSE9zmT38M/RuQWY2rUNJFuuDbZJY2mEq4z7LBxRD5iV74J34U14YnQCUy8h+/sR4r8LGxk8CFPZItQ0Gh5Is8jJCHB2LNwwrmySWfHCdeCtxi+jdL/p3AhIkFdCbwv4fNPEs8KghKST1EJ11Rk+i7Lanx/WZgP+N0lIpIcOhlJ8s/DThcdnwsXlXDVRF4jKZmM7Gz7VYSbREchIHJbKW1+6dkIiey2hPRFiNwUPrHzmr0QDp3fTRYwVuQquSEossqZ2404k7u0Z7sQeUcYF4bIzq6ViZCK8mw4UuSOsvhnRI4xmZR5hKe/54Snnk8lQuSSt8J20HfO78uEppYJXwk/WJiQyBIXgwPm1ZcXrvZsLJLhprwycUy4jkSE60AgLJdpD3FG952JGWWH2t7Fo8ep0WVKiV3MW0SZXZiXLOCZkEmvSrbgX1UGtAnmGbedj4SfJrLB+VrxWOP7ZRatw2oXAjmgl3p7wiXBjnWbjThgARaU8lJ3NuW6u1O1nNpjnHo3xy0mncim935SuUhMO98v5fwR8G2ccezZ/kKiuSecy6mVr+24vwGFkdkzltO0vAAAAABJRU5ErkJggg==':'其他人员',

        'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADkAAAAOCAYAAACVZ7SQAAACk0lEQVR42rWWQWRcURSGn4roYoSI6qKqVESMitlVRUSJqCxidhExiwgjYlR1U1XVRZUsqkY9pSIisggREREjjIgsIsLoIqqqVEXULGYXXTxPaM+p/9bpce6dN6WXz9x37rtzz3/vOee+KOq8dREznrFZoiCeC7BlbaNEKcN7eSLO4OdfbYW4CPBWvJsjEvQXiCXBF6IunuuwyXcWIHzJ4JD45BkrCx/GiJZHXC+xSmz8wwFGW0RRiRzCgo4a8Vw8P8U87j8gxjGHmTCoEruesUIGkXNEk9gkrlkiFvHCd0ETdp9Ibs8gbo/4Bs7hxAGcZraN0N0R48wp5ktbzfBViuxGdHDEfMaGeFuMndA7EwdE5tVJOhYhwBrLi/+/CKznWhIQ2UP8IBrEdJZwjJETOkdCIksY13AufvSMlZTIdieZtDnJm53kHC9eUXlQEU75wpWf1xXHCB9tvyPm3cN/FwUxwlPa+J3rmMMF5WeH/ImMq/gDH7mAyD5iH7nh4Nx7p2w1nEAkKrM+5X0jAr4aeaYLTwkbG2w5hI7Lm1T0GxASEnmuwvzAuArOhMj7yD/NKoRK2wdU3fGAyCtYr5xF5AhIRf/kP4jkUJ0yeI8qLW0nKGQjba6Qu/BrLCQyEblzKfpNCBnC3WPl5GP8OspwWNoeEgNiXtVIiyNcA9J2liFcB4kb2JQUqWCKbHnKdh0i5RdFonZwS9FALmn7sJg3bFwvb4yrp2acjhM5ivFUfCxMYIzDfNI6SVe2L0W/BZFPUAj2ICDC7hUNqkaVdOiS34PCMYWTrGS4CR6hcrJvL4yvmz74moqPmd/VdV1VQ8crbMI8sYz8crt2Cw52wm3lEBeNNaz/Gmu1a/3ES/gdanz1dP0CG38SpdFXf2kAAAAASUVORK5CYII=': '副董事长',


        'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB0AAAAOCAYAAADT0Rc6AAABoUlEQVR42r2UT0REURTGr5G0eCJJWkWrFrNLxshom1m0mM1IRkak1WgRLUbSLmmRJDIyRtImaTFGJC3Sov0s0ma0GEkkSVrE9J18L2fuvDtv2nT5effdd+89/77zjGkefWDV/PNYA0ecz4JPBxPcMwkyCjkzB94c1E1AlE9gOMSpG/W+AHbpyD7YBvNck5EEp5x303DT2ALr/CgX9Frfl8E9GAhw5hl4nIvRPd4zDc4492yjMV7YA/LgUn2TzUXQACuODNhGa6AMbsEj5xXbaJEpksVXpjjC9EkdCmCcB6tgKsRoR+mNEIlwEUTpodQvYRlI0REpxQ4vavBZo9EyDfoaSDLVLTXNK6/8lHsOhogr0jtQYhAPnB/aRsWLL7bLCTjmWp28gA/1vtkmvV3Uhp1eo/b89tsByHJjv3Vpho6YDoSUowaEc6a8oBgNukBqG+fzL0Zn2CqigTTZoILTikH/UJx9KjV4p0o7iVR695qluaIu9LDT26LIJTCmRHShqFLNei1H0aRUDbMUTSlASD6uXv/5JSZCGAk4F2V07Yh9A2Qgg+AVrBiLAAAAAElFTkSuQmCC': '经理',

         'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACsAAAAOCAYAAAC2POVFAAACPUlEQVR42sWVX2SVYRzHHzNHcsSRJF2MyWR2l5kk3SXnYjKOYzKZMV0dk9jFJF3EZCZJzMwcSczMLmZipovM7H4XGZkuJhlJki5ifX983vl59j7vToz9+DjP8573eZ7fn+/ze0M4alfEg5znDf7Ls4p4HE7BLog9Meie3RTfxMXEmifiLeN74k+CG7xzSww5bM198TPBXt6hVZgUz9z8s5h28zirFkhHQQIsmA03HxWvCGBGvBAjPMv8WGJcwuEjdiAWxLsEC7zjbUo8ZVM7+Fz0/yOxQ8Vi2xdlxubsa/bpF8uMy0XOlgoyVIqc7cORM2JCrLv/7JB53h9P7Bc7uytWxJb4ynj1pJydp5S22Q+k0EaZTWezopcDt8WdY5z9bxnUxN0EtcjZNling/SQkQ0upbcBAjDJvMSBA353cXYFRzONV5HEiWl2wmUhk0Y5wSVIZfaTaBL8F8ZvUs5WyVSW/k3RHWWy5uYW9V/a1iIB9ZNB47v47ebPC2TQjvZjGQT3zqHNobUq5Qj0wB3aU6DP2qGdrl/aumHWnY/2HCKA0MIFa6Bx4z3SmHVczRadJQMdkbMBjdnz27ShUfpuJTrYsn7dVaZVZwdpWabxOkzSEeqOww/SQ6LJSrCWs/E4mwbKPo1zU2jsF7e+lcxa0B+R0Ad0H8txKRVhnYPNLpPlpivBHF+pXqehdm74mLjmLteaY5vu4J81uEwDTqPDnNfMuWAZqV4duqIS1GlLx1mFchbRmbOux33KU/T9A1cGuQIA/VG9AAAAAElFTkSuQmCC':'总经理',

        'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADkAAAAOCAYAAACVZ7SQAAACxUlEQVR42r2WX2RbURzHr4iYiRE1NXsoNTNTM6aqpvYyM3moKRFVNVWqDxMzIw8104dSUzVTY6aiZkJN7KGmVE1NTdljH6bM7CFiwkzNTIXtd/hcvjnuvUkfusOHc07uPff3/f07CYLjj7QxEbF/wZiN2C/xW9TIGY+C/zQqxmECz+TZrPEn4oyzRt0Yl70R47vRG/Pdx8Zr5hOcG8V1nrlhTArunbsJdteP64iacSdGZB4WjQVZfzGWZe1H0TmgL+Gbzgm7sp4xVvj+C+OpMc1eaEeNeQahbcMZ2EB9SIP9TiL/GutGNYZ1ntGxZMxjjDP4jPf7Q+OADPFHEzsCRD7nnFHjLfNslMgVXtChXuokMpMQkYwncggBp4w5Y9srhwrPl2PO80V+NTaMPQLj5u/iRO4YL4WdExJZ4QxnxE9SNkU61vn2IIbuG7c7iOw6XV0h35P6ybOe7FJkgd+jKHgiU7BNRx4gArs0Kx1jCJ+nAR5y1iERnCZyeanhPKnbJtKlzVoC2ROoyTnxepjC2RjOQVwkP2Onc9o35q98kWGR3oQjmX8yerrorilJk4/GZS9yBVk7L7e4Pt7giFFpeD+M37J+kpCuaYLkp2sgz7SJHIEjme91ELlKLeVJmzD1D7gmAu5JZ2y/3HfuvSne64konWpCjavIkvSQTVJY+8ol/4IP06sl8wZGXKGdq8jTeLzPExlQQ27/FtfBDPdmzjPYRXlYMqFbkeNcHS4QRVgkKEWhV0U25RCN1Jbn6Zz8/gDvhamyFWFQGWMC0nMZUUvU0C+6aDeRdM76QBDeU9d+2dTiPBNGZwNaMm8iskyr3iQiAZ4aZn6eqK5Jqqzyr2ZQvpOmY943rknT2RL2ySDdK9FkxqQGp7wGqY0npKzdtUrT8FnAuFmMdsZfjXHWRS9VilwPnUZOekAc/RHvDXhXXhRD/wB5SwMiRVOUpAAAAABJRU5ErkJggg==': '副总经理'
         }


        Con_info=[]
        # for j in range(len(url)):
        person={}
        Rzhiwei={}

        #获取所有主要人员名单
        try:
            driver.find_element_by_xpath('//*[@id="keyperForAll"]/span/a[2]').click()
            time.sleep(3)
            #切换到最后一个句柄
            driver.switch_to_window(driver.window_handles[-1])
            print 'ok'
            driver.find_element_by_xpath(' //*[@id="more"]/a/span').click()
        except:
            pass
        time.sleep(3)
        for i in range(1,30):
            try:
                person[i]=driver.find_element_by_xpath('//*[@id="personInfo"]/ul/li[%d]/a/div[1]' %i).text
                person[i]=''.join(re.findall(ur'[\u4e00-\u9fa5]',person[i],re.M))
                # print person[i]
            except:
                break

        for i in range(1, len(person) + 1):
            for j in range(i, len(person) + 1):
                if person.get(i) == person.get(j + 1):
                    person[j + 1] = person[j + 1] + str(j)
        #print person
        time.sleep(1)


    #职位分开来
        for i in range(1,30):
            try:
                Rzhiwei[i]= zhiweibiao[str(driver.find_element_by_xpath('//*[@id="personInfo"]/ul/li[%d]/a/div[2]/span/img' %i).get_attribute('src'))]
            except:
                try:
                    Rzhiwei[i]=driver.find_element_by_xpath('//*[@id="personInfo"]/ul/li[%d]/a/div[2]/span' %i).text
                except:
                    try:
                        if driver.find_element_by_xpath('//*[@id="personInfo"]/ul/li[%d]/a/div[1]' %i).text:
                            Rzhiwei[i]='空'
                    except:
                        break
        if driver.window_handles[-1]!=driver.window_handles[0]:
            driver.close()
            driver.switch_to_window(driver.window_handles[0])
        else:
            pass

        #该公司社会统一编码
        scocial_Code=driver.find_element_by_xpath('/html/body/div[5]/div[4]/div[2]/div[15]/div[2]/div[1]/span[1]/span').text
        #把信息整合成字典的形式，加上社会统一编码
        called=['name','position','social_unique_code']
        with codecs.open('kpi_dicw.csv','a+','utf-8') as csvfile:
            writer=csv.DictWriter(csvfile,fieldnames=called)
            for i  in  range(1,len(Rzhiwei)+1):
                result = {}
                result['name']=person[i]
                result['position']=Rzhiwei[i]
                result['social_unique_code']=scocial_Code
                Con_info.append(result)
                writer.writerow(result)

        print Con_info
        print len(Con_info)


        return  Con_info







#测试
driver=webdriver.Chrome()
# url='http://www.gsxt.gov.cn/%7BBIpUiz2ySe_d1Zd8nSikrFMeQFGfCJEpu1v92i6rnuPLauFNB0zqm6u9-5GX80x8x71nWLX87Dkz_ULWZsEOUxht9ownoVoxXdGYk7wUXT9t5xL3E8G8oHgD58yz0PUK-1508980989967%7D'
url=['http://www.gsxt.gov.cn/%7BNCk7uRHqcoE-P4Fm6-WovpP-YjP4AXumW3rn7_VuQShI8QI6UNMO-7hCAKErGXWQGy83P0vhvV2l5YO0amGPoD29fFSXOsvweNyShQ81s1WjRVY8C04sRC0piImnL2mA-1508988604287%7D','http://www.gsxt.gov.cn/%7BYUBD9Lcsq3ssknL-QLsLxWcw9_7TydPnY29go8hSF7BDXJjZGqSrxvxq8Vv1w6dNixN0DRvUUlVeiZrhrVR053h01nTQiSvTuS4jC32G-tQleNluDjXfQuW9rqLgmwhn-1508988012703%7D','http://www.gsxt.gov.cn/%7BYUBD9Lcsq3ssknL-QLsLxWcw9_7TydPnY29go8hSF7BDXJjZGqSrxvxq8Vv1w6dNixN0DRvUUlVeiZrhrVR059RoIrD9NNniWBlqytkyfyDe6KLC2bFVqE7nE_2GvEUH-1508987602135%7D','http://www.gsxt.gov.cn/%7BBIpUiz2ySe_d1Zd8nSikrFMeQFGfCJEpu1v92i6rnuPLauFNB0zqm6u9-5GX80x8K4tn2F9mmb-NIl--ZwPcntqWqaRR57CYjOm8e8VtB0b3jjw-bhuRV8jlugCFom1Y-1508981306646%7D','http://www.gsxt.gov.cn/%7BBIpUiz2ySe_d1Zd8nSikrFMeQFGfCJEpu1v92i6rnuPLauFNB0zqm6u9-5GX80x8x71nWLX87Dkz_ULWZsEOUxht9ownoVoxXdGYk7wUXT9t5xL3E8G8oHgD58yz0PUK-1508980989967%7D','http://www.gsxt.gov.cn/%7BEbmYKfydJwF7l8fh4Qrhps_bRETdJbnBBrANWwfUazs8qT-ktLLkHuBjoem9TtvW-nHuDLjaAN3InjmS5ZUZcVXr8NO2MssNNI5JItpnqTl44E7Gk-_5DFIsFeG5CAZT-1508978450538%7D','http://www.gsxt.gov.cn/%7BhAmmc6FpT8V618uMFjSZmqZcgLK7nzGI2PudIqVDgJ9Hwk5dLczBIYPEv87WfIch4_zfynyKGKt0XEDe9KfKx6lH-yxyr0ZyqJ3AwDg9J1pcmau5rbjdh20kPVHkPY28BJp_A5mlO3-rzLC_VTlqSg-1508980306677%7D','http://www.gsxt.gov.cn/%7BpaXLVyWEb_ViKy3-BtzuXnnnvN-1FAyyyTVkPXJ-z5tDV7PJCkUxk1UE4q1Wc6jLTnJDL18SDeoPrHfLpCoaat6DDq-4-Wfu__ZiB8RfkgRAhN8ou6djL7PvONVMM3Nb-1508979729301%7D','http://www.gsxt.gov.cn/%7BQ1DaO6xsy2U8dBKR7Zzr35bGwYbe4fnx7k3NScI6lLCDnyd-NtiO9MbOGEst11aS6YtNBFbd-1fbzvhfyWYjjZ-McqD7hdELPz-7oIkRE95akzP7c_E04OZ2KBzfJrM5-1508977256932%7D','http://www.gsxt.gov.cn/%7B7ajRZ9kWW4COFx6DuMrXYtzAI8xZ5ifr-dImvKZSe0xYikQfdO2td0xZCSozmB9LCOAYuIAC9ArYAntsgnI3C_eqPGxSTxfh5VAGkPjgogDJJMf2hZZtnvaCr2lHA6fg-1508917426272%7D','http://www.gsxt.gov.cn/%7B7ajRZ9kWW4COFx6DuMrXYtzAI8xZ5ifr-dImvKZSe0xYikQfdO2td0xZCSozmB9L2kY2Z_ctnD1_GvkL44LizEyywsY8Fp0C4UNY2qy1Acgntid26AaMo1pCeHgKDUug-1508918591065%7D','http://www.gsxt.gov.cn/%7B7ajRZ9kWW4COFx6DuMrXYtzAI8xZ5ifr-dImvKZSe0xYikQfdO2td0xZCSozmB9L0_4Z7-knQrlkWfTYlZk64C_dhrKag9ZO0NqAlMYiuNuUJtpJIaplLoi_-JjY-_fWfQtfn5t-wFY5MPO4dhLulA-1508918591067%7D','http://www.gsxt.gov.cn/%7B7ajRZ9kWW4COFx6DuMrXYtzAI8xZ5ifr-dImvKZSe0xYikQfdO2td0xZCSozmB9LhTO5ZQuj0WIMKPEhZ6M6-MqUr97ld8vC7zdrAI4J1FXR1zpZcFgrEvfmjOzaMzlx4Uv-VnP5mShl_YIUIUzV-2PW9ED6N7DGn9TjS2-VRGQ-1508918591063%7D','http://www.gsxt.gov.cn/%7B7ajRZ9kWW4COFx6DuMrXYtzAI8xZ5ifr-dImvKZSe0xYikQfdO2td0xZCSozmB9LytTeyXUVkWArocttMqA6MkWCUBHgLcr7xDLUf7diFsRBJHhLUiSfiB9gA_8TB3MT-1508911915425%7D']
con_data_k=[]
con_data_b=[]
con_data_s=[]
for j in range(len(url)):

    driver.get(url[j])
    if driver.current_url=='http://www.gsxt.gov.cn/index/invalidLink':
        pass
    else:
        #留出页面加载时间
        time.sleep(10)
        #窗口向下滚动
        driver.execute_script("window.scrollBy(0,3000)")
        time.sleep(1)
        driver.execute_script("window.scrollBy(0,5000)")
        time.sleep(1)
        ck_info=getIC_INFO(url,driver)
        ck_info.business_licence_info()
        time.sleep(1)
        ck_info.Key_person_info()
        ck_info.Shareholder_investment_info()


# conn = MySQLdb.connect(host='192.168.60.100', user='root', passwd='ahzx2016', db='test1', port=3306, charset='utf8')
# cur = conn.cursor()
# db=HeroDB('hello', conn, cur)
#
#
# db.insertMore('hello1',con_data_s(ck_info.Shareholder_investment_info()))
# db.insertMore('hello2',con_data_k(ck_info.Key_person_info()) )
# db.insertMore('hello',con_data_b(ck_info.business_licence_info()))




driver.close()