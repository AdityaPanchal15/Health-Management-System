from django.shortcuts import render

# Create your views here.
from django.db.models import Q, Count
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from .models import Test
from .models import RatingDoc
from .models import Patient
from .models import forstats
from .models import EmergencyContact
from .models import Doctor
from .models import Nurse
from .models import Prescription
from .models import Hospital
from .models import Appointment
from .models import LogInInfo
from .models import Administrator
from .models import Message
from .models import MedicStore
from .models import Lab
from .models import Speciality
from .models import pres

from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
import datetime
from datetime import date
import os
import csv
import json
from django import template
import simplejson
from django.utils.safestring import mark_safe

register = template.Library()

# This variable is for storing the username entered when a user logs-in
uname = ''
u_type = ''
alert = ''


@register.filter
def json(value):
    return mark_safe(simplejson.dumps(value))


# This module handles the logging of activities by saving logs to a plaintext file which is then rendered
# in HTML for administrators to view.
def medicals(request):
    global uname
    medics = MedicStore.objects.order_by('-zipcode')
    try:
        patient = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        return render(request, 'HealthNet/medical.html', {
            'error_message': "something wrong"
        })
    else:
        context = {
            'medical_store': medics,
            'patient': patient
        }
        return render(request, 'HealthNet/medical.html', context)


def all_labs(request):
    global uname
    # labs = MedicStore.objects.order_by('-zipcode')
    lab = Lab.objects.order_by('-zipcode')
    try:
        patient = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        return render(request, 'HealthNet/lab.html', {
            'error_message': "something wrong"
        })
    else:
        context = {
            # 'labs': labs,
            'patient': patient,
            'lab': lab
        }
        return render(request, 'HealthNet/lab.html', context)


def Alldocs(request):
    try:
        admin = Administrator.objects.get(username=uname)
    except Administrator.DoesNotExist:
        return HttpResponseRedirect(reverse('HealthNet/home.html', args=()))
    else:
        # d = Doctor.objects.get()
        specs = Speciality.objects.order_by("-city")
        context = {
            # 'doctors': d,
            'specs': specs
        }
        return render(request, 'HealthNet/docs.html', context)


def logActivity(activity):
    filename = "log.txt"
    cwd = os.getcwd()
    target = open(cwd + "\\HealthNet\\log\\" + filename, 'a')
    target.write(activity)
    target.write("\n")
    target.close()


# This module handles the generic template view for the index page in which users will log-in or register
# if they have not made credentials.
class IndexView(generic.ListView):
    template_name = 'HealthNet/index.html'
    context_object_name = 'user_login_information'

    def get_queryset(self):
        return LogInInfo.objects.order_by('-username')


# This module simply renders the HTML page for the registration screen.
def registerP(request):
    return render(request, 'HealthNet/registerP.html')


# This module handles the user registration. The "LogInInfo" object is used to store their credentials in the database.
def createPLogIn(request):
    firstName = (request.POST['firstName'])
    lastName = (request.POST['lastName'])
    paddress = (request.POST['address'])
    number = (request.POST['number'])
    email = (request.POST['email'])
    provider = (request.POST['provider'])
    insuranceid = (request.POST['insuranceid'])
    contactfname = (request.POST['contactfname'])
    contactlname = (request.POST['contactlname'])
    contactaddress = (request.POST['contactaddress'])
    contactnumber = (request.POST['contactnumber'])
    contactcity = (request.POST['contactcity'])
    contactstate = (request.POST['contactstate'])
    contactzip = (request.POST['contactzip'])
    height = (request.POST['height'])
    weight = (request.POST['weight'])
    allergies = (request.POST['allergies'])
    gender = (request.POST['gender'])
    username = (request.POST['username'])
    password = (request.POST['password'])
    p_city = (request.POST['ccity'])
    p_state = (request.POST['cstate'])
    p_zip = (request.POST['czip'])

    try:
        logininfo = LogInInfo.objects.get(username=username)
    except ObjectDoesNotExist:
        LogInInfo.objects.create(username=username, password=password)
        global uname
        uname = username
        try:
            contact = EmergencyContact.objects.get(firstName=contactfname, lastName=contactlname,
                                                   address=contactaddress, number=contactnumber, em_city=contactcity,
                                                   em_state=contactstate, em_zip=contactzip)
        except ObjectDoesNotExist:
            contact = EmergencyContact.objects.create(firstName=contactfname, lastName=contactlname,
                                                      address=contactaddress, number=contactnumber, em_city=contactcity,
                                                      em_state=contactstate, em_zip=contactzip)

        Patient.objects.create(username=uname)
        patient = Patient.objects.get(username=uname)
        patient.firstName = firstName
        patient.lastName = lastName
        patient.address = paddress
        patient.number = number
        patient.email = email
        patient.provider = provider
        patient.insuranceid = insuranceid
        patient.contact = contact
        patient.height = height
        patient.weight = weight
        patient.allergies = allergies
        patient.gender = gender
        # patient.patient_area=patient_area
        patient.p_city = p_city
        patient.p_state = p_state
        patient.p_zip = p_zip
        str1 = "p" + p_zip[0:3]
        count = Patient.objects.count()
        print(count)
        len1 = len(str(count))
        len1 = 8 - len1
        st = "0"
        for i in range(len1):
            str1 = str1 + st
        # count = count + 1
        str1 = str1 + str(count)
        print(str1)
        patient.pid = str1
        p_id = patient.pid
        patient.save()
        msg = 'Your Unique ID is ' + str(p_id)
        print(msg)
        activity = "User " + username + " registered a new account - logged on: " + \
                   datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
        logActivity(activity)
        send_mail('Hello from healthindia',
                  msg,
                  'healthindia319@gmail.com',
                  [email],
                  fail_silently=False)
        return HttpResponseRedirect(reverse('HealthNet:home', args=()))
    else:
        return render(request, 'HealthNet/registerP.html', {
            'username': username,
            'error_message': "Username already exists.",
        })


# This module simply renders the HTML page for the password change screen.
def password(request):
    return render(request, 'HealthNet/password.html')


# This module handles the changing of a user's password
def changePass(request):
    try:
        username = (request.POST["username"])
        newpass = (request.POST["password"])
        currinfo = LogInInfo.objects.get(username=username)
    except LogInInfo.DoesNotExist:
        return render(request, 'HealthNet/password.html', {
            'username': username,
            'error_message': "There was a problem with your username.",
        })
    else:
        currinfo.password = newpass
        currinfo.save()
        activity = "User " + username + " changed their password - logged on: " + \
                   datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
        logActivity(activity)
        return HttpResponseRedirect(reverse('HealthNet:index', args=()))


# This module handles the attempt of a user to log-in to their profile. If the username and password are valid,
# the user is redirected to their profile. If not, an error message is generated and the user is
# redirected to the index page.
def verify(request):
    username = (request.POST['username'])
    passwordInput = (request.POST['password'])
    utype = (request.POST['type'])
    global u_type
    u_type = utype
    print(u_type)
    try:
        current = LogInInfo.objects.get(username=username)
    except LogInInfo.DoesNotExist:
        return render(request, 'HealthNet/index.html', {
            'username': username,
            'error_message': "There was a problem with your username.",
        })
    else:
        passwordActual = current.password
        if passwordInput == passwordActual:
            global uname
            uname = username
            activity = "User " + username + " logged in - logged on: " + datetime.datetime.now().strftime(
                '%m/%d/%y @ %H:%M:%S')
            logActivity(activity)
            return HttpResponseRedirect(reverse('HealthNet:home', args=()))
        else:
            return render(request, 'HealthNet/index.html', {
                'username': username,
                'error_message': "There was a problem with your password.",
            })


