from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Contact
from app.schemas import ContactCreate, ContactResponse
from app.services.email import send_notification

router = APIRouter(prefix="/api", tags=["contacts"])


@router.post("/contact")
async def submit_contact(data: ContactCreate, db: AsyncSession = Depends(get_db)):
    contact = Contact(
        name=data.name,
        phone=data.phone,
        email=data.email,
        message=data.message,
    )
    db.add(contact)
    await db.commit()
    await db.refresh(contact)

    await send_notification(data.name, data.phone, data.email, data.message)

    return {
        "status": "success",
        "message": "Thank you! We'll get back to you soon.",
    }


@router.get("/contacts", response_model=list[ContactResponse])
async def list_contacts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Contact).order_by(Contact.created_at.desc()))
    rows = result.scalars().all()
    return [
        ContactResponse(
            id=r.id,
            name=r.name,
            phone=r.phone,
            email=r.email,
            message=r.message,
            created_at=r.created_at.isoformat() if r.created_at else "",
        )
        for r in rows
    ]
