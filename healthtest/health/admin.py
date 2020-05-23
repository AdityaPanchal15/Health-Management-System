from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Patient
from .models import Doctor
from .models import Nurse
from .models import Administrator
from .models import Hospital
from .models import LogInInfo
from .models import Prescription
from .models import Appointment
from .models import Lab
from .models import MedicStore
from .models import Test
from .models import forstats
from .models import EmergencyContact
from .models import Message
from .models import RatingDoc
from .models import Speciality
from .models import pres

# model registers
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Nurse)
admin.site.register(Administrator)
admin.site.register(Hospital)
admin.site.register(LogInInfo)
admin.site.register(Prescription)
admin.site.register(Appointment)
admin.site.register(Lab)
admin.site.register(MedicStore)
admin.site.register(Test)
admin.site.register(forstats)
admin.site.register(EmergencyContact)
admin.site.register(Message)
admin.site.register(RatingDoc)
admin.site.register(Speciality)
admin.site.register(pres)
