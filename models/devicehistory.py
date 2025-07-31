# from tortoise import fields, models
# from enum import Enum


# class AssignmentAction(Enum):
#     ASSIGNED = "Assigned"
#     RETURNED = "Returned"

# class DeviceHistory(models.Model):
#     id = fields.IntField(pk=True)
#     device = fields.CharField(max_length=64)
#     employee = fields.ForeignKeyField("models.Employee", related_name="assignment_logs")
#     action = fields.CharEnumField(enum_type=AssignmentAction)
#     assigned_at = fields.DatetimeField(auto_now_add=True)
#     returned_at = fields.DatetimeField(null=True)
