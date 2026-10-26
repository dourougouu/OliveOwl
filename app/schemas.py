from pydantic import BaseModel, Field, ConfigDict

class ProducerCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    first_name: str = Field(min_length=1, max_length=150)
    last_name: str = Field(min_length=1, max_length=150)
    fathers_name: str | None = Field(default=None, max_length=150)

    phone_number: str = Field(min_length=1, max_length=10)
    home_number: str | None = Field(default=None, max_length=10)
    address: str | None = Field(default=None, max_length=255)

    afm: str = Field(pattern=r"^[0-9]{9}$")
    adt: str | None = Field(default=None, max_length=20)

    tk: str = Field(min_length=1, max_length=5)
    dhmos: str = Field(min_length=1, max_length=255)
    doy: str = Field(min_length=1, max_length=255)

    notes: str | None = None