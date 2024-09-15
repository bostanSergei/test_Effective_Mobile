from pydantic import BaseModel

from typing import Dict


class CreateSchema(BaseModel):
    id: int
    node_id: str
    name: str
    full_name: str
    owner: Dict[str, str | int | bool]
    private: bool
    html_url: str
    description: str | None
    url: str

    class Config:
        extra = 'ignore'
