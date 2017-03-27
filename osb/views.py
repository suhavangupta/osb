#update the number of rows before reading the file
from django.core.cache import cache
from ezodf import opendoc,Sheet
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import crypto
import string
import random
from django.core.mail import EmailMessage
from django.db.models import Sum
import os,subprocess,sys
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core import serializers

# Create your views here.
from django.contrib.auth.models import User
from .models import UserData,Slot,ExcelData
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
#from random import random
# Create your views here.


def random_password_generate(size = 6,charts = string.ascii_uppercase+string.digits):           #complete
    return ''.join(random.choice(charts) for i in range(size))


def return_time(x):
    if x%2 != 0:
        x = int(x/2)
        format1 = "am"
        x = x + 8
        if x == 12 :
            print str(str(x)+":00 pm" +" to "+ str(x)+":30 pm" )
            return str(str(x)+":00 pm" +" to "+ str(x)+":30 pm" )
        if (x > 12):
            x = x - 12
            format1 = "pm"
        print str(str(x)+":00"+format1 + " to "+ str(x)+":30"+format1)
        return str(str(x)+":00"+format1 + " to "+ str(x)+":30"+format1)
    else:
        x = int(x/2)
        x = x+7
        format1 = "am"
        if x == 11 :
            print str(str(x)+":30 am" +" to "+ str(x+1)+":00 pm" )
            return str(str(x)+":30 am" +" to "+ str(x+1)+":00 pm" )
        if x == 12 :
            print str("12:30 pm" +" to "+"1:00 pm")
            return str("12:30 pm" +" to "+"1:00 pm")

        if x > 12 :
            format1 = "pm"
            x = x-12

        print str(str(x)+":30"+format1 +" to "+ str(x+1)+":00" +format1)
        return str(str(x)+":30"+format1 +" to "+ str(x+1)+":00" +format1)


@csrf_exempt
def home(request):          #complete
    return render(request,'Login.html')

@csrf_exempt
def resend_mail_password(request):           #under testing not complete
    if request.method == "POST":
        registration_id = request.POST['username']
        event_flag = request.POST['event']
        mobile_no = request.POST['mobile_no']
        participant = UserData.objects.filter(registration_id = registration_id,event_flag = event_flag)
        for temp in participant:
            if temp.mobile_no1 == mobile_no or temp.mobile_no2 == mobile_no:
                temp_user = User.objects.get(username = temp.user.username)
                if temp.event_flag == 0 :
                    event = "Reverse Coding"
                else:
                    event = "Clash"
                body = "Dear Participant,\n\nGreetings from the team PISB!\nYou have participated in Credenz'16 in event " + str(event) +". Slot booking for the same has started at url:  http://pisbcredenz.pythonanywhere.com. \nIt is compulsary to book your slot to participate in the event.\n\tYour login credentials are:\n\t\tUsername         : "+str(temp.user.username)+"\n\t\tPassword         : "+str(temp.password)+"\n\t\tMobile No.        : Mobile number given while registration.\n\t\tRegistration No.  : Registration number is same as receipt number. \n\n\tInsructions:\n\t\t1)If in case you didn't get receipt number then your receipt number will be 9999.\n\t\t2) Mobile number of any one of the team member is valid which is submitted while registration.\n\t\t3) Only one slot will be booked for individual or team participation.\n\t\t4) Slots are available for round 1 only on 9th and 10th of September.\n\t\t5) Slots are scheduled for 30 minutes each.\n\t\t6) Once the slot is booked, it cannot be cancelled or changed.\n\t\t7) In case of any problem contact us with the details provided on the website.\nReguards,\nPICT IEEE Student Branch"
                subject="Slot booking for "+str(event)+"CREDENZ'16"
                email_list = []
                print temp_user.userdata.email1
                if temp.email1 != None:
                    email_list.append(temp.email1)
                if temp.email2 != None:
                    email_list.append(temp.email2)
               # email_list.append(temp.email1)
               # email_list.append(temp.email2)
                email = EmailMessage(subject, body,to=email_list)
                print email_list
                try:
                    email.send()
                    return render(request,'Login.html',{'message':'Email successfully sent'})
                except:
                    return render(request,'Login.html',{'message':'Connection error... try again!'})
        else:
            return render(request,'Login.html',{'message':'Invalid Data'})
    else:
        return render(request,'Login.html')