# This module simply renders the home page for a user
def home(request):
    print(u_type)
    try:
        at = Administrator.objects.get(username=uname)
        lvl = 6
    except Administrator.DoesNotExist:
        try:
            at = Doctor.objects.get(username=uname)
            lvl = 5
        except Doctor.DoesNotExist:
            try:
                at = Nurse.objects.get(username=uname)
                lvl = 4
            except Nurse.DoesNotExist:
                try:
                    at = MedicStore.objects.get(username=uname)
                    lvl = 3
                except MedicStore.DoesNotExist:
                    try:
                        at = Lab.objects.get(username=uname)
                        lvl = 2
                    except Lab.DoesNotExist:
                        try:
                            at = Patient.objects.get(username=uname)
                            lvl = 1
                        except Patient.DoesNotExist:
                            return HttpResponseRedirect(reverse('HealthNet:logOut', args=()))
                        else:
                            utype = "Patient"
                    else:
                        utype = "Lab"
                else:
                    utype = "MedicStore"
            else:
                utype = "Nurse"
        else:
            utype = "Doctor"
    else:
        utype = "Administrator"

    if u_type == "Administrator" and lvl == 6:
        a = at
        utype = "Administrator"
        context = {'user': a,
                   'type': utype}
        return render(request, 'HealthNet/home.html', context)
    elif u_type == "Doctor" and lvl >= 5:
        d = at
        utype = "Doctor"
        context = {'user': d,
                   'type': utype}
        return render(request, 'HealthNet/home.html', context)
    elif u_type == "Nurse" and lvl >= 4:
        n = at
        utype = "Nurse"
        context = {'user': n,
                   'type': utype}
        return render(request, 'HealthNet/home.html', context)
    elif u_type == "MedicStore" and lvl >= 3:
        m = at
        utype = "MedicStore"
        context = {'user': m,
                   'type': utype}
        return render(request, 'HealthNet/home.html', context)
    elif u_type == "Lab" and lvl >= 2:
        l = at
        utype = "Lab"
        context = {'user': l,
                   'type': utype}
        return render(request, 'HealthNet/home.html', context)
    elif u_type == "Patient" and lvl >= 1:
        p = at
        utype = "Patient"
        context = {'user': p,
                   'type': utype}
        return render(request, 'HealthNet/home.html', context)
    else:
        return HttpResponseRedirect(reverse('HealthNet:logOut', args=()))


# This module simply renders the HTML page for the doctor and nurse registration screen.
def registerDN(request):
    admin = Administrator.objects.get(username=uname)
    city = admin.p_city
    workplaces = Hospital.objects.filter(hosp_city=city)
    context = {'workplaces': workplaces,
               'admin': admin}
    return render(request, 'HealthNet/registerDN.html', context)


# This module simply renders the HTML page for the doctor and nurse registration screen.
def registerML(request):
    workplaces = Hospital.objects.order_by("-name")
    admin = Administrator.objects.get(username=uname)
    context = {'workplaces': workplaces,
               'admin': admin}
    return render(request, 'HealthNet/registerML.html', context)


# This module handles the doctor and nurse registration. The "LogInInfo" object is used to store their credentials
# in the database.
def createDNLogIn(request):
    firstName = (request.POST['firstName'])
    lastName = (request.POST['lastName'])
    type = (request.POST['type'])
    username = (request.POST['username'])
    print(username)
    password = (request.POST['password'])
    paddress = (request.POST['address'])
    licid = (request.POST['licid'])
    number = (request.POST['number'])
    email = (request.POST['email'])
    provider = (request.POST['provider'])
    insuranceid = (request.POST['insuranceid'])
    contactfname = (request.POST['contactfname'])
    contactlname = (request.POST['contactlname'])
    contactaddress = (request.POST['contactaddress'])
    contactnumber = (request.POST['contactnumber'])
    contactcity = (request.POST['contactcity'])
    contactstate = (request.POST['contactstate'])
    contactzip = (request.POST['contactzip'])
    height = (request.POST['height'])
    # workplaces = (request.POST['workplaces'])
    weight = (request.POST['weight'])
    allergies = (request.POST['allergies'])
    gender = (request.POST['gender'])
    p_city = (request.POST['ccity'])
    p_state = (request.POST['cstate'])
    p_zip = (request.POST['czip'])

    admin = Administrator.objects.get(username=uname)
    try:
        logininfo = LogInInfo.objects.get(username=username)
    except ObjectDoesNotExist:
        LogInInfo.objects.create(username=username, password=password)
        try:
            contact = EmergencyContact.objects.get(firstName=contactfname, lastName=contactlname,
                                                   address=contactaddress, number=contactnumber, em_city=contactcity,
                                                   em_state=contactstate, em_zip=contactzip)
        except ObjectDoesNotExist:
            contact = EmergencyContact.objects.create(firstName=contactfname, lastName=contactlname,
                                                      address=contactaddress, number=contactnumber, em_city=contactcity,
                                                      em_state=contactstate, em_zip=contactzip)
        if type == "Doctor":
            Doctor.objects.create(username=username)
            d = Doctor.objects.get(username=username)
            workplaces = admin.workplace

            # work = Hospital.objects.get(name=workplaces)
            specs = (request.POST['member'])
            specs = int(specs)
            j = 0
            for i in range(specs):
                str1 = "member" + str(j)
                mem = (request.POST[str1])
                Speciality.objects.create(hospital=workplaces.name, doctor=d, speciality=mem, city=p_city)
                j = j + 1

            d.firstName = firstName
            d.lastName = lastName
            d.address = paddress
            d.licid = licid
            # d.doc_spec = speciality
            d.number = number
            d.email = email
            d.provider = provider
            d.insuranceid = insuranceid
            d.contact = contact
            d.height = height
            d.weight = weight
            d.allergies = allergies
            d.gender = gender
            # patient.patient_area=patient_area
            d.p_city = p_city
            d.p_state = p_state
            d.p_zip = p_zip
            str1 = "d" + p_zip[0:3]
            count = Doctor.objects.count()
            len1 = len(str(count))
            len1 = 8 - len1
            st = "0"
            for i in range(len1):
                str1 = str1 + st
            # count = count + 1
            str1 = str1 + str(count)
            d.pid = str1
            p_id = d.pid
            d.workplace = Hospital.objects.get(name=workplaces)
            # d.workplace = Hospital.objects.get(name=workplaces)
            # d.workplaces = workplaces
            d.save()

            msg = 'Your Unique ID is ' + str(p_id)
            print(msg)
            activity = "User " + username + " registered a new account - logged on: " + \
                       datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
            logActivity(activity)
            send_mail('Hello from healthindia',
                      msg,
                      'healthindia319@gmail.com',
                      [email],
                      fail_silently=False)
            return HttpResponseRedirect(reverse('HealthNet:home', args=()))
        elif type == "Nurse":
            Nurse.objects.create(username=username)
            n = Nurse.objects.get(username=username)
            n.firstName = firstName
            n.lastName = lastName
            n.address = paddress
            n.licid = licid
            # n.doc_spec = speciality
            n.number = number
            n.email = email
            n.provider = provider
            n.insuranceid = insuranceid
            n.contact = contact
            n.height = height
            n.weight = weight
            n.allergies = allergies
            n.gender = gender
            # patient.patient_area=patient_area
            n.p_city = p_city
            n.p_state = p_state
            n.p_zip = p_zip
            str1 = "n" + p_zip[0:3]
            count = Nurse.objects.count()
            print(count)
            len1 = len(str(count))
            len1 = 8 - len1
            st = "0"
            for i in range(len1):
                str1 = str1 + st
            # count = count + 1
            str1 = str1 + str(count)
            print(str1)
            n.pid = str1
            p_id = n.pid
            # n.workplace = Hospital.objects.get(name=workplaces)
            n.workplaces = admin.workplace.name
            n.save()

            msg = 'Your Unique ID is ' + str(p_id)
            activity = "Administrator " + uname + " registered a new nurse account - logged on: " + \
                       datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
            logActivity(activity)
            send_mail('Hello from healthindia',
                      msg,
                      'healthindia319@gmail.com',
                      [email],
                      fail_silently=False)
            return HttpResponseRedirect(reverse('HealthNet:home', args=()))
        # elif type == "Administrator":
        #     Administrator.objects.create(username=username, firstName=firstName, lastName=lastName)
        #     a = Administrator.objects.get(username=username)
        #     a.workplace = admin.workplace
        #     a.save()
        #     activity = "Administrator " + uname + " registered a new Administrator account - logged on: " + \
        #                datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
        #     logActivity(activity)
        #     return HttpResponseRedirect(reverse('HealthNet:home', args=()))
    else:
        return render(request, 'HealthNet/registerDN.html', {
            'username': username,
            # 'workplace': Hospital.objects.order_by("-name"),
            'error_message': username + " Username already exists.",
        })


