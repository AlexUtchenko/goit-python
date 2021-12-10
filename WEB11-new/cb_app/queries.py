from cb_app.models import User, Contact
from cb_app.forms import LoginForm, RegistrationForm, RequestForm, EditForm

LoginQuery = User.query.filter_by(username=LoginForm().username.data).first()
RecordQuery = Contact.query.filter_by(name=RequestForm().data.data).all()
SearchPhoneQuery = Contact.query.filter(Contact.phone.like('%' + RequestForm().data.data + '%')).all()
SearchEmailQuery =Contact.query.filter(Contact.email.like('%' + RequestForm().data.data + '%')).all()
SearchNameQuery = Contact.query.filter(Contact.name.like('%' + RequestForm().data.data + '%')).all()
