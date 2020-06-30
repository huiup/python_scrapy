### scrapy的基本使用：

- ##### 创建一个工程：

  - `scrapy startproject ProName(项目名字)`
  - 目录结构：
    - spiders:爬虫文件夹
      - 必须要存放一个爬虫源文件
    - setting.py:工程的配置文件

- cd ProName

- 创建爬虫源文件：

  - `scrapy genspider spiderName(爬虫文件名称) www.url.com`
  - 在爬虫文件中编写对应的代码

- 执行工程：

  - `scrapy crawl spiderName(爬虫文件名称)`
  - 执行工程后，默认会输出工程所有的日志信息
  - 指定类型日志的输出：
    - 在setting.py中加入`LOG_LEVEL = 'ERROR'`：表示只打印错误的日志信息

##### 爬虫文件spiderName内容阐述：

- name：爬虫文件名称，该文件的唯一标识
- allowed_domains：允许的域名
- start_urls：起始url列表，存储的都是url，url可以被自动进行get请求的发送
- parse方法：请求后的数据解析操作，调用的次数取决于请求的次数，

##### setting.py：

- 禁止robots协议
- 指定日志类型：`LOG_LEVEL = 'ERROR'`
- UA伪装

##### scrapy数据解析

- 使用：response.xpath('xpath表达式')
- scrapy封装的xpath和etree中的xpath区别：
  - scrapy中的xpat直接将定位到的标签中存储的值或者属性值取出，返回的是Selector对象，且相关的数据值是存储在Selector对象的data属性中，需要调用extract()、extract_first()取出字符串数据

##### 持久化存储

- 基于终端指令的持久化存储
  - 要求：该种方式只可以将parse方法的返回值存储到本地指定后缀的文本文件中。
  - 执行指令：`scrapy crawl spiderName -o fileName.csv`
  - 文件后缀有：('json', 'jsonlines', 'jl', 'csv', 'xml','marshal', 'pickle')
- 基于管道的持久化存储
  - 在爬虫文件中进行数据解析
  - 在items.py中定义相关属性
    - 步骤1中解析出了几个字段的数据，在此就定义几个属性
  - 在爬虫文件中将解析到的数据存储封装到Item类型的对象中
  - 将Item类型的对象提交给管道
  - 在管道文件(pipelines.py)中，接受爬虫嗯见提交过来的Item类型对象，且对其进行任意形式的持久化存储操作
  - 在配置文件中开启管道机制
- 基于管道实现数据的备份
  - 将爬取到的数据分别存储到不同的载体
  - 实现：将数据一份存储到mysql，一份存储到redis
  - 问题：管道文件中的一个管道类表示一个怎样的操作呢？
    - 一个管道类对应一种形式的持久化存储操作。如果将数据存储到不同的载体中，就需要使用多个管道类
  - 已经定义好了多个管道类，将数据写入到其载体中进行存储：
    - item会不会依次提交给多个管道类
      - 不会，爬虫文件中的item只会被提交给优先级最高的管道类
      - 优先级高的管道类需要在`process_item`函数中实现`return item`，将item传递给下一个优先级高的管道类

##### scrapy的手动请求发送实现的全站数据爬取

- `yield scrapy.Request(url,callback)`：GET请求
- `yield scrapy.FormRequest(url,callback,formdata)`：POST请求

##### - 为什么start_url列表中的url会被自动进行get请求的发送？

- 因为列表中的url其实是被`start_requsets`这个父类方法实现的get请求发送

##### - 如何将 `start_requsets`中的url默认进行post请求发送？

- 重写`start_requsets`方法即可

  ```python
  def start_requests(self):
  	for u in self.start_urls:
  		yield scrapy.FormRequest(url=u,callback=self.parse,formdata)
  ```

    

##### 五大核心组件工作流程：

- **引擎(Scrapy)**
  - 用来处理整个系统的数据流处理, 触发事务(框架核心)
- **调度器(Scheduler)**
  - 用来接受引擎发过来的请求, 压入队列中, 并在引擎再次请求的时候返回. 可以想像成一个URL（抓取网页的网址或者说是链接）的优先队列, 由它来决定下一个要抓取的网址是什么, 同时去除重复的网址
- **下载器(Downloader)**
  - 用于下载网页内容, 并将网页内容返回给蜘蛛(Scrapy下载器是建立在twisted这个高效的异步模型上的)
- **爬虫(Spiders)**
  - 爬虫是主要干活的, 用于从特定的网页中提取自己需要的信息, 即所谓的实体(Item)。用户也可以从中提取出链接,让Scrapy继续抓取下一个页面
