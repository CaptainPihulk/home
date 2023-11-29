from typing import Type, Union, Optional
from pydantic import BaseModel, ValidationError, EmailStr, validator
from errors import HttpError
import re

password_regex = re.compile("^(?=.*[a-z_])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&_])[A-Za-z\d@$!#%*?&_]{8,50}$")


class LoginUser(BaseModel):

    email_address: EmailStr
    password: str


class RegisterUser(BaseModel):

    name: str
    email_address: EmailStr
    password: str

    @validator('password')
    def validate_password(cls, value: str):
        if not re.search(password_regex, value):
            raise ValidationError('password is to easy')
        return value


class UserData(BaseModel):

    name: Optional[str]
    email_address: Optional[EmailStr]
    password: Optional[str]


class CreateAd(BaseModel):

    ad_header: str
    description: str
    owner_id: int


class AdData(BaseModel):

    ad_header: Optional[str]
    description: Optional[str]


SCHEMA_TYPE = Union[Type[RegisterUser], Type[LoginUser], Type[UserData], Type[CreateAd], Type[AdData]]


def validate(schema: SCHEMA_TYPE, json_data: dict):
    try:
        schema = schema(**json_data)
        return schema.dict(exclude_none=True)
    except ValidationError as er:
        raise HttpError(status_code=400, message=er.errors())
