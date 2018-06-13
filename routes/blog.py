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
)


from models import Pagination

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
    count = Post.count()
    all_posts = Post.page_post(all_posts, skip=start, limit=PAGE_COUNT)
    pagination = Pagination(page, PAGE_COUNT, count)
    return render_template('blog/index.html', posts=all_posts, pagination=pagination, tags=Tags.all())


#/blog/1
@blog.route("/post/<int:blog_id>", methods=["GET"])
def post(blog_id):
    comments = PostComment.find_all(blog_id=blog_id)
    blog = Post.find(blog_id)
    return render_template("blog_view.html", blog=blog, comments = comments)


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