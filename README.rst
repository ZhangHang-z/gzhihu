getzhihu是一个爬取从问答网站知乎上爬取内容的爬虫 
----------

##How to use
----------

####conf.ini文件说明
conf.ini文件通过模块ConfigParser.ConfigParser解析, 通过名字就可以知道这个文件一般是放置一些常用的配置信息。  
比如post信息，header头信息。
 
.. code-block:: python
  conf = ConfigParser()  #初始一个ConfigParser对象  
  conf.read('conf.ini')  #读取当前目录下conf.ini文件  
  email = conf.get('account', 'email')   #得到account段中email的value

  conf.section()   #执行结果为一个列表，包含3个段的头信息   
  ['account', 'cookies', 'header']  

  dict(conf._section['account'])  #生成一个然后转化为字典，但是会自动加入 '__name__': 'account'
  {'__name__': 'account', 'password': ' ', 'email': ' '}

  #未转化为dict前的执行结果：  
  conf._section['account']
  OrderedDict([('__name__', 'account'), ('email', 'sbzhg1@163.com'), ('password', '7748548w')])

  type(conf._section['account'])
  <class 'collections.OrderedDict'>



####代码示例
.. code-block:: python

  from zhihu import mysession, MyZhihu, Question

  #创建一个会话
  session = mysession()

  #把会话对象创给MyZhihu类
  my = MyZhihu(session)
  print my.ask()  #打印我的全部问题
  print my.topic()  #打印我的话题
  print my.column()  #打印我关注的专栏

  #有些问题在question/23905111 还有#12817817 请删除后面的
  question = Question('http://www.zhihu.com/question/23905111', session)
  print question.title()  #问题的标题
  print question.question_detail()  #问题的详情
  print question.answer_number()   #问题的回答数
  print question.follower()    #问题的关注数

  
  #会打印出问题的每个答案
  answers = question.all_answer()  
  for each in answers:
     print each

  #如果你需要保存，第二个参数是保存文件的路径，第三个参数是文件打开的读写模式。
  #如果你要指定文件   /home/path/a.txt
  #如果你要指定命令  /home/path/dir/   会在次路径下生成以问题标题为名的文件
  question.save(answers, '/path', 'w')




