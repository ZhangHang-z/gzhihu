# -*- coding:utf-8 -*-
import requests
import re
import sys
import json
import functools
import os
import sys
from bs4 import BeautifulSoup
from ConfigParser import ConfigParser

reload(sys)
sys.setdefaultencoding('utf8')


def mysession():
     conf = ConfigParser()
     conf.read('conf.ini')
     cookies = dict(conf._sections['cookies'])
     header = dict(conf._sections['header'])
     post_data = dict(conf._sections['account'])
     session = requests.Session()
     r = session.post('http://www.zhihu.com/login', data = post_data, headers=header)
     return session


class MyZhihu(object):
    def __init__(self, session=None):
        self.zhi = 'http://www.zhihu.com'
        if session == None:
            raise "Exception: session is None" 
        else:
            self.session = session
    #我的提问
    def ask(self):
        html =  self.session.get(self.zhi + '/people/Grapher/asks').text
        soup = BeautifulSoup(html)
        ask_gen = ((self.zhi + str(ask.get('href')) + ' ' + str(ask.get_text().encode('utf-8'))) \
                    for ask in soup.find_all('a', 'question_link'))
        for ask in ask_gen:
            print ask

    '''def inbox(self):
        html = self.session.get('http://www.zhihu.com/inbox').text
        soup = BeautifulSoup(html)
        for x in soup.find_all('div', 'zm-pm-item-main')
            print x.get(a) '''
    #话题
    def topic(self):
        html = self.session.get(self.zhi + '/people/Grapher/topics').text
        soup = BeautifulSoup(html)
        topic_gen = (topic.strong.get_text() for topic in soup.find_all('div', 'zm-profile-section-main'))
        for t in topic_gen:
            print t
    
    #专栏 
    def column(self):
        html = self.session.get(self.zhi + '/people/Grapher/columns/followed').text 
        soup = BeautifulSoup(html)
        column_gen = (column.strong.get_text() for column in soup.find_all('div', 'zm-profile-section-main'))
        for c in column_gen:
            print c




class Question(object):
    def __init__(self, qurl=None, session=None):
        if qurl == None or session ==None:
            raise 'Your question-url or session is None'
        else:
            html = session.get(qurl).text
            self.soup = BeautifulSoup(html)

    def title(self):
        thetitle = self.soup.find('h2', 'zm-item-title zm-editable-content')
        return thetitle.get_text().strip()

    def question_detail(self):
        question_detail = self.soup.find('div', 'zm-editable-content')
        s = question_detail.get_text()
        d = re.sub('<>','',s)
        return d.strip()

    def an(self):
        ans = self.soup.h3['data-num']
        return ans.strip() 

    def answer_number(self):
        answer_number = self.an()
        return answer_number + '-人回答'

    def follower(self):
        follower = self.soup.find('div', 'zg-gray-normal')
        return '-'.join(follower.get_text().split())

    def logging(log):
        if callable(log):
            F = log
            @functools.wraps(F)
            def internal(self):
                return F(self)
            return internal
        else:
            def wrapper(F):
                @functools.wraps(F)
                def internal(self):
                    print log
                    return F(self)
                return internal
            return wrapper
              
    @logging('生成中..............')
    def all_answer(self):
        answer_number = self.an()
        reg_img = r'http://pic3.zhimg.com/\w+\.jpg'
        if answer_number == 0:
            print "This question is no answers"
        else:
            re_br = re.compile(r'<br/?>')
            re_allmark = re.compile(r'<[^>]+>',re.S)
            all_answer_list = self.soup.find_all( 'div', 'zm-item-answer ') #所有回答列表
            for each in all_answer_list:
                yield each.h3.get_text()  #答主
                content = str(each.find('div', ' zm-editable-content clearfix')) 
                br2n = re.sub(re_br, '\n', content)
                for s in br2n.split('\n'):
                    yield re.sub(re_allmark, '', s)
                
    def save(self, answers, path, pattern):
        title = self.title()
        question_detail = self.question_detail()
        answer_number = self.answer_number()
        followers = self.follower()
        all_answers = answers
        filename = '/' + title.strip() + '.txt'
        if sys.platform == 'linux2':
            if os.path.exists(os.path.split(path)[0]):
                if not os.path.split(path)[1]:
                    destpath = os.path.split(path)[0] + filename
                else:
                    destpath = path
            else:
                raise 'You path is not exists'
        else:
            raise 'Other systems such as Windows are not currently supported'
        with open(destpath, pattern) as f:
            f.write('标题：%s \n' % title + '问题详情：%s \n' % question_detail + '回答数：%s \t' % answer_number \
                + ' 关注数：%s \n' % followers)
            for each in all_answers:
                f.write(each + '\n')


   
