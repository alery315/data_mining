# 文本分类

自己爬了一些数据,加上下载的数据,拼起来差不多100W左右

用到了tf_idf,卡方检验,朴素贝叶斯分类,svm分类

* spider里面是几个爬虫,有微博热门,京东评价,头条新闻,新浪滚动新闻
* main_control: 入口(其实没什么用,每一步结果都有保存)
* config: 文件路径的设置
* split_file_to_small, split_sohu_data, due_process: 预处理相关,分割文件,统计数量,去除一些css代码等等
* corpus_segment: 分词,去除停用词,选取训练集和测试集相关
* chi_square: 计算卡方并提取特征词
* save_to_bunch: 将数据存到bunch中
* word_vector_space: 计算并保存tf_idf词向量空间
* naive_bayes: 调库的朴素贝叶斯
* manual_naive_bayes: 手写的朴素贝叶斯
* svm: 调库的svm分类器,并用网格搜索最佳参数
* tf_idf: 这个单独计算tf_idf,和上面的参数不一样.
* process_THU_news: 从下载的清华数据集提取一些数据

