from datetime import datetime
from home.models import Information

def close_window():
    current_time = datetime.now().strftime("%H:%M:%S")
    info = Information.objects.all()
    for item in info.values('id', 'status', 'repair',):
        item_id = item['id']
        item_status = item['status']
        item_repair = item['repair'].strftime("%H:%M:%S")
        if item_status == 'Close' and item_repair == current_time:
            for start in info.filter(id=item_id, status=item_status, repair=item_repair):
                start.status = 'Open'
                start.save()
            return 'ok'


def Taskone():
    return close_window()