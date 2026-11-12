"""Data shapes shared across the project."""
from typing import Literal, Optional

from pydantic import BaseModel, Field

Status = Literal["PASS", "FAIL", "REVIEW"]
EquipmentType = Literal[
    "utility_service", "transformer", "cable_bus", "iso_phase_bus", "non_seg_bus",
    "mv_switchgear", "lv_switchgear", "ups", "server_rack",
]


class Requirement(BaseModel):
    id: str
    parameter: str
    value_number: Optional[float] = None
    value_text: Optional[str] = None
    unit: str = ""
    mandatory: bool = True
    section: str = ""
    source_quote: str = ""


class SpecRequirements(BaseModel):
    equipment_type: EquipmentType
    requirements: list[Requirement]


class CheckResult(BaseModel):
    requirement: Requirement
    required: str
    product_value: str
    status: Status
    note: str = ""


class ProductCheck(BaseModel):
    product_id: str
    product_name: str
    price_usd: Optional[float] = None
    results: list[CheckResult]

    @property
    def mandatory_fails(self) -> int:
        return sum(r.status == "FAIL" and r.requirement.mandatory for r in self.results)

    @property
    def preferred_misses(self) -> int:
        return sum(r.status == "FAIL" and not r.requirement.mandatory for r in self.results)

    @property
    def reviews(self) -> int:
        return sum(r.status == "REVIEW" for r in self.results)


class Review(BaseModel):
    equipment_type: EquipmentType
    ranked: list[ProductCheck]
    recommended_id: Optional[str] = None
    summary: str = ""
    customer_questions: list[str] = Field(default_factory=list)
    source: Literal["claude", "saved_example"] = "saved_example"
