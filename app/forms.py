from flask.ext.wtf import Form
from wtforms import SelectField, SubmitField
from wtforms.validators import Required

list_of_topics = (
	('Comedy', 'Comedy'),
    ('Education', 'Education'),
    ('Entertainment', 'Entertainment'),
    ('Environment', 'Environment'),
    ('Fashion', 'Fashion'),
    ('Health', 'Health'),
    ('Politics', 'Politics'),
    ('Religion', 'Religion'),
    ('Science', 'Science'),
    ('Sports', 'Sports'),
    ('Technology', 'Technology'),
    ('Transportation', 'Transportation'),
)

class topicsForm(Form):
    topics = SelectField('category', choices=list_of_topics, validators=[Required()])
    submit = submit = SubmitField("Send")