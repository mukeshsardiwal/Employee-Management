from tortoise import fields,models
from models.device import Device

class Employee(models.Model):
    employee_id = fields.CharField(max_length=32, pk=True)
    name = fields.CharField(max_length=128)
    email = fields.CharField(max_length=256, unique=True)
    department = fields.CharField(max_length=64)
    created_at = fields.DatetimeField(auto_now_add=True,null=True)

    devices: fields.ReverseRelation[Device]

    def __str__(self):
        return f"Employee({self.employee_id}, {self.name})"