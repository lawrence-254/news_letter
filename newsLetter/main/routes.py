from flask import Blueprint

main = Blueprint('main', __name__)



# '''Home route section'''
@main.route("/")
@main.route("/home/")
def home():
    '''Home route section'''
    page = request.args.get('page', 1, type=int)
    posts= Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)
    return render_template('home.html', posts=posts, title='Home')
# '''end of home route'''

# '''about route'''
@main.route("/about/")
def about():
    '''about route'''
    return render_template('about.html', title='About')