@csrf_exempt
def resend_confirmation_mail(request):           #under testing
    if request.method == "POST":
        username = request.POST['username']
        if User.objects.filter(username = username).exists() :
            temp_user = User.objects.get(username = username)
            if temp_user.userdata.slot_booked == 1:
                if temp_user.userdata.event_flag == 0 :
                    event = "Reverse Coding"
                else:
                    event = "Clash"

                body = "Dear Participant,\n\nGreetings from the team "+str(event)+" ,CREDENZ'16!\nYour slot has been successfully booked. Details of slot are as follows\n\tTime  : "+str(return_time(temp_user.userdata.slot.time_slot))+"\n\tDate  : "+str(temp_user.userdata.slot.date_slot) +"th September, 2016\n\tVenue : PICT, Dhankawadi, Pune\n\tUsername : "+str(temp_user.username)+"\nInstructions:\n\t1) Icard for your respective college is necessary.\n\t2) Further details will be provided at venue.\n\t3) Report on venue 20 minutes before scheduled time along with the printout of this mail.\n\t4) Slot cannot be cancelled or booked again.\n\t5) Keep checking are website www.credenz.info to stay updated.\nReguards,\nPICT IEEE Student Branch"
                subject="Confirmation mail for slot booking for the event "+str(event)+"CREDENZ'16"
                email_list = []
                print temp_user.userdata.email1
                if temp_user.userdata.email1 != None:
                    email_list.append(temp_user.userdata.email1)
                if temp_user.userdata.email2 != None:
                    email_list.append(temp_user.userdata.email2)
                #email_list.append(temp_user.userdata.email1)
                #email_list.append(temp_user.userdata.email2)
                email = EmailMessage(subject, body,to=email_list)
                print email_list
                try:
                    email.send()
                    return render(request,'Login.html',{'message':'Email successfully sent'})
                except:
                    return render(request,'Login.html',{'message':'Connection error... try again!'})
            else:
                return render(request,'Login.html',{'message':'Book your slot first'})
        else:
            return render(request,'Login.html',{'message':'Invalid Username'})
    else:
        return render(request,'Login.html')

@csrf_exempt
def log_in(request):
    if request.method == "POST" :
        username = request.POST['username']
        registration_id = request.POST['registration_no']
        password = request.POST['password']
        mobile_no = request.POST['mobile_no']
        #mobile_no = request.POST['mobile_no']
        print username
        if request.POST['event'] == '1':
            event = 1
            event_name = "CLASH"
        else:
            event = 0
            event_name = "Reverse Coding"
        reload(sys)
        sys.setdefaultencoding('utf-8')

        user = authenticate(username = username,password = password)
        print user
        if user is not None and  user.userdata.event_flag == event and (user.userdata.mobile_no1 == mobile_no or user.userdata.mobile_no2 == mobile_no) and user.userdata.registration_id == int(registration_id):
            print user
            if  user.userdata.slot_booked != 1:
                login(request,user)
                slot_matrix = [[0 for x in range(20)] for y in range(2)]
                for i in range(2):      #Discuss the format of time
                    for j in range(20):
                        slot_matrix[i][j] = Slot.objects.filter(event_flag = event,date_slot = i+9,time_slot = j+1).aggregate(Sum('comp_avail'))
                        slot_matrix[i][j] = slot_matrix[i][j]['comp_avail__sum']
                        if slot_matrix[i][j] == None:
                            slot_matrix[i][j] = 0
                return render(request,'Userslot.html',{'slot9':slot_matrix[0],'slot10':slot_matrix[1],'event_name':event_name})
            else:
                return render(request,'Login.html',{'message':'You have already booked your slot'})
        else:
            return render(request,'Login.html',{'message':'invalid registration no or password or username'})
    else:
        return render(request,'Login.html')



@csrf_exempt
def authenticate_func(request):         #complete
    return render(request,'Adminlogin.html')



@csrf_exempt
def admin_func(request):            #complete
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        if username == "pisb_credenz" and password == "pisb_clash_rc@2016":
            user = authenticate(username = username,password = password)
            login(request,user)
            return render(request,'Adminpage.html')
        else:
            return render(request,'Adminlogin.html',{'message':'Invalid username and password'})

    return render(request,'Adminlogin.html')



