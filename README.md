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
> ├─static //静态文件
> │  ├─css     //样式文件
> │  │  └─index //每个页面可以单独设置的样式保存在独立的文件夹里
> │  ├─fonts //字体文件
> │  └─images  //logo等图片保存位置
> ├─templates  //具体页面html代码 每个APP单独一个文件夹保存
> └─TestDjango //Django框架代码位置
>     │  asgi.py
>     │  settings.py
>     │  urls.py
>     │  views.py
>     │  wsgi.py
>     │  __init__.py
>     └─__pycache__
> ```

> #### 记录
> TestDjango作为主要项目  
> 将每一个新项目注册为APP  
> 其中main作为项目组整体页面，TestDjango只作为框架，内容均分散到各个APP中。   
> 注册命令是:  
> `python manage.py startapp APP名称`  
> 注册后，在主项目的 **_settings_** 文件里的 **_INSTALLED_APPS_** 中添加APP名称  
> 如何设置APP的url详见教程  [APP初始设置](https://baijiahao.baidu.com/s?id=1628323324998359528&wfr=spider&for=pc)  
> 