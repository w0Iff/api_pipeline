from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'osoba'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    cameras = db.relationship('Kamera', backref='osoba', lazy=True, cascade="all, delete-orphan")
    relationships = db.relationship('Znajomosc',
                                    foreign_keys="[Znajomosc.user_id_1, Znajomosc.user_id_2]",
                                    primaryjoin="(User.id == Znajomosc.user_id_1) | (User.id == Znajomosc.user_id_2)",
                                    backref='osoba', lazy=True, cascade="all, delete-orphan")


class Kamera(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('osoba.id'), nullable=False)


class Znajomosc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id_1 = db.Column(db.Integer, db.ForeignKey('osoba.id'), nullable=False)
    user_id_2 = db.Column(db.Integer, db.ForeignKey('osoba.id'), nullable=False)


with app.app_context():
    print("Sukces! Polaczono.")
    db.create_all()


@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data.get('name')
    phone_number = data.get('phone_number')

    user = User(name=name, phone_number=phone_number)
    db.session.add(user)
    db.session.commit()

    return jsonify({'sukces': 'Sukces! Osoba dodana.'})


@app.route('/view_users', methods=['GET'])
def view_users():
    users = User.query.all()
    user_list = [{'Osoba': user.name, 'Numer Telefonu': user.phone_number} for user in users]
    return jsonify({'osoby': user_list})


@app.route('/add_camera', methods=['POST'])
def add_camera():
    data = request.get_json()
    user_id = data.get('user_id')

    camera = Kamera(user_id=user_id)
    db.session.add(camera)
    db.session.commit()

    return jsonify({'sukces': 'Sukces! Kamera zostala dodana.'})


@app.route('/add_friend', methods=['POST'])
def add_friend():
    try:
        data = request.get_json()
        user_id_1 = data.get('user_id_1')
        user_id_2 = data.get('user_id_2')

        user1 = User.query.get(user_id_1)
        user2 = User.query.get(user_id_2)

        if not user1 or not user2:
            return jsonify({'blad': 'Jedna lub wiecej osob nie istnieje.'})

        if not user1.cameras and not user2.cameras:
            return jsonify({'blad': 'Przynajmniej jedna osoba musi posiadac kamere żeby utworzyc znajomosc.'})

        existing_friendship = Znajomosc.query.filter(
            ((Znajomosc.user_id_1 == user_id_1) & (Znajomosc.user_id_2 == user_id_2)) |
            ((Znajomosc.user_id_1 == user_id_2) & (Znajomosc.user_id_2 == user_id_1))
        ).first()

        if existing_friendship:
            return jsonify({'blad': 'Znajomosc juz istnieje.'})

        new_friendship = Znajomosc(user_id_1=user_id_1, user_id_2=user_id_2)
        db.session.add(new_friendship)
        db.session.commit()

        return jsonify({'sukces': 'Sukces! Znajomosc zostala dodana.'})
    except Exception as e:
        return jsonify({'blad': str(e)})


@app.route('/find_user_with_camera', methods=['GET'])
def find_user_with_camera():
    try:
        nazwa_osoby = request.args.get('nazwa_osoby')

        user_x = User.query.filter_by(name=nazwa_osoby).first()

        if not user_x:
            return jsonify({'blad': 'Nie znaleziono osoby.'})

        if user_x.cameras:
            return jsonify({'nazwa_osoby': user_x.name, 'numer_telefonu': user_x.phone_number, 'ma_kamere': True})

        friends_with_cameras = db.session.query(User).join(Znajomosc, (Znajomosc.user_id_1 == User.id) | (Znajomosc.user_id_2 == User.id)).filter((Znajomosc.user_id_1 == user_x.id) | (Znajomosc.user_id_2 == user_x.id)).filter(User.cameras.isnot(None)).all()

        if friends_with_cameras:
            friend_with_camera = friends_with_cameras[0]
            return jsonify({'nazwa_osoby': friend_with_camera.name, 'numer_telefonu': friend_with_camera.phone_number, 'ma_kamere': True})
        else:
            return jsonify({'blad': 'Nie znaleziono znajomych z kamera'})

    except Exception as e:
        return jsonify({'blad': str(e)})


@app.route('/browse_users', methods=['GET'])
def browse_users():
    znajomosci = Znajomosc.query.all()
    znajomosci_list = [{'user_id_1': znajomosc.user_id_1, 'user_id_2': znajomosc.user_id_2} for znajomosc in znajomosci]
    return jsonify({'znajomosci': znajomosci_list})


@app.route('/check_user_name_palindrome', methods=['POST'])
def check_user_name_palindrome():
    try:
        data = request.get_json()
        nazwa_osoby = data.get('nazwa_osoby')

        cleaned_user_name = ''.join(char.lower() for char in nazwa_osoby if char.isalnum())

        is_palindrome = cleaned_user_name == cleaned_user_name[::-1]

        return jsonify({'nazwa_osoby': nazwa_osoby, 'is_palindrome': is_palindrome})
    except Exception as e:
        return jsonify({'blad': str(e)})


def quicksort_users(users):
    if len(users) <= 1:
        return users
    pivot = users[len(users) // 2]
    less = [user for user in users if user.id < pivot.id]
    equal = [user for user in users if user.id == pivot.id]
    greater = [user for user in users if user.id > pivot.id]
    return quicksort_users(less) + equal + quicksort_users(greater)


@app.route('/sort_users', methods=['GET'])
def sort_users():
    try:
        users = User.query.all()

        sorted_users = quicksort_users(users)

        sorted_user_list = [{'id': user.id, 'name': user.name, 'numer_telefonu': user.phone_number} for user in sorted_users]

        return jsonify({'Lista osob po sortowaniu': sorted_user_list})
    except Exception as e:
        return jsonify({'blad': str(e)})


@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user_to_delete = User.query.get(user_id)

        if not user_to_delete:
            return jsonify({'blad': 'Nie znaleziono osoby.'})

        db.session.delete(user_to_delete)
        db.session.commit()

        return jsonify({'sukces': 'Sukces! Osoba zostala usunieta.'})
    except Exception as e:
        return jsonify({'blad': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
