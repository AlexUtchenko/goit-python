from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///sqlalchemy_example.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()

class ContactBook(Base):
    __tablename__ = 'contact_book'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    phone_number = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)

    def __init__(self, name, phone_number, email):
        self.name = name
        self.phone_number = phone_number
        self.email = email

    def __repr__(self):
        return f'{self.name}'

if __name__ == '__main__':
    session = Session()
    print(f'{" "*20}*** Welcome to Personal assistant Contact book DB edition!***')
    print("Commands:\n - add;\n - show;\n - show all;\n - delete;\n - find;\n - update;\n - exit\n")
    commands = ['add', 'show', 'delete', 'show all', 'find', 'exit', 'update']
    while True:
        answer = str(input('Enter command:\n>>> ')).lower().strip()
        if answer == 'add':
            name = input('Enter name: ')
            phone = input('Enter phone: ')
            email = input('Enter email: ')
            new_record = ContactBook(name, phone, email)
            session.add(new_record)
            session.commit()
            print('New record successfully added')
            continue
        elif answer == 'show all':
            for raw in session.query(ContactBook).all():
                print(f'id = {raw.id}, name = {raw.name}, phone = {raw.phone_number}, email = {raw.email}')
                continue
        elif answer == 'delete':
            name = input('Enter name: ')
            session.query(ContactBook).filter(ContactBook.name == name).delete()
            session.commit()
            print(f'Record with name "{name}" has been successfully deleted')
            continue
        elif answer == 'show':
            name = input('Enter name: ')
            result = session.query(ContactBook).filter(ContactBook.name == name).first()
            print(f'id = {result.id}, name = {result.name}, phone = {result.phone_number}, email = {result.email}')
            continue
        elif answer == 'update':
            name = input('Enter name: ')
            result = session.query(ContactBook).filter(ContactBook.name == name).first()
            phone = input('Enter phone: ')
            email = input('Enter email: ')
            result.email = email
            result.phone_number = phone
            session.commit()
            print(f'Record "{name}" was successfully updated')
            continue
        elif answer == 'find':
            text = input('Enter data: ')
            search = f'%{text}%'
            result = session.query(ContactBook).filter(ContactBook.phone_number.like(search)).all()
            result2 = session.query(ContactBook).filter(ContactBook.email.like(search)).all()
            for raw in  result:
                print(f'id = {raw.id}, name = {raw.name}, phone = {raw.phone_number}, email = {raw.email}')
            for raw in  result2:
                print(f'id = {raw.id}, name = {raw.name}, phone = {raw.phone_number}, email = {raw.email}')
            continue
        elif answer == 'exit':
            break
        else:
            print("Command input error. Try correct command again")
            continue
    session.close()
    print("Good bye!")







