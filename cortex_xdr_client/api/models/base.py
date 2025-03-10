from pydantic import BaseModel, Extra


class CustomBaseModel(BaseModel):
    class Config:
        extra = Extra.allow
        use_enum_values = True
