from .user import User
from .doctor import Doctor
from .clinic import Clinic
from .specialty import Specialty
from .wilaya import Wilaya, Commune
from .service import Service, DoctorService
from .working_hour import WorkingHour
from .holiday import Holiday
from .report import Report
from .platform_setting import PlatformSetting

__all__ = [
    'User',
    'Doctor',
    'Clinic',
    'Specialty',
    'Wilaya',
    'Commune',
    'Service',
    'DoctorService',
    'WorkingHour',
    'Holiday',
    'Report',
    'PlatformSetting'
]