# This module handles the doctor and nurse registration. The "LogInInfo" object is used to store their credentials
# in the database.
def createMLLogIn(request):
    firstName = (request.POST['firstName'])
    lastName = (request.POST['lastName'])
    type = (request.POST['type'])
    username = (request.POST['username'])
    print(username)
    city = (request.POST['city'])
    zipcode = (request.POST['zipcode'])
    state = (request.POST['state'])
    password = (request.POST['password'])
    admin = Administrator.objects.get(username=uname)
    try:
        logininfo = LogInInfo.objects.get(username=username)
    except ObjectDoesNotExist:
        LogInInfo.objects.create(username=username, password=password)
        if type == "Lab":
            lab_name = (request.POST['name'])
            Lab.objects.create(username=username, firstName=firstName, lastName=lastName,
                               lab_name=lab_name, city=city, zipcode=zipcode, state=state)
            activity = "Administrator " + uname + " - " + username + " registered a new lab account - logged on: " + \
                       datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
            logActivity(activity)
            return HttpResponseRedirect(reverse('HealthNet:home', args=()))
        elif type == "MedicStor":
            medic_name = (request.POST['name'])
            MedicStore.objects.create(username=username, firstName=firstName, lastName=lastName,
                                      medic_name=medic_name, city=city, zipcode=zipcode, state=state)
            activity = "Administrator " + uname + " - " + username + " registered a new medical account - logged on: " + \
                       datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
            logActivity(activity)
            return HttpResponseRedirect(reverse('HealthNet:home', args=()))
    else:
        return render(request, 'HealthNet/registerDN.html', {
            'username': username,
            # 'workplace': Hospital.objects.order_by("-name"),
            'error_message': username + " Username already exists.",
        })


# This module simply renders the HTML page for the user information screen.
def information(request):
    global uname
    global u_type
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                return render(request, 'HealthNet/index.html', {
                    'error_message': "An error has occurred"
                })
            else:
                utype = u_type
                patients = Patient.objects.order_by("-lastName")
                patw = Patient.objects.filter(hospital=n.workplace)
                context = {'patients': patients,
                           'patw': patw,
                           'employee': n,
                           'type': utype}
                return render(request, 'HealthNet/information.html', context)
        else:
            utype = u_type
            app = Appointment.objects.filter(admit='1')
            patients = Patient.objects.filter(hospital=d.workplace)
            tests = Test.objects.filter(doctor=d)
            patw = Patient.objects.filter(hospital=d.workplace)
            context = {'patient': d,
                       'tests': tests,
                       'patients': patients,
                       'app': app,
                       'patw': patw,
                       'employee': d,
                       'type': utype}
            return render(request, 'HealthNet/information.html', context)
    else:
        utype = u_type
        tests = Test.objects.filter(patient=p)
        context = {'patient': p,
                   'type': utype,
                   'tests': tests}
        return render(request, 'HealthNet/information.html', context)


# This module simply renders the HTML page for the patient information screen.
def pinformation(request):
    global uname
    if request.GET.get('pid'):
        id = request.GET.get('pid')
        try:
            p = Patient.objects.get(pid=id)
        except Patient.DoesNotExist:
            return render(request, 'HealthNet/home.html', {
                'error_message': "No Patient Available"
            })
        else:
            try:
                d = Doctor.objects.get(username=uname)
            except Doctor.DoesNotExist:
                try:
                    m = MedicStore.objects.get(username=uname)
                except MedicStore.DoesNotExist:
                    try:
                        l = Lab.objects.get(username=uname)
                    except Lab.DoesNotExist:
                        return render(request, 'HealthNet/home.html', {
                            'error_message': "No Patient Available"
                        })

                    else:
                        utype = "Lab"

                        tests = Test.objects.filter(patient=p)
                        context = {'patient': p,
                                   'tests': tests,
                                   'type': utype}
                        return render(request, 'HealthNet/pinformation.html', context)
                else:
                    utype = "MedicStore"
                    # meds = MedicStore.objects.filter(patient=p)
                    prescriptions = Prescription.objects.get(patient=p)
                    tests = Test.objects.filter(patient=p)
                    context = {'patient': p,
                               'type': utype,
                               'prescriptions': prescriptions}
                    return render(request, 'HealthNet/pinformation.html', context)
            else:
                utype = "Doctor"
                print(p.firstName)
                press = pres.objects.filter(pid=p.pid)
                prescriptions = Prescription.objects.filter(patient=p.pid, doctor=d)
                i = 0
                prids = []
                oldprid = -1
                for pr in prescriptions:
                    print(pr.prid)
                    if i == 0 or pr.prid != oldprid:
                        prids.append(pres.objects.filter(prid=pr.prid))
                        oldprid = pr.prid
                        i = i + 1

                # django_list = list(pres.objects.filter(pid=p.pid))
                # json_list = json.dumps(django_list)
                # porder = Prescription.objects.order_by("-day", "-month", "-year")

                tests = Test.objects.filter(patient=p)
                context = {'patient': p, 'prescriptions': prescriptions, 'type': utype, 'tests': tests, 'press': press,
                           'pridss': prids}
                return render(request, 'HealthNet/pinformation.html', context)

    context = {'t': "flag", 'type': "Doctor"}
    return render(request, 'HealthNet/pinformation.html', context)


# This module simply renders the HTML page for the update profile screen.
def updatePro(request):
    global uname
    try:
        patient = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            doctor = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                nurse = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                try:
                    administrator = Administrator.objects.get(username=uname)
                except Administrator.DoesNotExist:
                    return render(request, 'HealthNet/home.html', {
                        'error_message': "error occured try again after sometime."
                    })
                else:
                    context = {'patient': administrator}
                    return render(request, 'HealthNet/updatePro.html', context)
            else:
                context = {'patient': nurse}
                return render(request, 'HealthNet/updatePro.html', context)
        else:
            context = {'patient': doctor}
            return render(request, 'HealthNet/updatePro.html', context)
    else:
        context = {'patient': patient}
        return render(request, 'HealthNet/updatePro.html', context)


