from tortoise import fields, models
from enum import Enum

class DeviceAction(Enum):
    ASSIGNED = "Assigned"
    RETURNED = "Returned"
    REPAIRED = "Repaired"
    RETIRED = "Retired"

class DeviceHistory(models.Model):
    id = fields.IntField(pk=True)
    device = fields.ForeignKeyField("models.Device", related_name="history", on_delete=fields.CASCADE)
    action = fields.CharEnumField(DeviceAction)
    timestamp = fields.DatetimeField(auto_now_add=True)
    notes = fields.TextField(null=True)
