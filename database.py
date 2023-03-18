class Watchlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mediaID = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(300), nullable=False)



    def __rep__(self):
        return '<Task %r>' % self.id

class TodoExpanded(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)
    watched = db.Column(db.Boolean())
    release_date = db.Column(db.DateTime(timezone=True))
    created_date_UTC = db.Column(db.DateTime(timezone=True), default=func.now())

    def __rep__(self):
        return '<Task %r>' % self.id