- **项目管道(Pipeline)**
  - 负责处理爬虫从网页中抽取的实体，主要的功能是持久化实体、验证实体的有效性、清除不需要的信息。当页面被爬虫解析后，将被发送到项目管道，并经过几个特定的次序处理数据。

<img src="https://img-blog.csdn.net/20180416224202657?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzI4ODE3NzM5/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" alt="image-20200618001314586" style="zoom:80%;" />



##### 请求传参实现深度爬取：

- 深度爬取：爬取的数据没有在同一个页面中（首页+详情页数据）
- 在scrapy中如果没有请求传参，我们是无法进行持久化存储数据
- 实现方式：
  - scrapy.Request(url,callback,meta)
    - meta是一个字典，可以将meta传递给callback
  - callback取出meta：
    - response.meta['']

##### 中间件

- 作用：批量拦截请求和相应
- 爬虫中间件
- 下载中间件
  - 拦截请求
    - 篡改请求url
    - 伪装请求头信息
      - UA
      - Cookie
        - 注：scrapy已经自动帮程序处理好了cookie，一般情况不做设置
    - 设置请求代理
  - 拦截相应
    - 篡改相应数据
  - 代理操作必须使用中间件才可以实现
    - process_exception：
      - `request.mata['proxy'] = 'http://ip:port'`
      - return request：修正后重新发送

##### 大文件下载：大文件数据是在管道中请求到的

- 下属管道类是scrapy封装好的，可以直接使用
- 导入`from scrapy.pipelines.images import ImagesPipeline`，提供了数据下载功能(包括视音频)
- 重写该管道类的三个方法：
  - get_media_requests
    - 根据图片地址发起请求
  - file_path
    - 返回图片名称即可
  - item_completed
    - 返回item，将其返回给下一个即将执行的管道类
- 在setting配置文件中添加
  - `IMAGES_STORE = ‘dirName’`，即下载文件的文件夹

##### setting中的常用配置：增加scrapy爬取效率

- 增加并发：
  - 默认scrapy开启的并发线程为32个，可以适当进行增加。在settings配置文件中修改CONCURRENT_REQUESTS = 100值为100,并发设置成了为100。

- 降低日志级别：
  - 在使用scrapy crawl spiderFileName运行程序时，在终端里打印输出的就是scrapy的日志信息。
    - 日志信息的种类：
      - ERROR ： 一般错误
      - WARNING : 警告
      - INFO : 一般的信息
      - DEBUG ： 调试信息
      -  设置日志信息指定输出：
        - 在settings.py配置文件中，加入
          - LOG_LEVEL = ‘指定日志信息种类’即可。
          - LOG_FILE = 'log.txt'则表示将日志信息写入到指定文件中进行存储。
  - 在运行scrapy时，会有大量日志信息的输出，为了减少CPU的使用率。可以设置log输出信息为INFO或者ERROR即可。在配置文件中编写：LOG_LEVEL = ‘INFO’，LOG_LEVEL = ‘ERROR’

- 禁止cookie：
  - 如果不是真的需要cookie，则在scrapy爬取数据时可以进制cookie从而减少CPU的使用率，提升爬取效率。在配置文件中编写：COOKIES_ENABLED = ‘False’

- 禁止重试：
  - 对失败的HTTP进行重新请求（重试）会减慢爬取速度，因此可以禁止重试。在配置文件中编写：RETRY_ENABLED = ‘False’

- 减少下载超时：
  - 如果对一个非常慢的链接进行爬取，减少下载超时可以能让卡住的链接快速被放弃，从而提升效率。在配置文件中进行编写：DOWNLOAD_TIMEOUT = 10 超时时间为10s

##### CrawlSpider

- CrawlSpider是一个Spider的一个子类，Spider是爬虫文件中爬虫类的父类
  - 子类的功能一定多于父类
- 作用：被用作于专业实现全站数据爬取
  - 将一个页面下所有页码对应的数据进行爬取
- 基本使用：
  1. 创建一个工程
     - `scrapy startproject projectName`
  2. cd 工程
  3. 创建一个基于CrawlSpider的爬虫文件
     - `scrapy genspider -t crawl SpiderName www.xxx.com`
  4. 执行工程
     - `scrapy crawl SpiderName`
- 注意：
  - 一个链接提取器对应一个规则解析器(可以有多个)
  - 在实现深度爬取的过程中，需要和scrapyRequest()结合使用

##### CrawlSpider实现深度爬取

- 通用方式：CrawlSpider+Spider实现





##### selenium在scrapy中的使用

- 爬取网易新闻中的国内，国际，军事，航空，无人机这五个板块下所有的新闻数据(标题+内容)
- https://news.163.com/
- 分析
  - 每一个板块对应的页面中的新闻标题是动态加载的
    - **爬取新闻标题+详情页的url**
  - 每一条新闻详情页面中的数据不是动态加载
    - 爬取新闻内容
