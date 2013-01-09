from wtforms import Form, TextField, validators


class HelloSigner(Form):
    name = TextField('Name', [validators.Length(min=2, max=32)])
    email = TextField('Email', [validators.Length(min=6, max=128), validators.Email()])


class HelloDoc(Form):
    name = TextField('Name', [validators.Length(min=1, max=25)])


class HelloTeam(Form):
    name = TextField('Name', [validators.Length(min=1, max=25)])