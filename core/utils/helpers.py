import time
from functools import wraps
import uuid

from django.conf import settings
from django.utils import timezone


def func_debugger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        r = func(*args, **kwargs)
        time.sleep(2)
        print("Process took", "%.2f" % (time.time() - start), 'seconds')
        return r

    return wrapper


def file_upload_directory(instance, filename: str) -> str:
    model_name = instance.__class__.__name__
    _uuid = uuid.uuid4()
    instance_uuid = instance.guid
    try:
        name: str = instance.name
        name = name.split('.')[0]
    except AttributeError:
        name: str = ''
    now_time = timezone.now()
    year = now_time.year
    month = now_time.month
    day_number = now_time.day
    date_directory = '{0}/{1}/{2}'.format(year, month, day_number)
    _time = now_time.time()
    return settings.UPLOAD_DIRECTORY + '/' + model_name + '/' + str(instance_uuid) + '/' + date_directory + '/' + str(
        _time).replace(':', '_') + '_' + str(_uuid) + '_' + name + '.' + filename.split('.')[-1]
