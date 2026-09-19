from datetime import datetime
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String,JSON,DateTime,Float
from .database import Base
class EvaluationRun(Base):
    __tablename__="evaluation_runs"
    id:Mapped[str]=mapped_column(String(80),primary_key=True)
    dataset:Mapped[str]=mapped_column(String(160))
    status:Mapped[str]=mapped_column(String(40))
    score:Mapped[float]=mapped_column(Float,default=0)
    report:Mapped[dict]=mapped_column(JSON,default=dict)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
