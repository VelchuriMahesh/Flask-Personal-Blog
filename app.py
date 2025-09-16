# ---------------------------------------------------------------------------- #
#                                    IMPORTS                                   #
# ---------------------------------------------------------------------------- #
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# ---------------------------------------------------------------------------- #
#                                 APP SETUP                                    #
# ---------------------------------------------------------------------------- #

app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance/blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------------------------------------------------------------------------- #
#                              CONTEXT PROCESSOR                               #
# ---------------------------------------------------------------------------- #

@app.context_processor
def inject_now():
    """Injects the current year into all templates for the footer."""
    return {'now': datetime.utcnow()}

# ---------------------------------------------------------------------------- #
#                                DATABASE MODEL                                #
# ---------------------------------------------------------------------------- #

class Post(db.Model):
    """Defines the Post database model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50), nullable=False, default='Anonymous')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # --- NEW ---
    # This is the new column to store the image URL.
    # It is nullable=True, which means it's optional.
    image_url = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"Post('{self.id}', '{self.title}')"

# ---------------------------------------------------------------------------- #
#                                    ROUTES                                    #
# ---------------------------------------------------------------------------- #

@app.route('/')
def index():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        
        # --- NEW --- Get the image URL from the form data
        image_url = request.form['image_url']

        # Create a new Post instance, now including the image_url
        new_post = Post(title=title, content=content, author=author, image_url=image_url)
        
        db.session.add(new_post)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    return render_template('create.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post_to_edit = Post.query.get_or_404(id)
    
    if request.method == 'POST':
        post_to_edit.title = request.form['title']
        post_to_edit.content = request.form['content']
        post_to_edit.author = request.form['author']
        
        # --- NEW --- Update the image_url field from the form data
        post_to_edit.image_url = request.form['image_url']
        
        db.session.commit()
        
        return redirect(url_for('post', id=post_to_edit.id))
        
    return render_template('edit.html', post=post_to_edit)

@app.route('/delete/<int:id>')
def delete(id):
    post_to_delete = Post.query.get_or_404(id)
    
    db.session.delete(post_to_delete)
    db.session.commit()
    
    return redirect(url_for('index'))

# ---------------------------------------------------------------------------- #
#                                APP EXECUTION                                 #
# ---------------------------------------------------------------------------- #

if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists('instance'):
            os.makedirs('instance')
        # This will create the database and tables if they don't exist.
        db.create_all()

    app.run(debug=True)