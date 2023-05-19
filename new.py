from flask import Flask, render_template, request, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
import random

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with your own secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.sqlite3'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    player = db.relationship('Player', backref='user', uselist=False)


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)

    def get_points_earned(self):
        return self.level * 100


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_first_request
def create_tables():
    db.create_all()


def generate_sudoku_grid():
    # Generate a random Sudoku grid
    # You can implement your own logic to generate a Sudoku grid here
    # This example generates a partially-filled Sudoku grid
    grid = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    # Randomly remove some values to create the puzzle
    for i in range(3):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        grid[row][col] = 0

    return grid


def validate_sudoku_solution(values):
    # Validate the Sudoku solution
    # You can implement your own logic to validate the solution here
    # This example checks if the values match the pre-generated Sudoku grid
    solution_grid = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9]
    ]

    for i in range(9):
        for j in range(9):
            if values[i * 9 + j] != solution_grid[i][j]:
                return False

    return True


@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect('/level1')
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)

            # Check if player object exists, create one if not
            if not user.player:
                player = Player(name=username, user=user)
                db.session.add(player)
                db.session.commit()

            return redirect('/level1')
        else:
            flash('Invalid username or password', 'error')
            return redirect('/login')

    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/register', methods=['GET'])
def register_get():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    new_username = request.form['new_username']
    new_password = request.form['new_password']

    # Check if the username already exists
    existing_user = User.query.filter_by(username=new_username).first()
    if existing_user:
        flash('Username already exists. Please choose a different username.', 'error')
        return render_template('register.html')  # Render the registration form again with the error message

    # Create a new user in the database
    user = User(username=new_username, password=new_password)
    db.session.add(user)
    db.session.commit()

    flash('User registered successfully!', 'success')
    return redirect('/login')


@app.route('/level1')
@login_required
def level1():
    # Generate a Sudoku grid
    sudoku_grid = generate_sudoku_grid()

    return render_template('level1.html', sudoku_rows=sudoku_grid)


@app.route('/validate_solution', methods=['POST'])
def validate_solution():
    data = request.json
    values = data.get('values')

    # Validate the solution (you need to implement this logic)
    valid_solution = validate_sudoku_solution(values)

    return jsonify({'valid': valid_solution})


if __name__ == '__main__':
    app.run(debug=True)