# This module handles modifying the database object for a patient's profile information after retrieving POST data from
# the form submission. After the object is updated and saved, the user is redirected to the user information screen.
def updateProInfo(request):
    firstName = (request.POST['firstName'])
    lastName = (request.POST['lastName'])
    paddress = (request.POST['address'])
    number = (request.POST['number'])
    email = (request.POST['email'])
    provider = (request.POST['provider'])
    insuranceid = (request.POST['insuranceid'])
    contactfname = (request.POST['contactfname'])
    contactlname = (request.POST['contactlname'])
    contactaddress = (request.POST['contactaddress'])
    contactnumber = (request.POST['contactnumber'])
    em_city = (request.POST['contactcity'])
    em_state = (request.POST['contactstate'])
    em_zip = (request.POST['contactzip'])

    p_state = (request.POST['state'])
    p_city = (request.POST['city'])
    p_zip = (request.POST['zip'])
    try:
        contact = EmergencyContact.objects.get(firstName=contactfname, lastName=contactlname, address=contactaddress,
                                               number=contactnumber, em_city=em_city,
                                               em_state=em_state, em_zip=em_zip)
    except ObjectDoesNotExist:
        contact = EmergencyContact.objects.create(firstName=contactfname, lastName=contactlname, address=contactaddress,
                                                  number=contactnumber, em_city=em_city,
                                                  em_state=em_state, em_zip=em_zip)
    try:
        user = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            user = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                user = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                return render(request, 'HealthNet/home.html', {
                    'error_message': "Try Again"
                })
            else:
                user.firstName = firstName
                user.lastName = lastName
                user.paddress = paddress
                user.number = number
                user.email = email
                user.provider = provider
                user.insuranceid = insuranceid
                user.contact = contact
                user.p_city = p_city
                user.p_state = p_state
                user.p_zip = p_zip
                user.save()
        else:
            user.firstName = firstName
            user.lastName = lastName
            user.paddress = paddress
            user.number = number
            user.email = email
            user.provider = provider
            user.insuranceid = insuranceid
            user.contact = contact
            user.p_city = p_city
            user.p_state = p_state
            user.p_zip = p_zip
            user.save()
    else:
        user.firstName = firstName
        user.lastName = lastName
        user.paddress = paddress
        user.number = number
        user.email = email
        user.provider = provider
        user.insuranceid = insuranceid
        user.contact = contact
        user.p_city = p_city
        user.p_state = p_state
        user.p_zip = p_zip
        user.save()
    activity = "User " + user.username + " updated their profile information - logged on: " + \
               datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    logActivity(activity)
    return HttpResponseRedirect(reverse('HealthNet:information', args=()))


# This module simply renders the HTML page for the update medical information screen.
def updateMed(request, pat_id):
    global uname
    patient = Patient.objects.get(id=pat_id)
    context = {'patient': patient}
    return render(request, 'HealthNet/updateMed.html', context)


# This module handles modifying the database object for a patient's medical information after retrieving POST data from
# the form submission. After the object is updated and saved, the user is redirected to the user information screen.
def updateMedInfo(request, pat_id):
    height = (request.POST['height'])
    weight = (request.POST['weight'])
    allergies = (request.POST['allergies'])
    gender = (request.POST['gender'])
    patient = Patient.objects.get(id=pat_id)
    patient.height = height
    patient.weight = weight
    patient.allergies = allergies
    patient.gender = gender
    patient.save()
    activity = "User " + uname + " updated Patient " + patient.username + "'s medical information - logged on: " + \
               datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    logActivity(activity)
    return HttpResponseRedirect(reverse('HealthNet:information', args=()))


# This module when activated, downloads the current patient's information onto their current computer in a .csv file.
def export(request):
    global uname
    patient = Patient.objects.get(username=uname)
    testResults = Test.objects.filter(patient=patient, released=True)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="PatientInfo.csv"'
    filewriter = csv.writer(response)
    filewriter.writerow(['', 'Name', 'Email', 'Address', 'Phone Number', 'Insurance ID', 'Insurance Provider'])
    filewriter.writerow(
        ['Patient Profile Info:', patient.lastName + "," + patient.firstName, patient.email, patient.paddress,
         patient.number, patient.insuranceid, patient.provider])
    filewriter.writerow([''])
    filewriter.writerow(['', 'Name', 'Address', 'Phone Number'])
    filewriter.writerow(['Patient Emergency Contact:', patient.contact.lastName + ", " + patient.contact.firstName,
                         patient.contact.address, patient.contact.number])
    filewriter.writerow([''])
    filewriter.writerow(['', 'Height', 'Weight', 'Allergies', 'Gender'])
    filewriter.writerow(
        ['Patient Medical Information:', patient.height, patient.weight, patient.allergies, patient.gender])
    filewriter.writerow([''])
    filewriter.writerow(['Patient Test Information', 'Name', 'Doctor Notes', 'Doctor Name'])
    count = 1
    for test in testResults:
        filewriter.writerow(['Test ' + str(count), test.name, test.description, test.doctor])
        count += 1
    activity = "User " + patient.username + " exported their information - logged on: " + \
               datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    logActivity(activity)
    return response


# This module handles discharging a patient from a hospital.
def discharge(request, pat_id):
    patient = Patient.objects.get(id=pat_id)
    patient.hospital = None
    patient.save()
    return HttpResponseRedirect(reverse('HealthNet:information', args=()))


# This module handles admitting a patient to a hospital.
def admission(request, pat_id, emp_id):
    patient = Patient.objects.get(pid=pat_id)
    hospital = Hospital.objects.get(name=emp_id)
    patient.hospital = hospital
    patient.save()
    return HttpResponseRedirect(reverse('HealthNet:information', args=()))


# This module handles transferring a patient from one hospital to another.
def transfer(request, pat_id, emp_id):
    patient = Patient.objects.get(pid=pat_id)
    hospital = Hospital.objects.get(hos_id=emp_id)
    patient.hospital = hospital
    patient.save()
    return HttpResponseRedirect(reverse('HealthNet:information', args=()))


# This module simply renders the HTML page for the Tests screen.
def tests(request, pat_id):
    p = Patient.objects.get(id=pat_id)
    t = Test.objects.filter(patient=p)
    context = {'patient': p,
               'test': t}
    return render(request, 'HealthNet/tests.html', context)


# This module simply renders the HTML page for the Create Test screen
def createTest(request, pat_id):
    global uname
    patient = Patient.objects.get(id=pat_id)
    context = {'patient': patient}
    return render(request, 'HealthNet/createTest.html', context)


# This module handles creating a database object for a test after retrieving POST data from the form submission.
# After the object is created and saved, the user is redirected to the main Tests screen.
def createTestInfo(request, pat_id):
    global uname
    name = (request.POST['name'])
    t = Test.objects.create()
    description = (request.POST['description'])
    try:
        if request.FILES['file']:
            file = request.FILES['file']
    except MultiValueDictKeyError:
        placeholder = ""
        t.testResults = placeholder
    else:
        t.testResults = file
    patient = Patient.objects.get(id=pat_id)
    doctor = Doctor.objects.get(username=uname)
    t.name = name
    t.description = description

    t.doctor = doctor
    t.patient = patient
    t.save()
    activity = "Doctor " + doctor.username + " created a new test for Patient " + patient.username + " - logged on: " + \
               datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    logActivity(activity)
    return HttpResponseRedirect(reverse('HealthNet:tests', args=pat_id))


# This module handles releasing a previously unreleased test for a patient. Afterwards, the user is redirected
# to the main Tests page
def releaseTest(request, test_id):
    t = Test.objects.get(id=test_id)
    t.released = True
    t.save()
    activity = "Patient " + t.patient.username + "'s test results were released by Doctor " + t.doctor.username + \
               " - logged on: " + datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    logActivity(activity)
    return HttpResponseRedirect(reverse('HealthNet:tests', args=(t.patient.id,)))


# This module simply renders the HTML page for patients to view the details of a released test
def testDetails(request, test_id):
    global uname
    test = Test.objects.get(id=test_id)
    context = {'test': test}
    return render(request, 'HealthNet/testDetails.html', context)


# This module simply renders the HTML page for the appointments screen.
# def statics(reqquest):
#     tpatient = appointments.patient
#     city = appointments.location.hosp_city
#     diseases = (request.POST['disease'])
#     critic = (request.POST['critic'])
#     stats = forstats.object.create()
#     stats.for_patient = tpatient
#     stats.current_city = city
#     stats.disease = diseases
#     stats.critic_level = critic
#     stats.month = appointments.month
#     stats.year = appointments.year
#     stats.save()


