from typing import Optional
from sqlmodel import Field, SQLModel
import datetime

class IndicatorValue(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    indicator_id: Optional[int] = Field(default=None, foreign_key="indicator.id")
    value: str
    date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    def __str__(self):
        return f"#{self.id} | IndicatorValue for indicator_id {self.indicator_id}"
    
    def __repr__(self):
        return f"<IndicatorValue(id='{self.id}', indicator_id='{self.indicator_id}', value='{self.value}')>"