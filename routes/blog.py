from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
    current_app,
    jsonify,
)


from models.blog import (
    Post,
    PostComment,
    Tags,
    Reply,
)


from models import Pagination
from models.user import User
from utils import log


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


# /blog/1
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


@blog.route('/post/new', methods=('GET', 'POST'))
@blog.route('/post/change/<int:post_id>', methods=('GET', 'POST'))
def new(post_id=None):
    # 渲染new.html页面
    if request.method == 'GET':
        p = None
        if post_id: # 如果post_id不为None,则是修改页面；否则为新建页面
            p = Post.find(id=post_id)
            if not p:
                abort(404)
        return render_template('blog/new.html', post=p, tags=Tags.all())
    else:
        log('request.form:{}'.format(request.form))
        post = Post.new({})
        post.title = request.form['title']
        post.content = request.form['content']  # 这里标签需要重新初始化，这是一个bug
        str_tids = request.form['tids']  # 从文件中读出的问题，获得的格式为'[1，2]'，需要的格式为[1，2]
        str_tids = str_tids.split(' ')
        list_tids = []
        for i in range(len(str_tids)-1):
            list_tids.append(int(str_tids[i]))
        post.tids = list_tids
        log('post.title:{} post.content:{} post.tids:{}'.format(post.title, post.content, post.tids))

        # 新建博客
        if not post_id:
            post.author = 'admin'
            post.save()  # 更新信息
            post_id = post.id
            current_app.logger.info('Successfully new a post {}'.format(post_id))
        # 修改博客
        else:
            exist_post = Post.find(id=post_id)
            exist_post.title = post.title
            exist_post.content = post.content
            exist_post.tids = post.tids
            exist_post.save()
            Post.delete(id=post.id)
            current_app.logger.info('Successfully change a post {}'.format(exist_post.id))

    return jsonify(success=True, message='Save the post successfully.', pid=str(post_id))


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
