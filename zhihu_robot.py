# -*- coding: utf-8 -*-
'''
@version: Python 3.7.3
@Author: Louis
@Date: 2020-01-02 10:32:32
@LastEditors  : Louis
@LastEditTime : 2020-01-02 16:45:59
'''
import time
import json
import argparse
from selenium import webdriver


class ZhihuRobot:
    """
    运行该程序前需要用Chrome的扩展程序"EditThisCookie"导出登录状态下知乎的Cookies，
    保存为"zhihu_cookie.json"文件，放在与程序同一个目录下，然后双击运行程序即可。
    
    @personal_url: 个人域名，格式如"zhihu.com/people/12-18-19-5"，可从设置页面或者网址输入栏获取
    @keyword:      想要删除的想法所包含的关键字，默认为"红包派对"
    """
    def __init__(self, personal_url, key_word="红包派对"):
        self.url = "https://www.zhihu.com/login/email"
        self.thoughts_url = "https://www." + personal_url + "/pins?page={}"
        self.key_word = key_word
        self.page = 1
        self.item = 1
        
    def headless_options(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        return chrome_options
    
    def login(self, options = None):
        if options:
            self.driver = webdriver.Chrome(options = options)
            self.driver.implicitly_wait(1)
            self.driver.get(self.thoughts_url.format(self.page))
        else:
            self.driver = webdriver.Chrome()
            self.driver.implicitly_wait(1)
            self.driver.get(self.url)
    
    def turn_page(self):
        self.page += 1
        self.driver.get(self.thoughts_url.format(self.page))
        self.item = 1
        
    def get_cookies(self):
        self.login()
        self.driver.delete_all_cookies()
        print("请在60秒内手动完成登录操作！")
        self.driver.maximize_window()
        self.driver.refresh()
        time.sleep(30)
        cookies = self.driver.get_cookies()
        with open('zhihu_cookie.json','w') as f:
            json.dump(cookies,f)
        self.driver.close()
        
    def add_cookies(self):
        with open('zhihu_cookie.json','r') as f:
            cookies = json.load(f)
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.refresh()
        
    def delete_thoughts(self):
        self.login(options=self.headless_options())
        self.add_cookies()
        while True:
            try:
                tht = self.driver.find_element_by_xpath(f'//*[@id="Profile-posts"]/div[2]/div[{self.item}]/div/div[2]/div[1]/span')
            except:
                try:
                    self.driver.refresh()
                    time.sleep(0.8)
                    tht = self.driver.find_element_by_xpath(f'//*[@id="Profile-posts"]/div[2]/div[{self.item}]/div/div[2]/div[1]/span')
                except:
                    return None
            print(tht.text)
            if self.key_word in tht.text:
                print("{:=^40}".format("DELETED"))
                try:
                    delete_button = self.driver.find_element_by_xpath(f'//*[@id="Profile-posts"]/div[2]/div[{self.item}]/div/div[2]/div[3]/button[4]')
                except:
                    self.turn_page()
                    continue
                delete_button.click()
                time.sleep(0.8)
                yes_button = self.driver.find_element_by_xpath('/html/body/div[3]/div/div/div/div[2]/div/div/div/button[1]')
                yes_button.click()
                time.sleep(0.8)
            else:
                print("{:=^40}".format("KEPT"))
                self.item += 1
    
    def quit_program(self):
        self.driver.quit()
        input("请按任意键结束程序")
        
    def main(self, I_dont_have_cookie_json=False):
        if I_dont_have_cookie_json:
            self.get_cookies()
        self.delete_thoughts()
        self.quit_program()     
        
if __name__ == "__main__":
    p = input("请输入个人域名（必填项，格式如“zhihu.com/people/12-18-19-5”）：")
    k = input("请输入要删除的想法包含的关键字（直接回车默认为“红包派对”")
    if not p:
        print("必须输入个人域名！")
    if k:
        rbt = ZhihuRobot(personal_url=p, key_word=k)
    else:
        rbt=ZhihuRobot(personal_url=p)
    rbt.main()