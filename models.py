from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Expense:
    amount: float
    category: str
    id: Optional[int] = None
    description: Optional[str] = None
    date: Optional[str] = None
