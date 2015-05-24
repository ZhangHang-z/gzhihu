getzhihu是一个爬取从问答网站知乎上爬取内容的爬虫 

how to use
----------

例子 

.. code-block:: python

  from zhihu import mysession, MyZhihu, Question

  session = mysession()

  my = MyZhihu(session)
  print my.ask()
  print my.topic()
  print my.column()

  question = Question('http://www.zhihu.com/question/23905111', session)
  print question.title()
  print question.question_detail()
  print question.answer_number()
  print question.follower()
  print question.all_answer()

  answers = question.all_answer()
  question.save(answers, '/home/zhg/Pictures/', 'w')
