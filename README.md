# DEMO


> #### 部署步骤
> 1. 安装Django 版本不论 只要不报错
> 2. 调用manage.py脚本开启服务  
> `python manage.py runserver 8000`
> 3. 打开localhost:8000页面


> #### 目录结构描述
> ```
> │  db.sqlite3
> │  manage.py
> │  README.md
> │  task
> │ 
> ├─main
> │  │  admin.py
> │  │  apps.py
> │  │  models.py
> │  │  tests.py
> │  │  urls.py
> │  │  views.py
> │  │  __init__.py
> │  │  
> ├─neuropeptide
> │  │  admin.py
> │  │  apps.py
> │  │  forms.py
> │  │  models.py
> │  │  tests.py
> │  │  urls.py
> │  │  views.py
> │  │  __init__.py
> │  │
> ├─static
> │  ├─assets
> │  └─file
> │          test_download_file.txt
> │          
> ├─storage_file
> ├─templates
> │  ├─main
> │  │      index.html
> │  │      
> │  ├─neuropeptide
> │  │      index.html
> │  │      
> │  └─zsm
> │          index.html
> │          
> ├─TestDjango
> │  │  asgi.py
> │  │  settings.py
> │  │  urls.py
> │  │  views.py
> │  │  wsgi.py
> │  │  __init__.py
> │  │      
> ├─zsm
> │  │  admin.py
> │  │  apps.py
> │  │  models.py
> │  │  tests.py
> │  │  urls.py
> │  │  views.py
> │  │  __init__.py
> │  │   
> └─教程副本
>         app-url教程.pdf
> ```

> ### 记录
> TestDjango作为主要项目  
> 将每一个新项目注册为APP  
> 其中main作为项目组整体页面，TestDjango只作为框架，内容均分散到各个APP中。   
> 注册命令是:  
> `python manage.py startapp APP名称`  
> 注册后，在主项目的 **_settings_** 文件里的 **_INSTALLED_APPS_** 中添加APP名称  
> 如何设置APP的url详见教程  [APP初始设置](https://baijiahao.baidu.com/s?id=1628323324998359528&wfr=spider&for=pc)  
> ### 添加MySQL连接
> 设置教程 [MySql连接教程](https://blog.csdn.net/weixin_45539338/article/details/125547848)  
> `python manage.py migrate`  
> 当有新的APP注册、并且要通过模型新建表的时候需要用一次
> 
> ### 表单设置
> 请仿照neuropeptide 没有具体教程，太杂了。=-=
> 
> ### 接收数据
> 接收文件 [接收文件教程](http://www.chenxm.cc/article/1253.html.html)
> 
> ### 运行脚本
> `python manage.py runscript script`
> 
> ### 添加全局变量
> 在settings里添加全局变量 保存文件路径   
> 通过`from django.conf import settings`可以使用变量  
>  
> ### 数据库state记录
> state == 0 表示提交以后还没执行的任务
> state == 1 表示提交以后已经顺利执行完毕的任务
> state == 2 表示提交以后在执行过程中出错的任务
> 
> ### 在样式文件中的操作 style.css
> 在section的样式上加入了height:100vh，将每一个框限制为了一页页面，并且配合body中的overflow:hidden;样式，将项目修改为只能通过点击上方标题栏进行跳转，这样可以做出假的好几个页面的感觉。  
> 如果不喜欢，可以将上述设置取消即可。
> 
> ### 写神经肽脚本时的经验
> 在遇到脚本中，需要用到路径的地方，需要用绝对路径，可以利用`os.path.dirname(__file__)`获取文件所在项目的绝对路径，然后利用os.path模块进行操作  
> 切忌直接利用字符串形式操作，因为不同的操作系统会有不同的形式，转移到服务器会报错。