from fastapi import APIRouter, Depends, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import secrets, os
from app.database import get_db
from app.models import Contact
from app.config import settings

router = APIRouter(prefix="/admin", tags=["admin"])
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "templates"))

ADMIN_TOKEN = secrets.token_hex(16)

def verify_admin(request: Request):
    token = request.cookies.get("admin_token")
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=303, detail="Unauthorized")


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(request: Request, password: str = Form(...)):
    if password != settings.admin_password:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Wrong password"})
    response = RedirectResponse(url="/admin", status_code=303)
    response.set_cookie(key="admin_token", value=ADMIN_TOKEN, httponly=True, max_age=86400)
    return response


@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/admin/login", status_code=303)
    response.delete_cookie("admin_token")
    return response


@router.get("", response_class=HTMLResponse)
async def admin_dashboard(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        verify_admin(request)
    except HTTPException:
        return RedirectResponse(url="/admin/login", status_code=303)

    result = await db.execute(select(Contact).order_by(Contact.created_at.desc()))
    contacts = result.scalars().all()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "contacts": contacts,
        "count": len(contacts),
    })


@router.get("/export")
async def export_csv(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        verify_admin(request)
    except HTTPException:
        return RedirectResponse(url="/admin/login", status_code=303)

    result = await db.execute(select(Contact).order_by(Contact.created_at.desc()))
    contacts = result.scalars().all()

    csv = "Name,Phone,Email,Message,Date\n"
    for c in contacts:
        date = c.created_at.strftime("%Y-%m-%d %H:%M") if c.created_at else ""
        csv += f'"{c.name}","{c.phone}","{c.email}","{c.message}","{date}"\n'

    return Response(content=csv, media_type="text/csv",
                    headers={"Content-Disposition": "attachment; filename=stratumweb-leads.csv"})
