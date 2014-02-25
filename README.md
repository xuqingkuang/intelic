INTELIC Readme
==============



概况
---

INTELIC 是一套自动编译系统，可以通过选择基础代码库（Baseline）和选择设备补丁（Component）后，将编译任务交给编译后端进行编译，目前可选的编译后端只有 Jenkins 一种。

INTELIC 使用了 Python 开发语言，基于 Django 1.5+ 框架编写，通过 Nginx + uwsgi 进行部署。

准备开发环境
-----------

INTELIC 可以在 Linux 或者 Mac OS X 上运行，要求 Python 版本高于 2.6，Django 版本高于 1.5。

可以通过在命令行中运行如下命令查看相关版本：

    $ python
    Python 2.7.5 (default, Aug 25 2013, 00:04:04) 
    [GCC 4.2.1 Compatible Apple LLVM 5.0 (clang-500.0.68)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import django
    >>> django.VERSION
    (1, 6, 1, 'final', 0)

如果版本不对，可能需要更换更高版本的发行版，或者使用 pip 进行升级。

编辑器可以根据自己情况选择，我推荐使用在 Mac OS X 上的 Textmate 2。

如果需要部署，还需要 python-uwsgi 包和 nginx 服务器软件。

开发流程
-------

首先需要将代码从 Github 上下载下来：

    $ git clone https://github.com/xuqingkuang/intelic

然后进入目录并且初始化数据库，开发用数据库使用 SQLite，非常简单：

    $ cd intelic
    $ python ./manage.py syncdb
      ...

在执行过程中会提示用户输入超级用户的用户名和密码，这里可以选择 no，因为在 initial_data.json 中已经初始化四个用户，包含一个超级用户 admin 了。

然后就可以尝试着启动一下测试服务器了，如果正常则会打印出类似如下输出：

    $ python ./manage.py runserver
    Validating models...

    0 errors found
    February 25, 2014 - 22:53:05
    Django version 1.6.1, using settings 'intelic.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

然后使用浏览器访问 http://127.0.0.1:8000 即可打开测试页面。
    
如果需要中止，可以如提示按下 Control 和 C 键。

在开发过程中，对 Python 代码的编写将自动 auto reload 应用，无需开发者手工重启。

部署
---

INTELIC 使用 nginx + uwsgi 方式进行部署，范例配置文件放在 [deploy](https://github.com/xuqingkuang/intelic/tree/master/deploy) 目录中。


默认 INTELIC 在服务器上的位置放在 /var/www/intelic 下，将代码使用 git clone 命令放置到 /var/www/ 目录下后，将 deploy 目录下的 intelic-uwsgi.ini 放置于 /var/www/intelic 下，将 nginx-default.site 放到 /etc/nginx/sites-enabled 目录下。


然后使用如下命令启动 uwsgi 服务：

    uwsgi ./intelic-uwsgi.ini
    
随后重启 nginx 服务即可。

如果发现图片和 CSS 类的静态文件无法获取，需要将这些文件收集到一起，可以在 intelic 目录下执行

     $ python ./manage.py collectstatic

程序架构
-------

INTELIC 是一个标准的 [Django](https://www.djangoproject.com) 应用程序，采用 MVC 结构将代码拆分开，在进行开发之前，还请阅读[开发文档](https://docs.djangoproject.com)，了解相关知识。

### 主要的目录结构如下

    + bootstrap_admin <- Django 管理界面的 Bootstrap 的类库
    + bootstrapform <- Django 表单类库的 Bootstrap 类库
    + deploy <- 范例配置文件
    + intelic <- 主程序目录
    + + account <- 用户认证模块
    + + builder <- 主程序模块
    + media <- 用户上传的媒体文件，例如补丁和打包后的补丁都放置在其中

