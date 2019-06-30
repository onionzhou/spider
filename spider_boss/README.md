*   默认IP代理没有开启，如果需要开启,settings.py中 取消相关注释
*   下载载数据默认存储到monogdb中，若需要存储在其他地方，请在(pipelines.py)管道文件中修改相关存储位置

###执行方式：
* 指定user_agent执行
  *  $ scrapy crawl zhipin -s USER_AGENT='Mozilla/5.0'

* 默认执行 
     * $ scrapy crawl zhipin_test 

* python 执行方式 
   * python3 main.py 


###注意

*   scrapy crawl zhipin_test  爬取得测试相关的职位
*   scrapy crawl zhipin  爬取得python相关的职位
