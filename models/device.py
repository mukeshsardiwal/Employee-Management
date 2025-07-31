from tortoise import fields, models
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.employee import Employee

class DeviceStatus(Enum):
    AVAILABLE = "Available"
    ASSIGNED = "Assigned"
    UNDER_REPAIR = "Under Repair"
    RETIRED = "Retired"

class Device(models.Model):
    id = fields.IntField(pk=True)
    device_id = fields.CharField(max_length=16, unique=True, null=True) 
    device_type = fields.CharField(max_length=64)
    brand = fields.CharField(max_length=64)
    model = fields.CharField(max_length=128)
    serial_number = fields.CharField(max_length=128, unique=True)
    status = fields.CharEnumField(enum_type=DeviceStatus)
    created_at = fields.DatetimeField(auto_now_add=True,null=True)
    assigned_to: "fields.ForeignKeyRelation[Employee]" = fields.ForeignKeyField(
        "models.Employee",
        related_name="devices",
        null=True,
        on_delete=fields.CASCADE,
    )