def appointments(request):
    global uname
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                return render(request, 'HealthNet/index.html', {
                    'error_message': "An error has occurred"
                })
            else:
                utype = "Nurse"
                # Nurses can create and update an appointment with a Doctor at the location they work.
                # Nurses cannot cancel appointments.
                appointments = Appointment.objects.filter(location=n.workplace, done='0')
                tpatient = appointments.patient
                city = appointments.location.hosp_city
                diseases = (request.POST['disease'])
                critic = (request.POST['critic'])
                stats = forstats.object.create()
                stats.for_patient = tpatient
                stats.current_city = city
                stats.disease = diseases
                stats.critic_level = critic
                stats.month = appointments.month
                stats.year = appointments.year
                stats.save()
                context = {'appointments': appointments,
                           'employee': n,
                           'type': utype}
                return render(request, 'HealthNet/appointments.html', context)
        else:
            utype = u_type
            # Doctors can create and update an appointment with a Doctor at a location they work.
            # Doctors can cancel THEIR appointments.

            appointments = Appointment.objects.filter(location=d.workplace, done='0')
            this_appointments = Appointment.objects.filter(doctor=d, done='0')

            context = {'appointments': appointments,
                       'this_appointments': this_appointments,
                       'employee': d,
                       'user': d,
                       'type': utype}
            return render(request, 'HealthNet/appointments.html', context)
    else:
        utype = u_type
        # Patients can create an appointment with any Doctor
        # Patients can update THEIR appointments
        # Patients can cancel THEIR appointments
        hosp = Hospital.objects.order_by("-name")
        appointments = Appointment.objects.filter(patient=p.pid, rate='0')
        app = Appointment.objects.filter(patient=p.pid)

        # done = appointments.done
        context = {'appointments': appointments,
                   'user': p,
                   'type': utype,
                   'hospital': hosp}
        return render(request, 'HealthNet/appointments.html', context)


# This module simply renders the HTML page for the create appointment screen.
def createAppt(request):
    global uname
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                return HttpResponseRedirect(reverse('HealthNet:logOut', args=()))
            else:
                utype = "Nurse"
                # Nurses can create an appointment with any patient and any Doctor from their workplace.
                patients = Patient.objects.order_by("-lastName")
                doctors = Doctor.objects.filter(workplace=n.workplace)
                context = {'patients': patients,
                           'doctors': doctors,
                           'type': utype}
                return render(request, 'HealthNet/createAppt.html', context)
        else:
            utype = "Doctor"
            spec = Speciality.objects.filter(doctor=d)
            # Doctors can create an appointment with any patient with themselves.
            patients = Patient.objects.order_by("-lastName")
            context = {'patients': patients,
                       'doctor': d,
                       'spec': spec,
                       'type': utype}
            return render(request, 'HealthNet/createAppt.html', context)
    else:
        utype = "Patient"
        city = (request.POST['contactcity'])
        city = city[1:-1]
        print(city)
        # Patients can create an appointment with any Doctor
        hospitals = Hospital.objects.filter(hosp_city=city)
        specs = Speciality.objects.filter(city=city)
        # print(specs.city)

        doctors = Doctor.objects.order_by("-lastName")
        context = {'patient': p,
                   'doctors': doctors,
                   'hospitals': hospitals,
                   'type': utype,
                   'specs': specs}
        return render(request, 'HealthNet/createAppt.html', context)


def adminview(request):
    ad = Administrator.objects.create()
    ad.firstName = Administrator.objects.get(id=(request.POST['firstName']))
    ad.lastName = Administrator.objects.get(id=(request.POST['lastName']))
    ad.username = Administrator.objects.get(id=(request.POST['username']))
    ad.password = (request.POST['password'])
    ad.save()
    return render(request, 'HealthNet/.html')


def createApptInfo(request):
    patient = (request.POST['patient'])
    doctor = Doctor.objects.get(pid=(request.POST['doctor']))
    month = (request.POST['month'])
    day = (request.POST['day'])
    year = (request.POST['year'])
    appttime = (request.POST['appttime'])
    phase = (request.POST['phase'])
    # location = doctor.workplace
    pat = Patient.objects.get(pid=patient)
    try:
        appointment = Appointment.objects.get(appttime=appttime, doctor=doctor, month=month, day=day, year=year,
                                              phase=phase)
    except Appointment.DoesNotExist:
        hp = Appointment.objects.create()
        hp.patient = patient
        hp.doctor = doctor
        hp.month = month
        hp.day = day
        hp.year = year
        hp.appttime = appttime
        hp.phase = phase
        hp.location = doctor.workplace
        hp.save()
        pat.hospital = doctor.workplace
        pat.save()
        # activity = "User " + uname + " created an appointment @ " + location.name + " on " + month + "." + day + "." +\
        #             year + "," + appttime + " " + phase + " - logged on: " + datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
        # logActivity(activity)
        return HttpResponseRedirect(reverse('HealthNet:appointments', args=()))
    else:
        try:
            p = Patient.objects.get(username=uname)
        except Patient.DoesNotExist:
            try:
                d = Doctor.objects.get(username=uname)
            except Doctor.DoesNotExist:
                try:
                    n = Nurse.objects.get(username=uname)
                except Nurse.DoesNotExist:
                    return HttpResponseRedirect(reverse('HealthNet:logOut', args=()))
                else:
                    utype = "Nurse"
                    # Nurses can create an appointment with any patient and any Doctor from their workplace.
                    patients = Patient.objects.order_by("-lastName")
                    doctors = Doctor.objects.filter(workplace=n.workplace)
                    context = {'patients': patients,
                               'doctors': doctors,
                               'type': utype,
                               'error_message': "The appointment could not be created, the doctor is busy at that time."}
                    return render(request, 'HealthNet/createAppt.html', context)
            else:
                utype = "Doctor"
                # Doctors can create an appointment with any patient with themselves.
                patients = Patient.objects.order_by("-lastName")
                context = {'patients': patients,
                           'doctor': d,
                           'type': utype,
                           'error_message': "The appointment could not be created, the doctor is busy at that time."}
                return render(request, 'HealthNet/createAppt.html', context)
        else:
            utype = "Patient"
            # Patients can create an appointment with any Doctor
            doctors = Doctor.objects.order_by("-lastName")
            context = {'patient': p,
                       'doctors': doctors,
                       'type': utype,
                       'error_message': "The appointment could not be created, the doctor is busy at that time."}
            return render(request, 'HealthNet/createAppt.html', context)


# This module simply renders the HTML page for the update appointment screen.
def updateAppt(request, appt_id):
    global uname
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                return HttpResponseRedirect(reverse('HealthNet:logOut', args=()))
            else:
                utype = "Nurse"
                # Nurses can update an appointment to be with any Doctor from their workplace

                appointment = Appointment.objects.get(id=appt_id)
                patient = appointment.patient

                doctors = Doctor.objects.filter(workplace=n.workplace)
                context = {'appointment': appointment,
                           'patient': patient,
                           'doctors': doctors,
                           'type': utype}
                return render(request, 'HealthNet/updateAppt.html', context)
        else:
            utype = "Doctor"
            # Doctors can update an appointment to be with any Doctor from their workplace

            appointment = Appointment.objects.get(id=appt_id)
            patient = appointment.patient
            doctors = Doctor.objects.filter(workplace=d.workplace)
            context = {'appointment': appointment,
                       'patient': patient,
                       'doctors': doctors,
                       'type': utype}
            return render(request, 'HealthNet/updateAppt.html', context)
    else:
        utype = "Patient"
        # Patients can update an appointment to be with any Doctor
        appointment = Appointment.objects.get(id=appt_id)
        doctors = Doctor.objects.order_by("-lastName")
        context = {'appointment': appointment,
                   'patient': p,
                   'doctors': doctors,
                   'type': utype}
        return render(request, 'HealthNet/updateAppt.html', context)


