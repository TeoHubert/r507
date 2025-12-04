from sqlmodel import Session, select, Field, SQLModel
from typing import Optional
from pydantic import BaseModel
import asyncio

class Scheduler(BaseModel):
    thread: Optional[asyncio.Task] = None

    def start(self, coro):
        if self.thread is None:
            self.thread = asyncio.create_task(coro)

    async def scheduler():
        while True:
            with Session(engine) as session:
                indicators = session.exec(select(Indicator)).all()
                result = []
                for indicator in indicators:
                    last = session.exec(
                        select(IndicatorValue)
                        .where(IndicatorValue.indicator_id == indicator.id)
                        .order_by(IndicatorValue.date.desc())
                        .limit(1)
                    ).first()
                    result.append({"indicator": indicator, "last_value": last.date if last else None})
                print(result)
            await asyncio.sleep(60)  # Check every minute