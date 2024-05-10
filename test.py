from pydantic import BaseModel, Field
from typing import Dict

class InnerModel(BaseModel):
    inner_field1: str
    inner_field2: int

class OuterModel(BaseModel):
    outer_field1: str
    outer_field2: int
    nested_dict: Dict[str, InnerModel]

# Tạo một instance của OuterModel
outer_instance = OuterModel(
    outer_field1="outer_value1",
    outer_field2=456,
    nested_dict={"nested_key": {"inner_field1": "value1", "inner_field2": 123}}
)

# In ra giá trị của outer_instance
print(outer_instance.dict())