@csrf_exempt
def get_data_app(request):
    if request.method == "POST" and request.user.is_authenticated() and request.user.username == "pisb_credenz":                     #complete
        print ("Hello1")
        #try:
        doc = opendoc('userdata.ods')
        index = 1
        for sheet in doc.sheets:
            for i in range(978):                          ###############Number of rows in .ods file      read the complete function
                random_password = random_password_generate()
                registration_id = sheet['A'+str(index)].value
                excel_count = ExcelData.objects.get(id = 1)
                excel_count.user_id = excel_count.user_id+1
                excel_count.save()
                username = excel_count.user_id
                try:
                    registration_id = int(registration_id)
                except:
                    print registration_id
                print sheet['A'+str(index)].value
                print "suhavan1"
                if sheet['B' + str(index)].value=="C" :     ###############################################Consider while integrating
                    event_flag = 1
                else :
                    event_flag = 0
                print i
                print registration_id
                print event_flag
                temp = User.objects.create_user(username = username,password = random_password)
                temp_slot = Slot.objects.get(pk = 1)
                temp_user = UserData.objects.create(registration_id = registration_id,event_flag = event_flag,password = random_password,user = temp,slot = temp_slot)
                try:
                    temp_user.mobile_no1 = int(sheet['D'+str(index)].value)
                except:
                    print "no mobile number"
                try:
                    temp_user.mobile_no2 = int(sheet['G'+str(index)].value)
                except:
                    print "no mobile number"
                try:
                    temp_user.email1 = sheet['E'+str(index)].value
                except:
                    print "no email1 id"
                try:
                    temp_user.email2 = sheet['H'+str(index)].value
                except:
                    print "no email2 id"
                try:
                    temp_user.name1 = sheet['C'+str(index)].value
                except:
                    print "no name1"
                try:
                    temp_user.name2 = sheet['F'+str(index)].value
                except:
                    print "no name2"
                temp_user.save()
                index = index+1
                print i
                print index
        return render(request,'Adminpage.html',{'message':'Data stored in the database and random passwords have been assigned'})
        #except:
        #    return render(request,'Adminpage.html',{'message':'There is no file'})
    else:
        return render(request,'Adminlogin.html',{'message':'Authentication failed'})

@csrf_exempt
def add_manually_func(request): #complete
    if request.method == "POST" and request.user.username == "pisb_credenz"  and request.user.is_authenticated() :
        return render(request,'Manualentry.html')
    else:
        return render(request,'Adminlogin.html',{'message':'Authentication failed'})

def add_data_manually(request):         #complete
    if request.method == "POST" and request.user.username == "pisb_credenz"  and request.user.is_authenticated() :
        if request.POST['event_flag'] == '1':
            event = 1
        else:
            event = 0
        excel_count = ExcelData.objects.get(id = 1)
        excel_count.user_id = excel_count.user_id+1
        excel_count.save()
        username = excel_count.user_id
        #username=request.POST['username']
        random_password=random_password_generate()
        temp_slot = Slot.objects.get(id = 1)
        temp=User.objects.create_user(username=username,password=random_password)
        UserData.objects.create(registration_id = request.POST['registration_id'],name1 = str(request.POST['name1']),name2 = str(request.POST['name2']),email1 = str(request.POST['email1']),email2 = str(request.POST['email2']),mobile_no1=str(request.POST['mobile_no1']),mobile_no2=str(request.POST['mobile_no2']),event_flag = event,password = random_password, user=temp,slot = temp_slot)
        return render(request,'Manualentry.html',{'message':'The entry is stored successfully'})
    else:
        return render(request,'Adminlogin.html',{'message':'Authentication failed'})

@csrf_exempt
def slot_add(request):
    if request.method == "POST" and request.user.username == "pisb_credenz"  and request.user.is_authenticated() :
        return render(request,'Slotpage.html')
    else :
        return render(request,'Adminlogin.html',{'message':'Authentication failed'})

def show_slot(request):
    if request.method == "POST" and request.user.username == "pisb_credenz" and request.user.is_authenticated() :
        slot_clash = Slot.objects.filter(event_flag = 1)
        slot_rc = Slot.objects.filter(event_flag = 0)

        json_cdata = serializers.serialize("json", Slot.objects.filter(event_flag = 1))
        json_rdata = serializers.serialize("json", Slot.objects.filter(event_flag = 0))

        return render(request,'Slotshow.html',{'dataclash':json_cdata,'datarc':json_rdata})
    else:
        return render(request,'Adminlogin.html',{'message':'Authentication failed'})


def show_user(request):
    if request.method == "POST" and request.user.username == "pisb_credenz" and request.user.is_authenticated() :
        if User.objects.filter(username = request.POST['username']).exists() :
            user = User.objects.get(username = request.POST['username'])
            return render(request,'Usershow.html',{'user':user})
        else:
            return render(request,'Adminpage.html',{'message':'Invalid Username'})
    else:
        return render(request,'Adminlogin.html',{'message':'Authentication failed'})

