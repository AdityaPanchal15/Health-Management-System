# Create your models here.
from django.db import models
from datetime import date
import uuid


# from djangoratings.fields import RatingField


# This module contains the Hospital model.
# class Location_common(models.Model):
#     state=models.CharField(max_length=50,null=False,default='')
#     city=models.CharField(max_length=50,default='')
#     zipcode=models.IntegerField(max_length=10,null=True)

class Hospital(models.Model):
    name = models.CharField(max_length=50, default='')
    address = models.CharField(max_length=200, default='')
    hosp_city = models.CharField(max_length=50, null=False)
    hosp_state = models.CharField(max_length=50, null=False)
    hosp_zip = models.CharField(max_length=50, null=False)
    hos_id = models.AutoField(primary_key=True, unique=True)

    def __str__(self):
        return self.name


# This module contains the Emergency Contact model.
class EmergencyContact(models.Model):
    firstName = models.CharField(max_length=50, default='')
    lastName = models.CharField(max_length=50, default='')
    number = models.CharField(max_length=13, default='')
    address = models.CharField(max_length=100, default='')
    em_city = models.CharField(max_length=50, null=False)
    em_state = models.CharField(max_length=50, null=False)
    em_zip = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.firstName + " " + self.lastName


class Patient(models.Model):
    firstName = models.CharField(max_length=50, default='')
    lastName = models.CharField(max_length=50, default='')
    number = models.CharField(max_length=13, default='')
    paddress = models.CharField(max_length=100, default='')
    email = models.CharField(max_length=100, default='')
    provider = models.CharField(max_length=100, default='')
    insuranceid = models.CharField(max_length=12, default='')
    contact = models.ForeignKey(EmergencyContact, null=True, on_delete=models.CASCADE)
    height = models.CharField(max_length=7, default='')
    weight = models.CharField(max_length=6, default='')
    allergies = models.TextField(max_length=500, default='')
    gender = models.CharField(max_length=23, default='')
    username = models.CharField(max_length=30, default='')
    hospital = models.ForeignKey(Hospital, default=None, blank=True, null=True, on_delete=models.CASCADE)
    # patient_area = models.ForeignKey(Location_common, null=False, on_delete=models.CASCADE)
    medications = models.CharField(max_length=256, default="")
    pid = models.CharField(max_length=12, default="")
    p_city = models.CharField(max_length=50, null=False)
    p_state = models.CharField(max_length=50, null=False)
    p_zip = models.CharField(max_length=50, null=False)
    sactive = models.CharField(max_length=2, default='1')

    def __str__(self):
        return self.firstName + " " + self.lastName

    def getEmergencyContact(self, patient):
        return patient.contact

    def getHospital(self, patient):
        return patient.hospital


# This module contains the Doctor model.
class Doctor(models.Model):
    firstName = models.CharField(max_length=50, default='')
    lastName = models.CharField(max_length=50, default='')
    username = models.CharField(max_length=30, default='')
    workplace = models.ForeignKey(Hospital, null=True, on_delete=models.CASCADE)
    doctor_exp = models.CharField(default="", max_length=2)
    number = models.CharField(max_length=13, default='')
    paddress = models.CharField(max_length=100, default='')
    email = models.CharField(max_length=100, default='')
    provider = models.CharField(max_length=100, default='')
    insuranceid = models.CharField(max_length=12, default='')
    contact = models.ForeignKey(EmergencyContact, null=True, on_delete=models.CASCADE)
    height = models.CharField(max_length=7, default='')
    weight = models.CharField(max_length=6, default='')
    allergies = models.TextField(max_length=500, default='')
    gender = models.CharField(max_length=23, default='')
    medications = models.CharField(max_length=256, default="")
    pid = models.CharField(max_length=12, default="")
    p_city = models.CharField(max_length=50, null=False)
    p_state = models.CharField(max_length=50, null=False)
    p_zip = models.CharField(max_length=50, null=False)
    licid = models.CharField(max_length=50, null=False)
    sactive = models.CharField(max_length=2, default='1')

    # doc_spec = models.CharField(max_length=50, null=False)

    def getEmergencyContact(self, doctor):
        return doctor.contact

    def __str__(self):
        return self.firstName + " " + self.lastName

    def getWorkplace(self, doctor):
        return doctor.workplace