# This module handles modifying the database object for an appointment after retrieving POST data from the form
# submission. After the object is updated and saved, the user is redirected to their appointments screen.
def updateApptInfo(request, appt_id):
    doctor = Doctor.objects.get(id=(request.POST['doctor']))
    month = (request.POST['month'])
    day = (request.POST['day'])
    year = (request.POST['year'])
    appttime = (request.POST['appttime'])
    phase = (request.POST['phase'])

    location = doctor.workplace
    try:
        appointment = Appointment.objects.get(appttime=appttime, doctor=doctor, month=month, day=day, year=year,
                                              phase=phase)
    except Appointment.DoesNotExist:
        appt = Appointment.objects.get(id=appt_id)
        appt.doctor = doctor
        appt.month = month
        appt.day = day
        appt.year = year
        appt.appttime = appttime
        appt.phase = phase
        appt.location = location
        appt.save()
        activity = "User " + uname + " updated Appointment #" + appt_id + " - logged on: " + \
                   datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
        logActivity(activity)
        return HttpResponseRedirect(reverse('HealthNet:appointments', args=()))
    else:
        try:
            p = Patient.objects.get(username=uname)
        except Patient.DoesNotExist:
            try:
                d = Doctor.objects.get(username=uname)
            except Doctor.DoesNotExist:
                try:
                    n = Nurse.objects.get(username=uname)
                except Nurse.DoesNotExist:
                    return HttpResponseRedirect(reverse('HealthNet:logOut', args=()))
                else:
                    utype = "Nurse"
                    if appt_id.patient[0] == "p":
                        patient = Patient.objects.get(pid=appointment.patient)
                    elif appt_id.patient[0] == "d":
                        patient = Doctor.objects.get(pid=appointment.patient)
                    else:
                        patient = Nurse.objects.get(pid=appointment.patient)
                    # Nurses can update an appointment to be with any Doctor from their workplace
                    appointment = Appointment.objects.get(id=appt_id)
                    doctors = Doctor.objects.filter(workplace=n.workplace)
                    context = {'appointment': appointment,
                               'patient': patient,
                               'doctors': doctors,
                               'type': utype,
                               'error_message': "The appointment could not be created, the doctor is busy at that time."}
                    return render(request, 'HealthNet/updateAppt.html', context)
            else:
                utype = "Doctor"
                if appt_id.patient[0] == "p":
                    patient = Patient.objects.get(pid=appointment.patient)
                elif appt_id.patient[0] == "d":
                    patient = Doctor.objects.get(pid=appointment.patient)
                else:
                    patient = Nurse.objects.get(pid=appointment.patient)
                # Doctors can update an appointment to be with any Doctor from their workplace
                appointment = Appointment.objects.get(id=appt_id)
                doctors = Doctor.objects.filter(workplace=d.workplace)
                context = {'appointment': appointment,
                           'patient': patient,
                           'doctors': doctors,
                           'type': utype,
                           'error_message': "The appointment could not be created, the doctor is busy at that time."}
                return render(request, 'HealthNet/updateAppt.html', context)
        else:
            utype = "Patient"
            # Patients can update an appointment to be with any Doctor
            appointment = Appointment.objects.get(id=appt_id)
            doctors = Doctor.objects.order_by("-lastName")
            context = {'appointment': appointment,
                       'patient': p,
                       'doctors': doctors,
                       'type': utype,
                       'error_message': "The appointment could not be created, the doctor is busy at that time."}
            return render(request, 'HealthNet/updateAppt.html', context)


# This module handles deleting the database object for an appointment. Afterwards, the user is redirected to
# their appointments screen.
def cancelAppt(request, appt_id):
    Appointment.objects.get(id=appt_id).delete()
    activity = "User " + uname + " cancelled Appointment #" + appt_id + " - logged on: " + \
               datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    logActivity(activity)
    return HttpResponseRedirect(reverse('HealthNet:appointments', args=()))


# This module handles creating a database object for a prescription after retrieving POST data from the form submission.
#  After the object is created and saved, the user is redirected to the prescriptions screen.
def createPresInfo(request, appt_id):
    global uname
    app = Appointment.objects.get(id=appt_id)
    try:
        pat = Patient.objects.get(pid=(request.POST['patient']))
    except Patient.DoesNotExist:
        try:
            pat = Doctor.objects.get(pid=(request.POST['patient']))
        except Doctor.objects.get(pid=(request.POST['patient'])):
            try:
                pat = Nurse.objects.get(pid=(request.POST['patient']))
            except:
                return HttpResponseRedirect(reverse('HealthNet:appointments', args=()))
            else:
                patid = (request.POST['patient'])
        else:
            patid = (request.POST['patient'])
    else:
        patid = (request.POST['patient'])
    admit = (request.POST['admit'])
    global uname
    doctor = Doctor.objects.get(username=uname)
    # app = Appointment.objects.get(patient=patid)
    # app = Appointment.objects.get(id=appt_id)
    app.done = "1"
    app.admit = admit

    # print(app.location.hosp_city)
    city = app.location.hosp_city
    app.save()
    appointments = Appointment.objects.filter(location=doctor.workplace)
    # this_appointments = Appointment.objects.filter(doctor=d)
    tpatient = pat.username
    diseases = (request.POST['disease'])
    critic = (request.POST['critic_level'])

    # name = (request.POST['name'])
    specs = (request.POST['member'])
    specs = int(specs)
    j = 0
    pre = Prescription.objects.create()
    for i in range(specs):
        str1 = "member" + str(j)
        mem = (request.POST[str1])
        pres.objects.create(prid=Prescription.objects.count(), pid=patid, name=mem)
        p = pres.objects.get(name=mem)
        str1 = "member1" + str(j)
        mem = (request.POST[str1])
        p.dosage = mem
        p.save()
        j = j + 1
    stats = forstats.objects.create()
    stats.for_patient = tpatient
    stats.current_city = city
    stats.disease = diseases
    stats.critic_level = critic
    stats.month = app.month
    stats.year = app.year
    stats.save()

    # doctor = Doctor.objects.get(username=uname)

    # pre.name = name
    # pre.dosage = dosage
    pre.prid = Prescription.objects.count()
    pre.doctor = doctor
    pre.patient = patid
    pre.disease = diseases
    pre.day = app.day
    pre.month = app.month
    pre.year = app.year
    pre.save()

    activity = "Doctor " + doctor.username + " created a prescription for Patient " + pat.username + \
               " - logged on: " + datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    logActivity(activity)
    return HttpResponseRedirect(reverse('HealthNet:appointments', args=()))


def doneAppt(request, appt_id):
    return HttpResponseRedirect(reverse('HealthNet:appointments', args=()))


def rate(request, appt_id):
    context = {'appt_id': appt_id}
    return render(request, 'HealthNet/ratings.html', context)


def ratings(request, appt_id):
    global uname
    p = Patient.objects.get(username=uname)
    app = Appointment.objects.get(id=appt_id)
    pat = Patient.objects.get(pid=app.patient)
    doc = app.doctor
    if app.rate == "0":
        tpatient = pat.username
        city = doc.workplace.hosp_city
        review = (request.POST['review'])
        rate1 = (request.POST['type'])
        rats = RatingDoc.objects.create()
        rats.rating = rate1
        rats.doc = doc.username
        rats.review = review
        rats.location = city
        rats.for_patient = tpatient
        app.rate = '1'
        app.save()
        rats.save()
    return HttpResponseRedirect(reverse('HealthNet:appointments', args=()))


