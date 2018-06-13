import time
from .model import Model
from utils import log
"""
博客model设计：
1）Tags：标签类
2）Post：博文类
3）PostComment：评论类
"""


class Tags(Model):  # 标签属性
    def __init__(self, form):
        self.id = None                          # 标签ID
        self.name = form.get('name', '')      # 标签名称
        self.weight = int(form.get('weight', 0))  # 标签对应博文数量
        self.create_time = int(time.time())     # 创建时间

    @classmethod
    def find_name(cls, id):
        """
        获得对应标签id的名称
        """
        m = cls.find(id)
        return m.name


class Post(Model):  # 博客文章数据属性
    def __init__(self, form):
        self.id = None                          # 博文ID
        self.title = form.get('title', '')      # 标题
        self.content = form.get('content', '')  # 内容
        self.tids = form.get('tids', '[]')  # 标签ID列表
        self.author = form.get('author', '')    # 作者
        self.create_time = int(time.time())     # 创建时间
        self.update_time = form.get('update_time', self.create_time)  # 更新时间

    @classmethod
    def find_tags(cls, **kwargs):
        """
        find_tags: 传入标签id，返回有该标签属性的博文
        """
        ms = []
        log('kwargs, ', kwargs, type(kwargs))
        k, v = '', -1
        for key, value in kwargs.items():
            k, v = key, int(value)
        all = cls.all()
        for m in all:
            # 也可以用 getattr(m, k) 取值
            if v in m.__dict__[k]:
                ms.append(m)
        return ms

    @classmethod
    def count(cls, all_post):
        return len(all_post)

    @classmethod
    def page_post(cls, all_posts, skip, limit):
        start = skip
        end = skip + limit
        if end > len(all_posts):
            ms = all_posts[start:]
        else:
            ms = all_posts[start:end]
        log('all_posts:{} start:{} end:{} len(ms):{}'.format(len(all_posts), start, end, len(ms)))
        return ms


class PostComment(Model):  # 博客评论数据属性
    def __init__(self, form):
        self.id = None
        self.content = form.get('content', '')
        self.author = form.get('author', '')
        self.post_id = int(form.get('post_id', 0))
        self.create_time = int(time.time())
        self.uid = form.get('uid', '')


class Reply(Model):  # 评论属性
    def __init__(self, form):
        self.id = None
        self.comment_id = form.get('comment_id', '') # 对应评论的回复
        self.uid = form.get('uid', '') # 发表回复的人
        self.rid = form.get('rid', '')  # 接受回复的人
        self.content = form.get('content', '')  # 内容
        self.create_time = int(time.time())  # 创建时间
