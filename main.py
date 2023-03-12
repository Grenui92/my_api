from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import get_db
from schemas import ContactResponse, ContactBase
from models import Contact
from datetime import date, timedelta

app = FastAPI()


@app.get('/', response_model=list[ContactResponse])
async def get_all_contacts(db: Session = Depends(get_db)):
    contacts = db.query(Contact).all()
    for contact in contacts:
        print(type(contact.birthday))
    return contacts


@app.post('/create_new_contact', response_model=ContactResponse)
async def create_new_contact(contact_body: ContactBase,
                             db: Session = Depends(get_db)):
    contact = Contact(**contact_body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


@app.get('/get_one_contact/{contact_id}', response_model=ContactResponse)
async def get_one_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return contact


@app.put('/update_contact/{contact_id}', response_model=ContactResponse)
async def update_contact(contact_body: ContactBase, id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    contact.name = contact_body.name
    contact.surname = contact_body.surname
    contact.email = contact_body.email
    contact.phone = contact_body.phone
    contact.birthday = contact_body.birthday
    contact.other = contact_body.other

    db.commit()
    db.refresh(contact)
    return contact


@app.delete('/delete_contact/{contact_id}', response_model=dict)
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db.query(Contact).filter(Contact.name == contact_id).delete()
    db.commit()
    return {'message': 'Contact was deleted'}


@app.get('/search_by_name/{name}', response_model=ContactResponse)
async def search_by_name(name: str = 'Stas', db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.name == name).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    return contact


@app.get('/search_by_surname/{surname}', response_model=ContactResponse)
async def search_by_surname(surname: str = 'Vasilenko', db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.surname == surname).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    return contact


@app.get('/search_by_email/{email}', response_model=ContactResponse)
async def search_by_email(email: str = 'grenui@gmail.com', db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.email == email).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    return contact


@app.patch('/contact_edit', response_model=ContactResponse)
async def edit_contact(field: str, new_data: str, id: int = 3, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id==id).first()
    setattr(contact, field, new_data)
    db.commit()
    db.refresh(contact)
    return contact

@app.get('/nearest_birthdays', response_model=list[ContactResponse])
async def nearest_birthdays(db: Session = Depends(get_db)):

    contacts = db.query(Contact).all()
    contacts = [contact for contact in contacts
                if abs(contact.birthday-date(contact.birthday.year, date.today().day, date.today().month))<timedelta(7)]

    return contacts