# This module simply loads the HTML page for the prescriptions screen.
def prescriptions(request):
    global u_type
    global uname
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                return render(request, 'HealthNet/index.html', {
                    'error_message': "An error has occurred"
                })
            else:
                utype = u_type
                press = Prescription.objects.filter(doctor=n)
                context = {'prescriptions': press,
                           'type': utype,
                           'employee': n}
                return render(request, 'HealthNet/prescriptions.html', context)
        else:
            presatw = Prescription.objects.filter(doctor=d)
            # print(presatw[0].patient)
            pat = []
            j = 0
            oldpat = -1
            for i in presatw:
                if j == 0 or i.patient != oldpat:
                    pat.append(i.patient)
                    oldpat = i.patient
                    j = j + 1
            print(pat)
            press = pres.objects.filter(pid__in=pat)
            utype = u_type
            if utype == "Doctor":

                presss = Prescription.objects.filter(doctor=d)
                context = {'prescriptions': presss,
                           'presatw': presatw,
                           'press': press,
                           'type': utype,
                           'employee': d}
            else:
                presss = Prescription.objects.filter(doctor=d)
                context = {'prescriptions': presss,
                           'type': utype,
                           'press': press,
                           'patient': d}
            return render(request, 'HealthNet/prescriptions.html', context)
    else:
        utype = u_type
        presss = Prescription.objects.filter(patient=p.pid)

        context = {'prescriptions': presss,
                   'type': utype,
                   'patient': p}
        return render(request, 'HealthNet/prescriptions.html', context)


def nomore(request, pat_id):
    # p_city= request.GET.get('city')
    # p_disease=request.GET.get('disease')
    patient = Patient.objects.get(id=pat_id)
    p = patient.username
    patient.sactive = "0"
    patient.save()
    stat = forstats.objects.filter(for_patient=p)
    co = forstats.objects.filter(for_patient=p).count()
    co = int(co)
    for f in stat:
        f.death = "1"
        co = co - 1
        disease = f.disease
        city = f.current_city
        f.save()
        if co < 2:
            f.delete()
            break

    # diseses = 'cold'

    total_count = Patient.objects.count()
    # city = 'anand'
    month = datetime.datetime.now().strftime('%mon')

    total_death = forstats.objects.values('death').count()
    total_death_disease_wise = forstats.objects.count()

    total_people = Patient.objects.count()
    print(total_death_disease_wise)
    print(total_people)
    threepercentoftotal = int((total_people * 3) / 100)
    if total_death_disease_wise > threepercentoftotal:
        msg = "due to " + str(disease) + " " + str(total_death_disease_wise) + " death has occured."
        send_mail('Hello from healthindia',
                  msg,
                  'healthindia319@gmail.com',
                  ['kushrana2015@gmail.com'],
                  fail_silently=True)
        alert = msg
        return render(request, 'HealthNet/home.html', {
            'error_message': msg
        })

        # return render(request, 'HealthNet:pradiction.html', {
        #     'chart_title': 'City Wise Pradiction Chart',
        #     'total_count': total_count,
        #     'disease': info,
        #     'data': 'Disease',
        #     'categories': json.dumps(categories),
        #     'survived_series': json.dumps(survived_series),
        # })
    else:
        return HttpResponseRedirect(reverse('HealthNet:information', args=()))

        # msg = "you need to get ready for " + disease + " . because of it " + total_death + " has been occured."
        # send_mail('Hello from healthindia',
        #           msg,
        #           'healthindia319@gmail.com',
        #           ['kushrana2015@gmail.com'],
        #           fail_silently=False)
        # print(total_death)
        # print(total_death_disease_wise)


def statistics(request):
    global uname
    global u_type
    try:
        a = Administrator.objects.get(username=uname)
    except Administrator.DoesNotExist:
        return render(request, 'HealthNet/index.html', {
            'error_message': "An error has occurred"
        })
    else:
        if request.GET.get('city') and not request.GET.get('month') and not request.GET.get('disease'):
            f_city = request.GET.get('city')
            f_city = f_city[1:-1]

            total_count = Patient.objects.filter(p_city=f_city).count()

            # print(total_allergies_count)
            dataset = forstats.objects \
                .values('disease') \
                .filter(current_city=f_city) \
                .annotate(DiseaseCount=Count('disease')) \
                .order_by('-disease')

            categories = list()
            survived_series = list()

            for entry in dataset:
                categories.append(entry['disease'])
                survived_series.append((float(entry['DiseaseCount']) / float(total_count)) * 100)

            return render(request, 'HealthNet/statistics.html', {
                'chart_title': 'City and State Wise Disease Chart',
                'total_count': total_count,
                'disease': f_city,
                'data': 'Disease',
                'categories': json.dumps(categories),
                'survived_series': json.dumps(survived_series),
                'type': u_type
            })
        elif request.GET.get('city') and request.GET.get('month'):
            f_city = request.GET.get('city')
            f_city = f_city[1:-1]
            f_month = request.GET.get('month')
            # f_month = f_month[:-1]

            total_count = Patient.objects.filter(p_city=f_city).count()

            dataset = forstats.objects \
                .values('disease') \
                .filter(Q(month=f_month) & Q(current_city=f_city)) \
                .annotate(DiseaseCount=Count('disease')) \
                .order_by('-disease')

            categories = list()
            survived_series = list()

            for entry in dataset:
                categories.append(entry['disease'])
                survived_series.append((float(entry['DiseaseCount']) / float(total_count)) * 100)

            return render(request, 'HealthNet/statistics.html', {
                'chart_title': 'City & Month Wise Disease Chart',
                'total_count': total_count,
                'disease': f_city,
                'data': 'Disease',
                'categories': json.dumps(categories),
                'survived_series': json.dumps(survived_series),
                'type': u_type
            })
        elif request.GET.get('disease'):

            f_disease = request.GET.get('disease')

            total_count = Patient.objects.filter().count()
            # print(total_patient)
            dataset = forstats.objects \
                .values('current_city') \
                .filter(disease=f_disease) \
                .annotate(DiseaseCount=Count('disease')) \
                .order_by('-current_city')

            categories = list()
            survived_series = list()

            for entry in dataset:
                categories.append(entry['current_city'])
                survived_series.append((float(entry['DiseaseCount']) / float(total_count)) * 100)

            return render(request, 'HealthNet/statistics.html', {
                'chart_title': 'Ratio of Disease in cities',
                'total_count': total_count,
                'disease': f_disease,
                'data': 'City',
                'categories': json.dumps(categories),
                'survived_series': json.dumps(survived_series),
                'type': u_type
            })

        else:
            context = {'t': "flag",
                       'type': u_type}
            return render(request, 'HealthNet/statistics.html', context)


# This module simply renders the HTML page for the create prescription screen.
def createPres(request, appt_id):
    app = Appointment.objects.get(id=appt_id)
    pat = Patient.objects.get(pid=app.patient)
    username = pat.username
    try:
        patients = Patient.objects.get(username=username)
    except Patient.DoesNotExist:
        try:
            patients = Doctor.objects.get(username=username)
        except Doctor.DoesNotExist:
            try:
                patients = Nurse.objects.get(username=username)
            except Nurse.DoesNotExist:
                return render(request, 'HealthNet/createPres.html', {
                    'error_message': "No Users"
                })

    context = {'patients': patients,
               'appoinments': app}
    return render(request, 'HealthNet/createPres.html', context)
    # return HttpResponseRedirect(reverse('HealthNet:appointments', args=()))


# This module simply renders the HTML page for the update prescriptions screen.
def updatePres(request, pres_id):
    p = Prescription.objects.get(id=pres_id)
    patients = Patient.objects.order_by("-lastName")
    context = {'patients': patients,
               'prescription': p}
    return render(request, 'HealthNet/updatePres.html', context)


