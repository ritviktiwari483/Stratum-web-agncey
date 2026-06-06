from pydantic import BaseModel, EmailStr, field_validator


class ContactCreate(BaseModel):
    name: str
    phone: str
    email: str
    message: str

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Name is required")
        return v.strip()

    @field_validator("email")
    @classmethod
    def email_valid(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email")
        return v.strip()

    @field_validator("message")
    @classmethod
    def message_not_empty(cls, v):
        if len(v.strip()) < 10:
            raise ValueError("Message must be at least 10 characters")
        return v.strip()


class ContactResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    message: str
    created_at: str

    model_config = {"from_attributes": True}
