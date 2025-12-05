from typing import Optional
from sqlmodel import Field, SQLModel
import datetime

class IndicatorValue(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    indicator_id: Optional[int] = Field(default=None, foreign_key="indicator.id")
    value: float = Field(default=0)
    unite: Optional[str] = Field(default="%")
    error_message: Optional[str] = Field(default=None)
    date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    def __str__(self):
        return f"#{self.id} | IndicatorValue for indicator_id {self.indicator_id}"
    
    def __repr__(self):
        return f"<IndicatorValue(id='{self.id}', indicator_id='{self.indicator_id}', value='{self.value}')>"
    
class ListeIndicatorValue(SQLModel):
    values: list[IndicatorValue]
    action_min_value: Optional[float] = None
    action_max_value: Optional[float] = None
    action_unite: Optional[str] = None
    action_labels: Optional[dict] = None
    