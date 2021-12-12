from cb_app.models import User, Contact


def LoginQuery(form):
    return User.query.filter_by(username=form.username.data).first()


def PostQuery(form):
    return Contact(name=form.name.data, email=form.email.data, phone=form.phone.data)


def AllQuery():
    return Contact.query.all()


def RecordQuery(form):
    return Contact.query.filter_by(name=form.data.data).all()



def SearchPhoneQuery(form):
    return Contact.query.filter(Contact.phone.like('%' + form.data.data + '%')).all()


def SearchEmailQuery(form):
    return Contact.query.filter(Contact.email.like('%' + form.data.data + '%')).all()


def SearchNameQuery(form):
    return Contact.query.filter(Contact.name.like('%' + form.data.data + '%')).all()
