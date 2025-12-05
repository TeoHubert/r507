from typing import Optional
from models.indicator_values import IndicatorValue
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, JSON

## Mon modèle initial
class IndicatorBase(SQLModel):
    host_id: Optional[int] = Field(default=None, foreign_key="host.id")
    name: str
    action_id: Optional[int] = Field(default=None, foreign_key="action.id")
    interval: int = Field(default=60)
    parametre: Optional[dict] = Field(default=None, sa_column=Column(JSON, nullable=True))

#Modèle utilisé pour la table "indicator" dans la base de données
class Indicator(IndicatorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    host_id: Optional[int] = Field(default=None, foreign_key="host.id")
    name: str
    action_id: Optional[int] = Field(default=None, foreign_key="action.id")
    interval: int = Field(default=60)
    parametre: Optional[dict] = Field(default=None, sa_column=Column(JSON, nullable=True))

    def __str__(self):
        return f"#{self.id} | Indicator {self.name} for host_id {self.host_id}"
    
    def __repr__(self):
        return f"<Indicator(id='{self.id}', name='{self.name}', host_id='{self.host_id}', action_id='{self.action_id}')>"

# Modèle utilisé pour les requêtes et réponses API
class IndicatorWithLastValue(IndicatorBase):
    id: Optional[int] = None
    last_value: Optional[IndicatorValue] = None