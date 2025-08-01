from sanic import Blueprint,response
from models.device import Device
from models.devicehistory import DeviceHistory
device_bp = Blueprint('device', url_prefix='/devices')

#All-Device
@device_bp.route("/all-devices",methods=["GET"])
async def all_devices(request):
    # print(request.query_params())

    devices = await Device.all()
    device_lst = []
    for device in devices:
        device_lst.append({
        "device_id":device.device_id,
        "device_type": device.device_type,
        "brand": device.brand,
        "model": device.model,
        "serial_number": device.serial_number,
        "status": device.status.value, 
        "assigned_to_id": device.assigned_to_id if hasattr(device, 'assigned_to_id') else None,
})

    return response.json({"Devices":device_lst})

# Pagination - Per Page / Page No.
#Device-Detail
@device_bp.route("/device-detail/<device_id>",methods=["GET"])
async def device_detail(request,device_id):

    devices= await Device.filter(device_id=device_id)

    if not devices:
        return response.json({"error": "Device not found"}, status=404)
    device_detail = []

    for device in devices:
           device_detail.append({
        "device_id":device.device_id,
        "device_type": device.device_type,
        "brand": device.brand,
        "model": device.model,
        "serial_number": device.serial_number,
        "status": device.status.value, 
        "assigned_to_id": device.assigned_to_id if hasattr(device, 'assigned_to_id') else None,
        })
    
    return response.json({"Device Detail": device_detail})
    
@device_bp.route("/device-history/<device_id:str>", methods=["GET"])
async def get_device_history(request, device_id):
    device = await Device.get_or_none(device_id=device_id)
    if not device:
        return response.json({"error": "Device not found"}, status=404)

    history = await DeviceHistory.filter(device=device).order_by("-timestamp").all()

    history_list = [
        {
            "action": h.action.value,
            "timestamp": h.timestamp.isoformat(),
            "notes": h.notes,
        }
        for h in history
    ]

    return response.json({
        "device_id": device.device_id,
        "history": history_list
    })