# DEMO


> #### 部署步骤
> 1. 安装Django 版本不论 只要不报错
> 2. 调用manage.py脚本开启服务
>    `python manage.py runserver 8000`
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
> ├─templates  //具体页面html代码
> │  ├─first.html
> │  └─index.html
> └─TestDjango //Django框架代码位置
>     │  asgi.py
>     │  settings.py
>     │  urls.py
>     │  views.py
>     │  wsgi.py
>     │  __init__.py
>     └─__pycache__
> ```
