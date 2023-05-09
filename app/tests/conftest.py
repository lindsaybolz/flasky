import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.crystal import Crystal


@pytest.fixture
def app():
    app = create_app(test_config={"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def two_saved_crystals():
    pearl = Crystal(name='Pearl', powers='Pretty Powers', color='White')
    garnet = Crystal(name='Garnet', powers='Awesomeness', color='Red')

    db.session.add_all([pearl, garnet])
    db.session.commit()

    