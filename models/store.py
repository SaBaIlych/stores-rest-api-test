from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'
    # SQLAlchemy does a bit of magic there: items defines the column. 
    # Whenever you create an instance, SQLAlchemy (via the db.Model superclass) adds properties to the object; 
    # one per column in the row that belongs to this instance.

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic', back_populates = 'store') # if we remove lazy, items will fetch all items automatically ->
                                                        # when you create object; if we leave lazy, items will fetch by function all()

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'id': self.id, 'name': self.name, 'items': [item.json() for item in self.items.all()]} # not unit test because of self.items( using database)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
