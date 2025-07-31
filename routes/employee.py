from sanic import Blueprint, response
from sanic.response import json,text
from models.employee import Employee

employee_bp = Blueprint('employee', url_prefix='/employees')

#view-all employee
@employee_bp.route("/all-employees",methods=["GET"])
async def all_employees(request):

    employees = await Employee.all()  
    employee_lst = []

    for emp in employees:
        employee_lst.append({
            "id":emp.employee_id,
            "name":emp.name,
            "gmail":emp.email,
            "department":emp.department,
        })
    
    return response.json({"Employees List": employee_lst})

#all-employee-with-devices
@employee_bp.route("/all-employees-devices", methods=["GET"])
async def all_employees_devices(request):
    employees = await Employee.all().prefetch_related("devices") 

    employee_lst = []
    for emp in employees:
        device_list = [
            {
                "device_id": device.device_id,
                "type": device.model,
            }
            for device in emp.devices 
        ]

        employee_lst.append({
            "id": emp.employee_id,
            "name": emp.name,
            "devices": device_list,
        })

    return response.json({"Employees List": employee_lst})


#view-profile
@employee_bp.route("/profile/<employee_id>",methods=["GET"])
async def employee_profile(request,employee_id):

    employees = await Employee.filter(employee_id=employee_id)

    if not employees:
        return response.json({"error": "Employee not found"}, status=404)
    profile_detail = []

    for emp in employees:
           profile_detail.append({
            "id":emp.employee_id,
            "name":emp.name,
            "gmail":emp.email,
            "department":emp.department,
        })
    
    return response.json({"Employee Detail": profile_detail})

#update-profile
@employee_bp.route("/update-profile/<employee_id>", methods=["PUT", "PATCH"])
async def update_profile(request, employee_id):
    emp = await Employee.get_or_none(employee_id=employee_id)
    if not emp:
        return response.json({"error": "Employee not found"}, status=404)

    data = request.json or {}
    print("Received update data:", data) 

    editable_fields = ["name", "email", "department"]
    updated_fields = {}
    for field in editable_fields:
        if field in data:
            setattr(emp, field, data[field])
            updated_fields[field] = data[field]

    if not updated_fields:
        return response.json({"error": "No fields to Update"}, status=400)

    await emp.save()

    return response.json({
        "message": "Profile updated successfully",
        "updated_fields": updated_fields
    })
