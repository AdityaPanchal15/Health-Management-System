# File: urls.py
# Description: This file contains the Django url statements.
# Author(s): Team Suites (1)

# imports
from django.urls import re_path
from . import views

# url statements
app_name = 'HealthNet'
urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(r'^register/$', views.registerP, name='registerP'),
    re_path(r'^register/$', views.adminview, name='registerA'),
    re_path(r'^register/create$', views.createPLogIn, name='createPLogIn'),
    re_path(r'^password/$', views.password, name='password'),
    re_path(r'^password/changepass/$', views.changePass, name='changepass'),
    re_path(r'^verify/$', views.verify, name='verify'),
#    re_path(r'^home/verifyDoc/$', views.verifyDoc, name='verifyDoc'),
    re_path(r'^home/$', views.home, name='home'),
    re_path(r'^home/registerDN$', views.registerDN, name='registerDN'),
    re_path(r'^home/registerDN/createDN$', views.createDNLogIn, name='createDNLogIn'),
    re_path(r'^home/registerML$', views.registerML, name='registerML'),
    re_path(r'^home/Alldocs$', views.Alldocs, name='Alldocs'),
    re_path(r'^home/registerML/createML$', views.createMLLogIn, name='createMLLogIn'),
    re_path(r'^information/$', views.information, name='information'),
    re_path(r'^information/updatePro$', views.updatePro, name='updatePro'),
    re_path(r'^information/updatePro/updateProInfo$', views.updateProInfo, name='updateProInfo'),
    re_path(r'^information/updateMed/(?P<pat_id>[0-9]+)/', views.updateMed, name='updateMed'),
    re_path(r'^information/updateMed/updateMedInfo/(?P<pat_id>[0-9]+)/', views.updateMedInfo, name='updateMedInfo'),
    re_path(r'^information/export$', views.export, name='export'),
    re_path(r'^information/tests/(?P<pat_id>[0-9]+)/', views.tests, name='tests'),
    re_path(r'^information/tests/createTest/(?P<pat_id>[0-9]+)/', views.createTest, name='createTest'),
    re_path(r'^information/tests/createTest/createTestInfo/(?P<pat_id>[0-9]+)/', views.createTestInfo, name='createTestInfo'),
    re_path(r'^information/tests/releaseTest/(?P<test_id>[0-9]+)/', views.releaseTest, name='releaseTest'),
    re_path(r'^information/testDetails/(?P<test_id>[0-9]+)/', views.testDetails, name='testDetails'),
    re_path(r'^information/discharge/(?P<pat_id>[0-9]+)/', views.discharge, name='discharge'),
    re_path(r'^information/nomore/(?P<pat_id>[0-9]+)/', views.nomore, name='nomore'),
    re_path(r'^information/admission/(?P<pat_id>[0-9]+)/(?P<emp_id>[0-9]+)/', views.admission, name='admission'),
    re_path(r'^information/transfer/(?P<pat_id>[0-9]+)/(?P<emp_id>[0-9]+)/', views.transfer, name='transfer'),
    re_path(r'^pinformation/$', views.pinformation, name='pinformation'),
    re_path(r'^appointments/$', views.appointments, name='appointments'),
    re_path(r'^appointments/createAppt$', views.createAppt, name='createAppt'),
    re_path(r'^appointments/createAppt/createApptInfo$', views.createApptInfo, name="createApptInfo"),
    re_path(r'^appointments/updateAppt/(?P<appt_id>[0-9]+)/', views.updateAppt, name='updateAppt'),
    re_path(r'^appointments/updateAppt/updateApptInfo/(?P<appt_id>[0-9]+)/', views.updateApptInfo, name='updateApptInfo'),
    re_path(r'^appointments/cancelAppt/(?P<appt_id>[0-9]+)/', views.cancelAppt, name='cancelAppt'),
    re_path(r'^appointments/doneAppt/(?P<appt_id>[0-9]+)/', views.doneAppt, name='doneAppt'),

    re_path(r'^appointments/createPres/(?P<appt_id>[0-9]+)/$', views.createPres, name='createPres'),
    re_path(r'^appointments/createPres/createPresInfo/(?P<appt_id>[0-9]+)/$', views.createPresInfo, name='createPresInfo'),
    re_path(r'^appointments/updatePres/(?P<pres_id>[0-9]+)/', views.updatePres, name='updatePres'),
    re_path(r'^appointments/updatePres/updatePresInfo/(?P<pres_id>[0-9]+)/', views.updatePresInfo, name='updatePresInfo'),
    re_path(r'^appointments/removePres/(?P<pres_id>[0-9]+)/', views.removePres, name='removePres'),
    re_path(r'^appointments/rate/(?P<appt_id>[0-9]+)/$', views.rate, name='rate'),
    re_path(r'^appointments/ratings/(?P<appt_id>[0-9]+)/$', views.ratings, name='ratings'),

    re_path(r'^pres/$', views.prescriptions, name='prescriptions'),

    re_path(r'^calendar/$', views.calendar, name='calendar'),
    re_path(r'^messages/$', views.messages, name='messages'),
    re_path(r'^messages/createMess/$', views.createMess, name='createMess'),
    re_path(r'^messages/createMess/createMessInfo/(?P<mess_id>-1)/', views.createMessInfo, name="createMessInfo"),
    re_path(r'^messages/replyMess/(?P<mess_id>[0-9]+)/', views.replyMess, name='replyMess'),
    re_path(r'^messages/replyMess/createMessInfo/(?P<mess_id>[0-9]+)/', views.createMessInfo, name="createMessInfo"),
    re_path(r'^messages/viewMess/(?P<mess_id>[0-9]+)/', views.viewMess, name='viewMess'),
    re_path(r'^messages/deleteMess/(?P<mess_id>[0-9]+)/', views.deleteMess, name='deleteMess'),
    re_path(r'^medical/$', views.medicals, name='medicals'),
    re_path(r'^all_labs/$', views.all_labs, name='all_labs'),
    re_path(r'^log/$', views.log, name='log'),
    re_path(r'^statistics/$', views.statistics, name='statistics'),
    re_path(r'^logOut/$', views.logOut, name='logOut')
]
