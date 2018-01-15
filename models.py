from wtforms import StringField,IntegerField,Form,validators,SubmitField,PasswordField
import sqlite3



class Studentdetails(Form):
    fname = StringField('First Name', [validators.required()])
    lname = StringField('Last Name', [validators.required()])
    stid = IntegerField('Student id', [validators.required()])
    submit = SubmitField('send')


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=20)])
    password = PasswordField('Password', [
        validators.required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

# con = sqlite3.connect('studentrec.db')
# con.row_factory=sqlite3.Row
# cur = con.cursor()
# row=cur.execute('select * from users where username = ?',('mujoshi',))
#
# data = row.fetchone()[2]
#
# if data is not None:
#     password = data[2]
    # print(data)