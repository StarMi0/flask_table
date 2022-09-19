import os

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Data_table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(50), unique=True)
    amount = db.Column(db.Integer, nullable=False)
    distance = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Tables {self.date} {self.name} {self.amount} {self.distance}>'


cols_dict = {
    'date': Data_table.date,
    'name': Data_table.name,
    'amount': Data_table.amount,
    'distance': Data_table.distance,
}


def cond_func(col_name, val, cond):
    page = request.args.get('page', 1, type=int)
    val_ = val_condition(col_name, val)
    if cond == '=':
        filtered = Data_table.query.filter(cols_dict[col_name] == val_).paginate(
            page, per_page=10)
    elif cond == 'contain':
        filtered = Data_table.query.filter(cols_dict[col_name].in_([val_])).paginate(
            page, per_page=10)
    elif cond == '>':
        filtered = Data_table.query.filter(cols_dict[col_name] > val_).paginate(
            page, per_page=10)
    elif cond == '<':
        filtered = Data_table.query.filter(cols_dict[col_name] < val_).paginate(
            page, per_page=10)
    return filtered


def val_condition(col_name, val):
    if col_name == 'name' or col_name == 'date':
        e_val = str(val)
    else:
        e_val = int(val)
    return e_val


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    1. Выбор колонки, по которой будет фильтрация
    2. Выбор условия (равно, содержит, больше, меньше)
    3. Поле для ввода значения для фильтрации
    :return:
    """
    get_col = request.form.get('coll')
    get_con = request.form.get('condition')
    get_val = request.form.get('value')
    page = request.args.get('page', 1, type=int)
    if request.method == 'POST':
        pagination = cond_func(get_col, get_val, get_con)
        return render_template('index.html', pagination=pagination)
    else:
        pagination = Data_table.query.order_by(Data_table.id).paginate(
            page, per_page=10)
        return render_template('index.html', pagination=pagination)
