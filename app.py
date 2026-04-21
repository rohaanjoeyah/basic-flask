import os
from dotenv import load_dotenv
from flask import Flask, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_user, current_user
from functools import wraps

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'default_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///secure_app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)

Talisman(app, content_security_policy=None, force_https=False)

limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return '<h1>Secure App</h1><a href="/login">Login</a> | <a href="/upload">Upload</a> | <a href="/admin/dashboard">Admin</a>'

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        return "Invalid credentials."
    
    return '''
    <form method="POST">
        <input type="hidden" name="csrf_token" value="{}">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Login</button>
    </form>
    '''.format(generate_csrf())

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return f'File {filename} successfully uploaded!'
        return 'Invalid file type.'
        
    return '''
    <form method="POST" enctype="multipart/form-data">
        <input type="hidden" name="csrf_token" value="{}">
        <input type="file" name="file" required>
        <button type="submit">Upload</button>
    </form>
    '''.format(generate_csrf())

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    return "<h1>Admin Dashboard</h1><p>Only admins can view this page.</p>"

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    with app.app_context():
        db.create_all()
        # Create default admin and user for testing if DB is empty
        if not User.query.first():
            hashed_pw = bcrypt.generate_password_hash('password123').decode('utf-8')
            admin = User(username='admin', password=hashed_pw, is_admin=True)
            normal_user = User(username='user', password=hashed_pw, is_admin=False)
            db.session.add_all([admin, normal_user])
            db.session.commit()
    app.run(debug=True)