# This module handles modifying the database object after retrieving POST data from the form submission.
# After the object is updated and saved, the doctor is redirected to their prescriptions screen.
def updatePresInfo(request, pres_id):
    name = (request.POST['name'])
    dosage = (request.POST['dosage'])
    patient = (request.POST['patient'])
    doctor = Doctor.objects.get(username=uname)
    pre = Prescription.objects.get(id=pres_id)
    pre.name = name
    pre.dosage = dosage
    pre.doctor = doctor
    pre.patient = patient
    pre.save()
    activity = "Doctor " + doctor.username + " updated Prescription #" + pres_id + " for Patient " + patient + \
               " - logged on: " + datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    logActivity(activity)
    return HttpResponseRedirect(reverse('HealthNet:appointments', args=()))


# This module handles deleting the database object for a prescription. Afterwards, the doctor is redirected to
# their prescriptions screen.
def removePres(request, pres_id):
    Prescription.objects.get(id=pres_id).delete()
    activity = "Doctor " + uname + " removed Prescription #" + pres_id + " - logged on: " + \
               datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    logActivity(activity)
    return HttpResponseRedirect(reverse('HealthNet:prescriptions', args=()))


# This module simply renders the HTML page for the calendar screen.
def calendar(request):
    global uname
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                return render(request, 'HealthNet/index.html', {
                    'error_message': "An error has occurred"
                })
            else:
                utype = "Nurse"
                # Nurses can view all appointments for the day and week between patients and doctors, in their workplace
                appts = Appointment.objects.filter(location=n.workplace)
                context = {'appointments': appts,
                           'user': n,
                           'type': utype}
                return render(request, 'HealthNet/calendar.html', context)
        else:
            utype = "Doctor"
            # Doctors can view all of their appointments on the calendar
            appts = Appointment.objects.filter(doctor=d)
            context = {'appointments': appts,
                       'user': d,
                       'type': utype}
            return render(request, 'HealthNet/calendar.html', context)
    else:
        utype = "Patient"
        # Patients can view all of their appointments on the calendar
        appts = Appointment.objects.filter(patient=p)
        context = {'appointments': appts,
                   'user': p,
                   'type': utype}
        return render(request, 'HealthNet/calendar.html', context)


# This module simply renders the activity log for an administrator account
def log(request):
    global uname
    try:
        a = Administrator.objects.get(username=uname)
    except Administrator.DoesNotExist:
        return render(request, 'HealthNet/index.html', {
            'error_message': "An error has occurred"
        })
    else:
        filename = "log.txt"
        cwd = os.getcwd()
        target = open(cwd + "\\HealthNet\\log\\" + filename, 'r')
        appString = target.readline()
        logString = []
        while appString != "":
            logString.append(appString)
            appString = target.readline()
        target.close()
        context = {'logString': logString}
        return render(request, 'HealthNet/log.html', context)


# This module simply renders the statistics page for an administrator account
# def statistics(request):
#     global uname
#     try:
#         a = Administrator.objects.get(username=uname)
#     except Administrator.DoesNotExist:
#         return render(request, 'HealthNet/index.html', {
#             'error_message': "An error has occurred"
#         })
#     else:
#         admins = Administrator.objects.count()
#         doctors = Doctor.objects.count()
#         nurses = Nurse.objects.count()
#         patients = Patient.objects.count()
#         appts = Appointment.objects.count()
#         pres = Prescription.objects.count()
#         statis=forstats.objects.order_by("-current_city")
#         context = {'admins': admins,
#                    'doctors': doctors,
#                    'nurses': nurses,
#                    'patients': patients,
#                    'appointments': appts,
#                    'prescriptions': pres,
#                    'statistics':statis}
#         return render(request, 'HealthNet/statistics.html', context)
#


# This module simply renders the main messaging page for a user. All of their received and sent message are displayed
# on the page, with various options for the user to choose from.
def messages(request):
    global uname
    try:
        m = Message.objects.filter(receiverDelete=False)
        mess = m.filter(receiverName=uname)
    except Message.DoesNotExist:
        mess = ''
        try:
            sm = Message.objects.filter(senderDelete=False)
            sendmess = sm.filter(senderName=uname)
        except Message.DoesNotExist:
            sendmess = ''
            try:
                p = Patient.objects.get(username=uname)
            except Patient.DoesNotExist:
                try:
                    d = Doctor.objects.get(username=uname)
                except Doctor.DoesNotExist:
                    try:
                        n = Nurse.objects.get(username=uname)
                    except Nurse.DoesNotExist:
                        try:
                            a = Administrator.objects.get(username=uname)
                        except Administrator.DoesNotExist:
                            return render(request, 'HealthNet/index.html', {
                                'error_message': "An error has occurred"
                            })
                        else:
                            utype = "Administrator"
                    else:
                        utype = "Nurse"
                else:
                    utype = "Doctor"
            else:
                utype = "Patient"
    else:
        context = {'messages': mess,
                   'type': u_type}
        return render(request, 'HealthNet/messages.html', context)


# This module simply renders the create message page for a user.
def createMess(request):
    global uname
    logins = LogInInfo.objects.all()
    context = {'logins': logins}
    return render(request, 'HealthNet/createMess.html', context)


# This module simply renders the reply message page for a user.
def replyMess(request, mess_id):
    global uname
    logins = LogInInfo.objects.all()
    context = {'logins': logins,
               'message': Message.objects.get(id=mess_id)}
    return render(request, 'HealthNet/replyMess.html', context)


# This module handles creating a database object for a message after retrieving POST data from the form submission.
# After the object is created and saved, the user is redirected to the main messages page.
def createMessInfo(request, mess_id):
    global uname
    subject = (request.POST['subject'])
    description = (request.POST['message'])
    m = Message.objects.create()
    if mess_id != "-1":
        replyMess = Message.objects.get(id=mess_id)
        if replyMess.senderName == uname:
            m.receiverName = replyMess.receiverName
            m.subjectLine = "RE - " + subject
        else:
            m.receiverName = replyMess.senderName
            m.subjectLine = "RE - " + subject
    else:
        username = LogInInfo.objects.get(id=(request.POST['users'])).username
        m.receiverName = username
        m.subjectLine = subject
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                try:
                    a = Administrator.objects.get(username=uname)
                except Administrator.DoesNotExist:
                    return HttpResponseRedirect(reverse('HealthNet:logOut', args=()))
                else:
                    utype = "Administrator"
            else:
                utype = "Nurse"
        else:
            utype = "Doctor"
    else:
        utype = "Patient"
    m.senderName = uname
    m.senderType = utype
    m.date = date.today()
    m.message = description
    m.save()
    activity = utype + " " + uname + " sent a message to " + m.receiverName + " - logged on: " + \
               datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    logActivity(activity)
    return messages(request)


# This module simply displays the View Message page for a user when they select the option to view a received/sent
# message.
def viewMess(request, mess_id):
    global uname
    mess = Message.objects.get(id=mess_id)
    context = {'message': mess}
    return render(request, 'HealthNet/viewMess.html', context)


# This module handles deleting a preexisting message from a user's inbox.
def deleteMess(request, mess_id):
    global uname
    mess = Message.objects.get(id=mess_id)
    if uname == mess.senderName:
        mess.senderDelete = True
        mess.save()
    else:
        mess.receiverDelete = True
        mess.save()

    if mess.senderDelete is True and mess.receiverDelete is True:
        mess.delete()

    activity = uname + " deleted message# " + mess_id + " - logged on: " + \
               datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    logActivity(activity)
    return HttpResponseRedirect(reverse('HealthNet:messages', args=()))


# This module handles logging-out a user. Afterwards the user is redirected to the index screen.
def logOut(request):
    global uname
    activity = "User " + uname + " logged out - logged on: " + datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    uname = ''
    logActivity(activity)
    return HttpResponseRedirect(reverse('HealthNet:index', args=()))
