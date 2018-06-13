from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)


from models.blog import (
    Post,
    PostComment,
    Tags,
    Reply,
)


from models import Pagination
from models.user import User


# 创建一个 蓝图对象 并且路由定义在蓝图对象中
# 然后在 flask 主代码中「注册蓝图」来使用
# 第一个参数是蓝图的名字, 以后会有用(add函数里面就用到了)
# 第二个参数是套路
blog = Blueprint('blog', __name__)
PAGE_COUNT = 5   # 每页显示5条博客


@blog.route("/")
@blog.route("/index")
def index():
    """
    Index.
    """
    tid = request.args.get('t', None)
    page = int(request.args.get('p', 1))
    start = (page - 1) * PAGE_COUNT
    if tid is not None:
        all_posts = Post.find_tags(tids=tid)
    else:
        all_posts = Post.all()
    count = Post.count(all_posts)
    all_posts = Post.page_post(all_posts, skip=start, limit=PAGE_COUNT)
    pagination = Pagination(page, PAGE_COUNT, count)
    return render_template('blog/index.html', posts=all_posts, pagination=pagination, tags=Tags.all())


#/blog/1
@blog.route("/post/<int:blog_id>", methods=["GET"])
def post(blog_id):
    # comments = PostComment.find_all(blog_id=blog_id)
    # blog = Post.find(blog_id)
    p = Post.find(id=blog_id)
    # 获得该博客的评论
    comments = PostComment.find_all(post_id=blog_id)
    uids = set()
    for c in comments:
        uids.add(c.uid)
        for r in Reply.find_all(comment_id=c.id):
            uids.add(r.uid)
    user_dict = {}
    for uid in list(uids):
        u = User.find(id=uid)
        user_dict[u.id] = u
    return render_template('blog/post.html', id=blog_id, post=p,tags=Tags.all(), Replay=Reply,
                           comments=comments, user_dict=user_dict)


@blog.route("/post/new", methods=["GET"])
def new():
    return render_template("blog_new.html")

@blog.route("/add", methods=["POST"])
def add():
    form = request.form
    Post.new(form)
    return redirect(url_for('.index'))


@blog.route("/comment/new", methods=["POST"])
def comment():
    form = request.form
    PostComment.new(form)
    return redirect(url_for('.view', blog_id=form.get("blog_id")))