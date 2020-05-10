import datetime

import requests
from flask import Flask, render_template, redirect, request, abort, jsonify, make_response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_restful import abort, Api

import jobs_api
import jobs_resources
import users_api
import users_resources
from data import db_session
from data.categories import CategoryJob
from data.departments import Department
from data.jobs import Jobs
from data.users import User
from forms import RegisterForm, LoginForm, JobForm, DepForm

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return render_template("jobs.html", title="Mars Colonization", jobs=jobs)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Sign in', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('registration.html', title='Sign up', form=form)


@app.route("/new_job", methods=['GET', 'POST'])
@login_required
def new_job():
    form = JobForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        job = Jobs()
        job.job = form.title.data
        job.team_leader = form.leader_id.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        job.creator = current_user.id

        category_id = form.category.data
        category = session.query(CategoryJob).filter(CategoryJob.id == category_id).first()
        job.categories.append(category)
        session.commit()

        try:
            current_user.jobs.append(job)
        except:
            pass
        session.merge(current_user)
        session.commit()
        return redirect('/')
    return render_template('new_job.html', title='New job', form=form)


@app.route('/new_job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = JobForm()
    if request.method == "GET":
        session = db_session.create_session()
        if current_user.id == 1:
            job = session.query(Jobs).filter(Jobs.id == id).first()
        else:
            job = session.query(Jobs).filter(Jobs.id == id,
                                             Jobs.creator == current_user.id).first()
        if job:
            form.title.data = job.job
            form.leader_id.data = job.team_leader
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.is_finished.data = job.is_finished
            form.category.data = job.categories[0].id
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        if current_user.id == 1:
            job = session.query(Jobs).filter(Jobs.id == id).first()
        else:
            job = session.query(Jobs).filter(Jobs.id == id,
                                             Jobs.creator == current_user.id).first()
        if job:
            job.job = form.title.data
            job.team_leader = form.leader_id.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.is_finished = form.is_finished.data

            category_id = form.category.data
            category = session.query(CategoryJob).filter(CategoryJob.id == category_id).first()
            job.categories[0] = category

            try:
                current_user.jobs.append(job)
            except:
                pass

            session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('new_job.html', title='Job edit', form=form)


@app.route('/delete_job/<int:id>', methods=['GET', 'POST'])
@login_required
def job_delete(id):
    session = db_session.create_session()
    if current_user.id == 1:
        job = session.query(Jobs).filter(Jobs.id == id).first()
    else:
        job = session.query(Jobs).filter(Jobs.id == id,
                                         Jobs.creator == current_user.id).first()
    if job:
        session.delete(job)
        session.commit()
    else:
        abort(404)
    return redirect('/')


@app.route("/departments")
def departments():
    session = db_session.create_session()
    deps = session.query(Department).all()
    return render_template("departments.html", title="List of Departments", deps=deps)


@app.route('/new_dep', methods=['GET', 'POST'])
@login_required
def new_dep():
    form = DepForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        dep = Department()
        dep.title = form.title.data
        dep.chief = form.chief_id.data
        dep.members = form.members.data
        dep.email = form.email.data
        dep.creator = current_user.id
        chief = session.query(User).filter(User.id == form.chief_id.data).first()
        chief.deps.append(dep)
        session.merge(current_user)
        session.commit()
        return redirect('/departments')
    return render_template('new_dep.html', title='New Department',
                           form=form)


@app.route('/new_dep/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_dep(id):
    form = DepForm()
    if request.method == "GET":
        session = db_session.create_session()
        if current_user.id == 1:
            dep = session.query(Department).filter(Department.id == id).first()
        else:
            dep = session.query(Department).filter(Department.id == id,
                                                   Department.creator == current_user.id).first()
        if dep:
            form.title.data = dep.title
            form.chief_id.data = dep.chief
            form.members.data = dep.members
            form.email.data = dep.email
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        if current_user.id == 1:
            dep = session.query(Department).filter(Department.id == id).first()
        else:
            dep = session.query(Department).filter(Department.id == id,
                                                   Department.creator == current_user.id).first()
        if dep:
            dep.title = form.title.data
            dep.chief = form.chief_id.data
            dep.members = form.members.data
            dep.email = form.email.data
            session.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('new_dep.html', title='Department edit', form=form)


@app.route('/delete_dep/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_dep(id):
    session = db_session.create_session()
    if current_user.id == 1:
        dep = session.query(Department).filter(Department.id == id).first()
    else:
        dep = session.query(Department).filter(Department.id == id,
                                               Department.creator == current_user.id).first()
    if dep:
        session.delete(dep)
        session.commit()
    else:
        abort(404)
    return redirect('/departments')


@app.route("/users_show/<int:user_id>", methods=['GET'])
def users_show(user_id):
    def get_coordinates_from_address(address):
        import requests

        geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={address}&format=json"

        response = requests.get(geocoder_request)
        if response:
            json_response = response.json()

            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0][
                "GeoObject"]
            toponym_coodrinates = toponym["Point"]["pos"]
            return toponym_coodrinates
        else:
            print("Ошибка выполнения запроса:")
            print(geocoder_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")

    def make_image_from_coordinates(coords):
        global k
        map_params = {
            'll': ','.join(coords.split()),
            'z': 12,
            'l': 'sat',
            'api_key': '40d1649f-0493-4b70-98ba-98533de7710b'
        }
        map_request = f"https://static-maps.yandex.ru/1.x/"
        response = requests.get(map_request, params=map_params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(response.url)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            abort(404)

        map_file = 'static/img/city.png'
        with open(map_file, "wb") as file:
            file.write(response.content)

    request = f'http://127.0.0.1:8080/api/users/{user_id}'
    user = requests.get(request).json()
    if 'error' in user:
        abort(404)

    make_image_from_coordinates(get_coordinates_from_address(user['user']['city_from']))

    return render_template("city.html", city=user['user']['city_from'],
                           name=user['user']['name'], surname=user['user']['surname'])


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(500)
def value_error(error):
    return make_response(jsonify({'error': 'ValueError'}), 500)


if __name__ == '__main__':
    db_session.global_init("db/mars_one.sqlite")
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    api.add_resource(users_resources.UsersListResource, '/api/v2/users')
    api.add_resource(users_resources.UserResource, '/api/v2/users/<int:user_id>')
    api.add_resource(jobs_resources.JobsListResource, '/api/v2/jobs')
    api.add_resource(jobs_resources.JobResource, '/api/v2/jobs/<int:job_id>')
    app.run(port=8080, host='127.0.0.1')
    app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