class Speciality(models.Model):
    hospital = models.CharField(max_length=50, null=False)
    city = models.CharField(max_length=50, null=False)
    doctor = models.ForeignKey(Doctor, default=None, blank=True, null=True, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.speciality

    # def getHospital(self, spec):
    #     return spec.hospital

    def getDoctor(self, spec):
        return spec.doctor


class RatingDoc(models.Model):
    rating = models.CharField(max_length=1)
    doc = models.CharField(max_length=50)
    review = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    by_patient = models.CharField(max_length=50)


# This module contains the Nurse model.
class Nurse(models.Model):
    firstName = models.CharField(max_length=50, default='')
    lastName = models.CharField(max_length=50, default='')
    username = models.CharField(max_length=30, default='')
    workplace = models.ForeignKey(Hospital, null=True, on_delete=models.CASCADE)
    number = models.CharField(max_length=13, default='')
    paddress = models.CharField(max_length=100, default='')
    email = models.CharField(max_length=100, default='')
    provider = models.CharField(max_length=100, default='')
    insuranceid = models.CharField(max_length=12, default='')
    contact = models.ForeignKey(EmergencyContact, null=True, on_delete=models.CASCADE)
    height = models.CharField(max_length=7, default='')
    weight = models.CharField(max_length=6, default='')
    allergies = models.TextField(max_length=500, default='')
    gender = models.CharField(max_length=23, default='')
    medications = models.CharField(max_length=256, default="")
    pid = models.CharField(max_length=12, default="")
    p_city = models.CharField(max_length=50, null=False)
    p_state = models.CharField(max_length=50, null=False)
    p_zip = models.CharField(max_length=50, null=False)
    sactive = models.CharField(max_length=2, default='1')

    def getEmergencyContact(self, nurse):
        return nurse.contact

    def __str__(self):
        return self.firstName + " " + self.lastName

    def getWorkplace(self, nurse):
        return nurse.workplace


# This module contains the Administrator model.
class Administrator(models.Model):
    firstName = models.CharField(max_length=50, default='')
    lastName = models.CharField(max_length=50, default='')
    username = models.CharField(max_length=30, default='')
    workplace = models.ForeignKey(Hospital, null=True, on_delete=models.CASCADE)
    number = models.CharField(max_length=13, default='')
    paddress = models.CharField(max_length=100, default='')
    email = models.CharField(max_length=100, default='')
    provider = models.CharField(max_length=100, default='')
    insuranceid = models.CharField(max_length=12, default='')
    contact = models.ForeignKey(EmergencyContact, null=True, on_delete=models.CASCADE)
    height = models.CharField(max_length=7, default='')
    weight = models.CharField(max_length=6, default='')
    allergies = models.TextField(max_length=500, default='')
    gender = models.CharField(max_length=23, default='')
    medications = models.CharField(max_length=256, default="")
    pid = models.CharField(max_length=12, default="")
    p_city = models.CharField(max_length=50, null=False)
    p_state = models.CharField(max_length=50, null=False)
    p_zip = models.CharField(max_length=50, null=False)
    sactive = models.CharField(max_length=2, default='1')

    def getEmergencyContact(self, administrator):
        return administrator.contact

    def __str__(self):
        return self.firstName + " " + self.lastName

    def getWorkplace(self, admin):
        return admin.workplace


class Lab(models.Model):
    username = models.CharField(max_length=50, default='')
    firstName = models.CharField(max_length=50, default='')
    lastName = models.CharField(max_length=50, default='')
    lab_name = models.CharField(max_length=50, default='')
    city = models.CharField(max_length=50, default='')
    zipcode = models.CharField(max_length=10, default='')
    state = models.CharField(max_length=10, default='')

    def __str__(self):
        return self.firstName + " " + self.lastName


# This module contains the Patient model.
class MedicStore(models.Model):
    username = models.CharField(max_length=50, default='')
    firstName = models.CharField(max_length=50, default='')
    lastName = models.CharField(max_length=50, default='')
    medic_name = models.CharField(max_length=50, default='')
    city = models.CharField(max_length=50, default='')
    zipcode = models.CharField(max_length=10, default='')
    state = models.CharField(max_length=10, default='')

    def __str__(self):
        return self.firstName + " " + self.lastName


# This module contains the Test model.
class Test(models.Model):
    lab_name = models.ForeignKey(Lab, max_length=50, default='', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default='')
    description = models.CharField(max_length=500)
    released = models.BooleanField(default=False)
    testResults = models.FileField(upload_to='tests', null=True, blank=True)
    patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def getPatient(self, test):
        return test.patient

    def getDoctor(self, test):
        return test.doctor

    def getLab(self, test):
        return test.Lab


#
# class Alert(models.Model):
#     msg = models.CharField(max_length=200)
#     city = models.CharField(max_length=20)

class forstats(models.Model):
    for_patient = models.CharField(max_length=50)
    current_city = models.CharField(max_length=50)
    disease = models.CharField(max_length=50)
    critic_level = models.CharField(max_length=50)
    month = models.CharField(max_length=50)
    year = models.CharField(max_length=50)
    death = models.CharField(max_length=2, default='0')

    def __str__(self):
        return self.for_patient


# This module contains the Appointment model.
class Appointment(models.Model):
    month = models.CharField(max_length=2, default='')  # '12'
    day = models.CharField(max_length=2, default='')  # '01'
    year = models.CharField(max_length=4, default='')  # '2016'
    appttime = models.CharField(max_length=5, default='')  # '05:30'
    phase = models.CharField(max_length=2, default='')  # 'AM' or 'PM'
    patient = models.CharField(max_length=12, default='')
    # patient = models.ForeignKey(Patient, null=True,on_delete=models.CASCADE)
    # current_city=models.CharField(null=True,max_length=20)
    location = models.ForeignKey(Hospital, null=True, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.CASCADE)
    done = models.CharField(max_length=1, default='0')
    admit = models.CharField(max_length=1, default='0')
    rate = models.CharField(max_length=1, default='0')

    # diseases = models.CharField(null=False,max_length=50)
    # critic_level=models.CharField(max_length=2)

    def getPatient(self, appoint):
        return appoint.patient

    def getLocation(self, appoint):
        return appoint.location

    def getDoctor(self, appoint):
        return appoint.doctor


# This module contains the Prescription model.
class Prescription(models.Model):
    prid = models.CharField(max_length=50, default='')
    # name = models.CharField(max_length=50, default='')
    patient = models.CharField(max_length=50, default='')
    # patient = models.ForeignKey(Patient, null=True,on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.CASCADE)
    # dosage = models.CharField(max_length=100)
    disease = models.CharField(max_length=100)
    # appt = models.ForeignKey(Appointment, null=True, on_delete=models.CASCADE)
    day = models.CharField(max_length=4)
    month = models.CharField(max_length=4)
    year = models.CharField(max_length=4)

    def __str__(self):
        return self.prid

    def getPatient(self, pre):
        return pre.patient

    def getDoctor(self, pre):
        return pre.doctor

    def getAppointment(self, pre):
        return pre.appointment


class pres(models.Model):
    pid = models.CharField(max_length=50)
    prid = models.ForeignKey(Prescription, default=None, blank=True, null=True, on_delete=models.CASCADE)
    # prid = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    dosage = models.CharField(max_length=50)

    def getPrescription(self, pid):
        return pid.prid


# This module contains the messaging model
class Message(models.Model):
    senderName = models.CharField(max_length=50, default='')
    senderType = models.CharField(max_length=50, default='')
    receiverName = models.CharField(max_length=50, default='')
    viewed = models.BooleanField(default=False)
    date = models.DateField(default=date.today())
    subjectLine = models.CharField(max_length=50, default='')
    message = models.TextField(max_length=500, default='')
    senderDelete = models.BooleanField(default=False)
    receiverDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.subjectLine

    def getSenderType(self, message):
        return message.senderType


# This module contains the LogInInfo model.
class LogInInfo(models.Model):
    username = models.CharField(max_length=30, default='')
    password = models.CharField(max_length=30, default='')

    def __str__(self):
        return self.username
