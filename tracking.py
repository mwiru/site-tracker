import datetime

from os.path import abspath, dirname, join

from flask import flash, Flask, Markup, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import fields
from wtforms_alchemy.fields import QuerySelectField

_cwd = dirname(abspath(__file__))

# set up some configurations
SECRET_KEY = 'This-is-it-for-me'
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:@localhost/sitetracker_db'
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_SECRET_KEY = 'this-should-be-more-than-it'


app = Flask(__name__)
app.config.from_object(__name__)

db = SQLAlchemy(app)


# set up our models
class Site(db.Model):
	__tablename__ = 'site_tracker'

	id = db.Column(db.Integer, primary_key=True)
	base_url = db.Column(db.String)
	visits = db.relationship('Visit', backref='site_tracker', lazy='select')

	def __repr__(self):
		return '<Site %r>' % (self.base_url)

	def __str__(self):
		return self.base_url


class Visit(db.Model):
	__tablename__ = 'tracking_visit'

	id = db.Column(db.Integer, primary_key=True)
	browser = db.Column(db.String)
	date = db.Column(db.DateTime)
	event = db.Column(db.String)
	url = db.Column(db.String)
	ip_address = db.Column(db.String)
	site_id = db.Column(db.Integer, db.ForeignKey('site_tracker.id'))

	def __repr__(self):
		return '<Visit %r - %r>' % (self.url, self.date)


# set up forms
class VisitForm(FlaskForm):
	browser = fields.StringField()
	date = fields.DateField()
	event = fields.StringField()
	url = fields.StringField()
	ip_address = fields.StringField("IP Address")
	site = QuerySelectField(query_factory=Site.query.all)


class SiteForm(FlaskForm):
	base_url = fields.StringField()


# add routes
@app.route('/')
def index():
	site_form = SiteForm()
	visit_form = VisitForm()
	return render_template('index.html', site_form=site_form, visit_form=visit_form)


@app.route('/site', methods=('POST',))
def add_site():
	form = SiteForm()
	if form.validate_on_submit():
		site = Site()
		form.populate_obj(site)
		db.session.add(site)
		db.session.commit()
		flash("Added site")
		return redirect(url_for("index"))
	return render_template('validation_error.html', form=form)


@app.route('/visit', methods=('POST',))
def add_visit():
	form = VisitForm()
	if form.validate_on_submit():
		visit = Visit()
		form.populate_obj(visit)
		visit.site_id = form.site.data.id
		db.session.add(visit)
		db.session.commit()
		flash("Added visit for site " + form.site.data.base_url)
		return redirect(url_for('index'))
	return render_template('validation_error.html', form=form)


@app.route('/sites')
def view_sites():
	query = Site.query.filter(Site.id >= 0)
	data = query_to_list(query)
	data = [next(data)] + [[_make_link(cell) if i == 0 else cell for i, cell in enumerate(row)] for row in data]
	return render_template('data_list.html', data=data, type='Sites')


_LINK = Markup('<a href="{url}"">{name}</a>')


def _make_link(site_id):
	url = url_for("view_site_visits", site_id=site_id)
	return _LINK.format(url=url, name=site_id)


@app.route('/site/<int:site_id>')
def view_site_visits(site_id=None):
	site = Site.query.get_or_404(site_id)
	query = Visit.query.filter(Visit.site_id == site_id)
	data = query_to_list(query)
	title = "visits for " + site.base_url
	return render_template('data_list.html', data=data, type=title)


def query_to_list(query, include_field_names=True):
	""" Turns an SQLAlchemy query into a list of data values. """
	column_names = []
	for i, obj in enumerate(query.all()):
		if i == 0:
			column_names = [c.name for c in obj.__table__.columns]
			if include_field_names:
				yield column_names
		yield obj_to_list(obj, column_names)


def obj_to_list(sa_obj, field_order):
	""" Takes an SQLAlchemy object and returns a list of all its data. """
	return [getattr(sa_obj, field_name, None) for field_name in field_order]


if __name__ == "__main__":
	app.debug = True
	db.create_all()
	app.run()
		

