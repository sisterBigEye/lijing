#!/usr/local/bin/python
# -*- coding: utf8 -*-
'''Created on 2016年9月2日@author: PaoloLiu'''
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time
def main():
    #这里的文件路径是webdriver的文件路径
    driver = webdriver.Chrome()
    # 打开网页
    driver.get("http://127.0.0.1:8000/")
    #     等待页面的上元素刷新出来
    WebDriverWait(driver, 30).until(lambda the_driver: the_driver.find_element_by_xpath("//div[@class='gt_slider_knob gt_show']").is_displayed())
    WebDriverWait(driver, 30).until(lambda the_driver: the_driver.find_element_by_xpath("//div[@class='gt_cut_bg gt_show']").is_displayed())
    WebDriverWait(driver, 30).until(lambda the_driver: the_driver.find_element_by_xpath("//div[@class='gt_cut_fullbg gt_show']").is_displayed())
    # 找到滑动的圆球
    element=driver.find_element_by_xpath("//div[@class='gt_slider_knob gt_show']")
    #鼠标点击元素并按住不放
    print "第一步,点击元素"
    ActionChains(driver).click_and_hold(on_element=element).perform()
    time.sleep(1)
    print "第二步，拖动元素"
    #拖动鼠标到指定的位置，注意这里位置是相对于元素左上角的相对值
    ActionChains(driver).move_to_element_with_offset(to_element=element, xoffset=200, yoffset=50).perform()
    time.sleep(1)
    print "第三步，释放鼠标"
    #释放鼠标    ActionChains(driver).release(on_element=element).perform()
    time.sleep(3)
if __name__ == '__main__':
   pass
main()