@csrf_exempt
def add_slot_func(request):             #complete
    if request.method == "POST" and request.user.username == "pisb_credenz"  and request.user.is_authenticated() :
        if request.POST['event_flag'] == '1':
            event = 1
        else:
            event = 0
        Slot.objects.create(room_no = str(request.POST['room_no']),total_comp = (request.POST['total_comp']),comp_avail = (request.POST['total_comp']),date_slot = (request.POST['date_slot']),time_slot=(request.POST['time_slot']),event_flag=event)
        return render(request,'Slotpage.html',{'message':'The entry is stored successfully'})
    else:
        return render(request,'Adminlogin.html',{'message':'Authentication failed'})


@csrf_exempt
def email_send(request):            #complete
    if request.method == "POST" and request.user.username == "pisb_credenz"  and request.user.is_authenticated() :
        participants = UserData.objects.filter(send_mail = 0)
        for u in participants:
            if u.event_flag == 0 :
                event = "Reverse Coding"
            else:
                event = "Clash"
            body = "Dear Participant,\n\nGreetings from the team PISB!\nYou have participated in Credenz'16 in event " + str(event) +". Slot booking for the same has started at url:  http://pisbcredenz.pythonanywhere.com. \nIt is compulsary to book your slot to participate in the event.\n\tYour login credentials are:\n\t\tUsername         : "+str(u.user.username)+"\n\t\tPassword         : "+str(u.password)+"\n\t\tMobile No.        : Mobile number given while registration.\n\t\tRegistration No.  : Registration number is same as receipt number. \n\n\tInsructions:\n\t\t1)If in case you didn't get receipt number then your receipt number will be 9999.\n\t\t2) Mobile number of any one of the team member is valid which is submitted while registration.\n\t\t3) Only one slot will be booked for individual or team participation.\n\t\t4) Slots are available for round 1 only on 9th and 10th of September.\n\t\t5) Slots are scheduled for 30 minutes each.\n\t\t6) Once the slot is booked, it cannot be cancelled or changed.\n\t\t7) In case of any problem contact us with the details provided on the website.\nReguards,\nPICT IEEE Student Branch"
            subject="Slot booking for "+str(event)+"CREDENZ'16"
            email_list = []
            if u.email1 != None:
                email_list.append(u.email1)
            if u.email2 != None:
                email_list.append(u.email2)
            email = EmailMessage(subject, body,to=email_list)
            if email_list == [] :
                print "No email id"
            else:
                try:
                    print email_list
                    email.send()
                    print u.name1
                    u.send_mail = 1
                    u.save()
                except:
                   return render(request,"Adminpage.html",{'message':'No internet try agin'})
        return render(request,"Adminpage.html",{'message':'All mails are successfully sent'})
    else :
        return render(request,'Adminlogin.html',{'mesage':'Authentication failed'})

