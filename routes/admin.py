from models.admin import Admin 
from models.employee import Employee
from models.device import DeviceStatus
from models.device import Device
from sanic import Blueprint, response,json
from utils.auth import hash_password
from datetime import datetime
from models.devicehistory import DeviceHistory,DeviceAction


admin_bp = Blueprint("admin", url_prefix="/admin")

#All-Admins
@admin_bp.route("/all-admins", methods=["GET"])
async def get_all_admins(request):
    admins = await Admin.all()
    admin_list = []
    for admin in admins:
        admin_list.append({
            "id": admin.admin_id,
            "username": admin.username,
            "name": admin.name
        })
    return response.json({"admins": admin_list})

#Add-Employee
@admin_bp.route("/add-employee", methods=["POST"])
async def add_employee(request):
    data = request.json or {}

    required_fields = ["employee_id", "name", "email", "department"]
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        return response.json({"error": f"Missing required fields: {', '.join(missing)}"}, status=400)

    try:
        employee = await Employee.create(
            employee_id=data["employee_id"],
            name=data["name"],
            email=data["email"],
            department=data["department"],
            created_at=datetime.utcnow()
        )
    except Exception as e:
        
        return response.json({"error": str(e)}, status=500)

    return response.json({
        "message": "Employee added successfully",
        "employee": {
            "employee_id": employee.employee_id,
            "name": employee.name,
            "email": employee.email,
            "department": employee.department,
            "created_at": employee.created_at.isoformat() 
        }
    }, status=201)

#Delete-Employee 
@admin_bp.route("/delete-employee/<employee_id>", methods=["DELETE"])
async def delete_user(request, employee_id):
    Emp = await Employee.get_or_none(employee_id=employee_id)
    if not Emp:
        return response.json({"error": "User not found"}, status=404)
    
    await Emp.delete()
    
    return response.json({"message": f"Employee with employee_id - {employee_id} & username - {Emp.name} deleted successfully"})

#Add-Device  
@admin_bp.route("/add-device", methods=["POST"])
async def add_device(request):
    data = request.json or {}

    required_fields = [
        "device_id",
        "device_type",
        "brand",
        "model",
        "serial_number",
        "status",
    ]

    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        return response.json(
            {"error": f"Missing required fields: {', '.join(missing)}"},
            status=400
        )

    try:
        device = await Device.create(

            device_id=data["device_id"],
            device_type=data["device_type"],
            brand=data["brand"],
            model=data["model"],
            serial_number=data["serial_number"],
            status=data["status"],
            assigned_to=data.get("assigned_to"),
            created_at=datetime.utcnow()
            )
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

    return response.json({
        "message": "Device added successfully",
        "device_id":device.device_id,
        "device_type": device.device_type,
        "model": device.model,
        "brand": device.brand,
        "serial_number": device.serial_number,
        "status": device.status.value,
        "assigned_to": device.assigned_to,
        "created_at": device.created_at.isoformat()  # <-- FIX here
    }, status=201)

#Delete-Device 
@admin_bp.route("/delete-device/<device_id>", methods=["DELETE"])
async def delete_device(request, device_id):
    dev = await Device.get_or_none(device_id=device_id)
    if not dev:
        return response.json({"error": "Device not found"}, status=404)
    
    await dev.delete()
    
    return response.json({"message": f"Device with device_id - {device_id} & serial_number - {dev.serial_number} deleted successfully"})

#Assign-Device 
@admin_bp.route("/assign-device/<device_id>/<employee_id>", methods=["POST"])
async def assign_device(request, device_id, employee_id):
    device = await Device.get_or_none(device_id=device_id)
    if not device:
        return response.json({"error": "Device not found"}, status=404)
    
    if device.status in [DeviceStatus.ASSIGNED, DeviceStatus.RETIRED, DeviceStatus.UNDER_REPAIR]:
        return response.json({"error": "Cannot assign device with current status"}, status=400)
    
    emp = await Employee.get_or_none(employee_id=employee_id)
    if not emp:
        return response.json({"error": "Employee not found"}, status=404)
    
    if device.status == DeviceStatus.AVAILABLE:
        device.assigned_to_id = employee_id
        device.status = DeviceStatus.ASSIGNED
        device.assigned_at = datetime.utcnow()
        await device.save()

        # ✅ Log history after successful assignment
        await DeviceHistory.create(
            device_id=device.id,  # ⚠️ Use device.id, not device object!
            action=DeviceAction.ASSIGNED,
            notes=f"Assigned to employee_id: {emp.employee_id}"
        )

        return response.json({
            "message": f"Device {device.device_id} successfully assigned to employee {emp.name}",
            "device": {
                "device_id": device.device_id,
                "status": device.status.value,
                "assigned_to": emp.name
            }
        }, status=200)
    
    return response.json(
        {
            "error": f"Cannot assign device. Device status is '{device.status.value}'. Only 'Available' devices can be assigned.",
            "device_status": device.status.value
        },
        status=400
    )