- selenium在scrapy中的使用流程
  1. 在爬虫类中实例化一个浏览器对象，将其作为爬虫类的一个属性
  2. 在中间件中实现浏览器自动化相关的操作
  3. 在爬虫类中重写`closed(self,spider)`，在其内部关闭浏览器对象



##### 分布式

- 实现方式：scrapy+redis(scrapy结合着scrapy-redis组件)

  - 安装：
    - `pip install scrapy_redis`

- 原生的scrapy是无法实现分布式的
  - 什么是分布式
    - 需要搭建一个分布式的机群，然后让机群中的每一台电脑执行同一组程序，让其对同一组资源进行**联合**且**分布**的数据爬取
  - 为什么原生的scrapy框架无法实现分布式：
    - 调度器无法被分布式机群共享
      - 多台机器上部署的scrapy会各自拥有各自的调度器，这样就使得多台机器无法分配start_urls列表中的url
    - 管道无法被分布式机群共享
      - 多台机器爬取到的数据无法通过同一个管道对数据进行统一的数据持久化存储
  - 如何实现分布式：使用scrapy-redis组件即可
  - scrapy-redis组件的作用：
    - 可以给原生的scrapy框架提供共享的管道和调度器

- 实现流程：

  1. 修改爬虫文件

     - 导包：`from scrapy_redis.spiders import RedisCrawlSpider`
     - 修改当前爬虫类的父类为：`RedisCrawlSpider`
     - 将`start_urls`替换成`redis_key`的属性，属性值为任意字符串
       - `redis_key='xxx'`:表示的是可以被共享的调度器队列的名称，最终是需要将起始的url手动放置到`redis_key`表示的队列中
     - ：将数据解析的操作补充完整

  2. 对`seetting.py`进行配置

     - 指定调度器

       - 添加到setting.py文件中

       - ```python
         # 使用scrapy-redis组件的去重队列
         # 增加了一个去重容器类的配置，使用redis的set集合类存储请求的指纹数据，从而实现请求去重
         DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
         # 使用scrapy-redis组件自己的调度器
         SCHEDULER = "scrapy_redis.scheduler.Scheduler"
         # 配置调度器是否要持久化，也就是当爬虫结束后，要不要清空Redis中请求队列和去重指纹的set。为True，就表示要持久化存储，就不清空数据，否则清空数据。
         SCHEDULER_PERSIST = True
         ```

     - 指定管道

       - ```
         开启使用scrapy-redis组件中封装好的管道(直接用)
         ```

       - ```python
         ITEM_PIPELINES = {
             'scrapy_redis.pipelines.RedisPipeline': 400
         }
         ```

         - 特点：这种管道只可以将item写入redis(即不能写入mysql或写入本地文件)

     - 指定redis

       - ```python
         REDIS_HOST = 'redis服务的ip地址'
         REDIS_PORT = 6379
         REDIS_ENCODING = ‘utf-8’
         REDIS_PARAMS = {‘password’:’123456’}
         ```

  3. 配置redis的配置文件 (redis.window.conf)

     - 解除默认绑定（视redis版本而定）
       - #bind 127.0.0.1 （注释掉）
     - 关闭保护模式
       - protected-mode no

  4. 启动redis服务和客户端

  5. 执行scrapy工程（不要在配置文件中加入LOG_LEVEL）

     - 执行后，程序会停留在listening位置：等待**起始url**加入

  6. 向redis_key表示的队列中添加**起始url**

     - 需要在redis 客户端执行如下指令：（调度器队列是存在于redis中）
       - `lpush redis_key的值 www.xxx.com`
       - `lpush sunQueue http://wz.sun0769.com/political/index/politicsNewest?id=1&page=1`

##### 增量式

- 概念：监测网站数据更新的情况，以便于爬取到最新更新出来的数据
- 实现核心：**去重**
- 实战中的去重方式：记录表
  - 记录表需要记录什么？记录的一定是爬取过的相关信息（能唯一标识一部电影）
    - 爬取过的相关信息：每一部电影详情页的url
    - 可以表示一部电影唯一标识的数据称为：**数据指纹**
      - 数据指纹一般是经过加密的
        - 什么情况数据需要加密：如果数据的唯一标识标识的内容数据量较大，可以使用**hash**将数据加密成32位的密文，从而节省空间
- 去重的方式对应的记录表：
  - python中的set集合（不可以）
    - set集合无法持久化存储，其内容会随着程序的中断而清空
  - redis中的set可以
    - 可以持久化存储
  - 即：需要满足能去重、能持久化存储两个需求