@csrf_exempt
def confirm_slot_book(request):
    if request.method == "POST" :
        date_slot = request.POST['date_slot']
        time_slot = request.POST['time_slot']
        print time_slot
        print date_slot
        participant = UserData.objects.get(user = request.user)
        s = Slot.objects.filter(event_flag = participant.event_flag,date_slot = date_slot,time_slot = time_slot)
        if s != None :
            slot_array = Slot.objects.filter(event_flag = participant.event_flag,date_slot = date_slot,time_slot = time_slot)
            for slot_data in slot_array:
                if slot_data.comp_avail > 0:
                    slot_data.comp_avail = slot_data.comp_avail-1
                    date = slot_data.date_slot
                    participant.slot = slot_data
                    participant.slot_booked = 1
                    if participant.event_flag == 1:
                        event = "Clash"
                    else:
                        event  = "Reverse Coding"
                    body = "Dear Participant,\n\nGreetings from the team "+str(event)+" ,CREDENZ'16!\nYour slot has been successfully booked. Details of slot are as follows\n\tTime  : "+str(return_time(slot_data.time_slot))+"\n\tDate  : "+str(date) +"th September, 2016\n\tVenue : PICT, Dhankawadi, Pune\n\tUsername : "+str(participant.user.username)+"\nInstructions:\n\t1) Icard for your respective college is necessary.\n\t2) Further details will be provided at venue.\n\t3) Report on venue 20 minutes before scheduled time along with the printout of this mail.\n\t4) Slot cannot be cancelled or booked again.\n\t5) Keep checking are website www.credenz.info to stay updated.\nReguards,\nPICT IEEE Student Branch"
                    #body = "Dear Participant,\n\n\t\tGreeting from team"+str(event)+" ,CREDENZ'16!\n\t\tYour slot has been successfully booked. Details of slot are as follows\n\t\tTime  : "+str(return_time(slot_data.time_slot))+"\n\t\tDate  : "+str(date)+" September, 2016\n\t\tVenue : PICT, Dhankawadi, Pune\n\t\tUsername : "+str(participant.user.username)+"\n\t\tInstructions:\n\t\t1) Icard for your respective college is necessary.\n\t\t2) Further details will be provided at venue.\n\t\t3) Report on venue 20 minutes before scheduled time.\n\t\t4) Slot cannot be cancelled or booked again.\n\t\t5) Keep checking are website www.credenz.info to stay updated."
                    subject="Confirmation mail for slot booking for the event "+str(event)+"CREDENZ'16"
                    email_list = []
                    if participant.email1 != None:
                        email_list.append(participant.email1)
                    if participant.email2 != None:
                        email_list.append(participant.email2)
                    #email_list.append(participant.email1)
                    #email_list.append(participant.email2)
                    email = EmailMessage(subject, body,to=email_list)
                    try:
                        email.send()
                        participant.save()
                        slot_data.save()
                        detail_slot = slot_data #maybe detail_slot is a local variable
                        logout(request)
                        return render(request,'Confirmationpage.html',{'slot':detail_slot})
                    except:
                        logout(request)
                        return render(request,'Login.html',{'message':'Connection time out  Try again after some time'})
            else:
                participant = UserData.objects.get(user = request.user)
                slot_matrix = [[0 for x in range(20)] for y in range(2)]
                for i in range(2):      #Discuss the format of time
                    for j in range(20):
                        slot_matrix[i][j] = Slot.objects.filter(event_flag = participant.event_flag,date_slot = i+9,time_slot = j+1).aggregate(Sum('comp_avail'))
                        slot_matrix[i][j] = slot_matrix[i][j]['comp_avail__sum']
                        if slot_matrix[i][j] == None:
                            slot_matrix[i][j] = 0
                return render(request,'Userslot.html',{'message':'Sorry...! all seats are booked in that slot','slot9':slot_matrix[0],'slot10':slot_matrix[1],'event_name':event_name})
        #return render(request,'slot.html',{'slot':slot_matrix,'message':'Sorry... You are late they are no seats remaining'})#just for testing
    else:
        return render(request,'Login.html',{'message':'Authentication Error'})


@csrf_exempt
def modify_data(request):           #not complete
    if request.method == "POST" and request.user.username == "pisb_credenz"  and request.user.is_authenticated() :
        userid = request.POST['username']
        temp_user = User.objects.get(username = userid)
        modify_user = UserData.objects.get(user = temp_user)
        modify_user.mobile_no1 = request.POST['mobile_no1']
        modify_user.mobile_no2 = request.POST['mobile_no2']
        modify_user.email1 = request.POST['email1']
        modify_user.email2 = request.POST['email2']
        modify_user.save()
        return render(request,'Adminpage.html',{'message':'User data modified successfully'})
    else:
        return render(request,'Adminlogin.html',{'mesage':'Authentication failed'})


@csrf_exempt
def receipt_name(request):
    if request.method == "POST" and request.user.username == "pisb_credenz"  and request.user.is_authenticated() :
        registration_id = request.POST['registration_id']
        if UserData.objects.filter(registration_id = registration_id).exists() :
            q = UserData.objects.filter(registration_id = registration_id)
            return render(request,'Receiptinfo.html',{'user':q})
        else:
            return render(request,'Adminpage.html',{'message':'Invalid Registration Number'})
    else:
        return render(request,'Adminlogin.html',{'mesage':'Authentication failed'})

@csrf_exempt
def call_user(request):
    if request.method == "POST" and request.user.username == "pisb_credenz"  and request.user.is_authenticated() :
        q = UserData.objects.filter(slot_booked = 0)
        return render(request,'Callinfo.html',{'user':q})
    else:
        return render(request,'Adminlogin.html',{'mesage':'Authentication failed'})


@csrf_exempt
def log_out(request):
    if request.method == "POST" :
        if request.user.username == "pisb_credenz" :
            logout(request)
            return render(request,'Adminlogin.html')
        else:
            logout(request)
            return render(request,'Login.html')
    else:
        logout(request)
        return render(request,'Login.html')


