from flask import Flask, request, render_template
from flask_wtf.csrf import CSRFProtect

from form import RegistrationForm
from model import db, User
# import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = '0141a3d56499a0eb9bd35f712a5c766b30734274007f99f448ffcfe5be917d16'
csrf = CSRFProtect(app)
"""
Генерация надежного секретного ключа
>>> import secrets
>>> secrets.token_hex()
"""
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///userbase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        password = form.password.data

        exist_user = User.query.filter(
            (User.firstname == firstname) or (User.lastname == lastname) or (User.email == email)
        ).first()
        if exist_user:
            error_msg = 'Username or email already exists.'
            form.firstname.errors.append(error_msg)
            return render_template('register.html', form=form)
        new_user = User(firstname=firstname, lastname=lastname,
                        email=email)
        new_user.set_pass(password)
        db.session.add(new_user)
        db.session.commit()
        success_msg = 'Registration successful!'
        return success_msg
    return render_template('register.html', form=form)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
    # print(secrets.token_hex())