#device-current-status
@admin_bp.route("/device-status/<device_id>",methods=["GET"])
async def device_status(request,device_id):

    device = await Device.get_or_none(device_id=device_id)
    if not device:
        return response.json({"error": "Device not found"}, status=404)

    return response.json({"device-status": device.status.value}, status=200)

#update-device-status
@admin_bp.route("/update-device-status/<device_id>", methods=["POST"])
async def update_device_status(request, device_id):
    data = request.json or {}
    required_fields = ["status"]
    
    device = await Device.get_or_none(device_id=device_id)
    if not device:
        return response.json({"error": "Device not found"}, status=404)
    
    if device.status == 'Assigned' or 'Retired':
        return response.json({"error": "Device Assigned Or Retired"},status=404)
    
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        return response.json(
            {"error": f"Missing required fields: {', '.join(missing)}"},
            status=400
        )
    device.status = data["status"]
    await device.save()
    
    return response.json({"device-status": device.status}, status=200)

#deallocate-Device
@admin_bp.route("/deallocate-device", methods=["POST"])
@admin_bp.route("/deallocate-device", methods=["POST"])
async def deallocate_device(request):
    data = request.json or {}
    device_id = data.get("device_id")
    if not device_id:
        return json({"error": "Missing device_id"}, status=400)
    
    # Look up Device by your custom device_id
    device = await Device.get_or_none(device_id=device_id)
    if not device:
        return json({"error": "Device not found"}, status=404)
    if not device.assigned_to_id:
        return json({"error": "Device is already unassigned"}, status=400)
    
    employee = await device.assigned_to
    
    # ✅✅✅ Use device.id (the numeric primary key), not device.device_id (your string)
    await DeviceHistory.create(
        device_id=device.id,  # <--- This is the FIX
        action=DeviceAction.RETURNED,
        notes=f"Deallocated from employee ID: {employee.employee_id}"
    )
    
    device.assigned_to = None
    device.status = "Available"
    device.deallocated_at = datetime.utcnow()
    await device.save()
    
    return json({
        "message": f"Device {device.device_id} deallocated from employee {employee.name} ({employee.employee_id})."
    }, status=200)


#switch
@admin_bp.route("/switch-device/<device_id>/<new_employee_id>", methods=["POST"])
async def switch_devices(request, device_id, new_employee_id):
    device = await Device.get_or_none(device_id=device_id)

    if not device:
        return response.json({"error": "Device not found"}, status=404)

    new_employee = await Employee.get_or_none(employee_id=new_employee_id)

    if not new_employee:
        return response.json({"error": "New employee not found"}, status=404)

    if device.assigned_to_id == new_employee.employee_id:
        return response.json(
            {"message": "Device already assigned to the given employee"},
            status=400
        )

    old_employee_id = device.assigned_to_id

    device.assigned_to = new_employee
    device.status = "Assigned"
    await device.save()

    return response.json({
        "message": f"Device {device.device_id} reassigned from employee {old_employee_id or 'N/A'} to {new_employee.employee_id}."
    }, status=200)

#add-admin
@admin_bp.route("/add-admin", methods=["POST"])
async def add_admin(request):
    data = request.json or {}

    required_fields = ["admin_id","name", "username", "email", "password"]
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        return response.json({"error": f"Missing required fields: {', '.join(missing)}"}, status=400)

    hashed_password = hash_password(data["password"])

    try:
        admin = await Admin.create(
            admin_id=data["admin_id"],
            name=data["name"],
            email=data["email"],
            username=data["username"],
            password=hashed_password,
            created_at=datetime.utcnow()
        )
    except Exception as e:
        
        return response.json({"error": str(e)}, status=500)

    return response.json({
        "message": "Admin added successfully",
        "employee": {
            "employee_id": admin.admin_id,
            "name": admin.name,
            "email": admin.email,
            "username": admin.username,
            "created_at": admin.created_at.isoformat() 
        }
    }, status=201)