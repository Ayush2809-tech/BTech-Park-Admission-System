from django.shortcuts import render,redirect
from .models import*
from datetime import datetime
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

import uuid
import hashlib
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control

# Create your views here.

# 
def home(request):
    return render(request,'login/home.html')

def course(request):
    return render(request,'login/courses.html')

def contact(request):
    return render(request,'login/contact.html')

def about(request):
    return render(request,'login/about.html')

def base(request):
    return render(request,'login/base.html')

def mainlogin(request):
    return render(request,'login/login.html')

def adminlogin1(request):
    return render(request,'login/adminlogin1.html')

def studentlogin(request):
    if request.method=="POST":
        emailaddress=request.POST.get('emailaddress')
        password=request.POST.get('password')
        user= tbll_student.objects.filter(emailaddress=emailaddress,password=password)
        if user:
            request.session['studentid']=emailaddress
            return redirect('studentdash')
        else:
            return redirect('studentlogin')
    return render(request, "login/studentlogin.html")

def loginsave(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=login.objects.filter(username=username,password=password).first()
        if user:
            if user.status=="Active":
                request.session['adminid']=username
                return redirect('dashboard')
            else:
                return redirect('adminlogin1')
        messages.error(request, "Invalid Username or Password")
        return redirect('adminlogin1')
    return redirect('adminlogin1')

            


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    if 'adminid' not in request.session:
        return redirect('adminlogin1')

    total_sessions = session.objects.count()
    total_courses = tbl_course.objects.count()
    total_students = tbll_student.objects.count()

    pending_verification = tbll_student.objects.filter(
        application_status="DV"
    ).count()

    verified_students = tbll_student.objects.filter(
        application_status="Verified"
    ).count()

    enrolled_students = tbll_student.objects.filter(
        fees_status="Paid"
    ).count()

    recent_students = tbll_student.objects.order_by("-sid")[:10]

    context = {
        "total_sessions": total_sessions,
        "total_courses": total_courses,
        "total_students": total_students,
        "pending_verification": pending_verification,
        "verified_students": verified_students,
        "enrolled_students": enrolled_students,
        "recent_students": recent_students,
    }

    return render(request, "admin/dashboard.html", context)


# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admindash(request): 
     return render(request,'admin/adminlayout.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addsession(request): 
    if 'adminid' not in request.session:
        return redirect('adminlogin1')
    if request.method == "POST":
        session_name=request.POST.get('session_name')
        create_at=datetime.now()
        sv=session.objects.filter(session_name=session_name).first()
        if sv is not None:
            messages.success(request,"This session Already Exists !!")
        else:
            ab=session(session_name=session_name,create_at=create_at)
            ab.save()
            messages.success(request,"Session Added Successfully !!")
        return redirect('addsession')
    return render(request,'admin/addsession.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addcourse(request):
    if 'adminid' not in request.session:
        return redirect('adminlogin1')
    else:
        if request.method == "POST":
            tbl_course.objects.create(
                session_name=request.POST.get('session_name'),
                course_name=request.POST.get('course_name'),
                duration=request.POST.get('duration'),
                fees=request.POST.get('fees'),
                create_at=datetime.now()
            )
            messages.success(request, "Course added successfully !!")
            return redirect('addcourse')
    
        ab = session.objects.all()
        return render(request, 'admin/addcourse.html', {'ab': ab})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def showcourse(request):
    if 'adminid' not in request.session:
        return redirect('adminlogin1')
    ab = tbl_course.objects.all()
    return render(request, 'admin/showcourse.html', {'ab': ab})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletecourse(request, id):
    if 'adminid' not in request.session:
        return redirect('adminlogin1')
    course = tbl_course.objects.get(id=id)
    course.delete()
    messages.success(request, "Course deleted successfully!")
    return redirect('showcourse')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update_course(request, id):
    if 'adminid' not in request.session:
        return redirect('adminlogin1')
    course = tbl_course.objects.get(id=id)
    if request.method == "POST":
        course.session_name = request.POST['session_name']
        course.course_name = request.POST['course_name']
        course.duration = request.POST['duration']
        course.fees = request.POST['fees']
        course.save()
        messages.success(request, "Course updated successfully!")
        return redirect('showcourse')
    return render(request, 'admin/showcourse.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def verified_student(request):
    if 'adminid' not in request.session:
        return redirect('adminlogin1')
    students = tbll_student.objects.filter(application_status="Verified")
    return render(request, 'admin/verified_student.html', {
        'students': students
    })

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def pending_student(request):
    if 'adminid' not in request.session:
        return redirect('adminlogin1')
    students = tbll_student.objects.filter(application_status="DV")
    return render(request, 'admin/pending_student.html', {
        'students': students
    })

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def enrolled_student(request):
    if 'adminid' not in request.session:
        return redirect('adminlogin1')
    students = tbll_student.objects.filter(fees_status="Paid")

    return render(request, "admin/enrolled_student.html", {
        "students": students
    })

# show session ---------------------------------------------------------------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def showsession(request):
    if 'adminid' not in request.session:
        return redirect('adminlogin1')
    ab=session.objects.all()
    return render(request, 'admin/showsession.html',{'ab':ab})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deldata(request,id):
    if 'adminid' not in request.session:
        return redirect('adminlogin1')
    ab=session.objects.get(id=id)
    ab.delete()
    messages.success(request, "Session deleted successfully.")
    return redirect('showsession')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit(request,id):
    if 'adminid' not in request.session:
        return redirect('adminlogin1')    
    ab=session.objects.get(id=id)
    return render(request,'admin/showsession.html',{'ab':ab})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update_session(request, id):
    if 'adminid' not in request.session:
        return redirect('adminlogin1')
    obj = session.objects.get(id=id)

    if request.method == "POST":
        obj.session_name = request.POST.get("session_name")
        obj.save()
        messages.success(request, "Session updated successfully.")
        return redirect("showsession")

# show session ---------------------------------------------------------------------------------------------

# show student----------------------------------------------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def showstudent(request):
    if 'adminid' not in request.session:
        return redirect('adminlogin1')
    ab = tbll_student.objects.all()
    return render(request, 'admin/showstudent.html', {'ab': ab})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletestudent(request, sid):
    if 'adminid' not in request.session:
        return redirect('adminlogin1')
    student = tbll_student.objects.get(sid=sid)
    student.delete()
    messages.success(request, "Student deleted successfully !!")
    return redirect('showstudent')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def updatestudent(request, sid):
    if 'adminid' not in request.session:
        return redirect('adminlogin1')
    student = tbll_student.objects.get(sid=sid)
    if request.method == "POST":
        student.name = request.POST.get('name')
        student.emailaddress = request.POST.get('emailaddress')
        student.contact_no = request.POST.get('contact_no')
        student.gender = request.POST.get('gender')
        student.dob = request.POST.get('dob')
        student.save()
        messages.success(request, "Student updated successfully !!")
        return redirect('showstudent')
    return redirect('showstudent')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def verify_student(request, sid):
    if 'adminid' not in request.session:
        return redirect('adminlogin1')
    student = tbll_student.objects.get(sid=sid)
    student.application_status = "Verified"
    student.save()
    message = f"""
Dear {student.name},

Congratulations!🎉🎉

Your documents have been verified successfully by the Admission Team.

You are now eligible to pay your admission fee.

Login to your account and complete the payment process.

Course : {student.course}
Session : {student.session}

Regards,
Biotech Park Admission Team
"""

    send_mail(
    "Documents Verified Successfully",
    message,
    settings.EMAIL_HOST_USER,
    [student.emailaddress],
    fail_silently=False,
    )
    messages.success(request, "Student verified successfully.")
    return redirect("showstudent")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reject_student(request, sid):
    if 'adminid' not in request.session:
        return redirect('adminlogin1')
    student = tbll_student.objects.get(sid=sid)
    student.application_status = "Rejected"
    student.save()
    message = f"""
Dear {student.name},

Your admission application has been reviewed.

Unfortunately, your documents could not be verified.😔😔

Please contact📞 the Admission Office or upload the correct documents if allowed.

Regards,
Biotech Park Admission Team
"""

    send_mail(
    "Admission Application Rejected",
    message,
    settings.EMAIL_HOST_USER,
    [student.emailaddress],
    fail_silently=False,
    )
    messages.success(request, "Student rejected.")
    return redirect("showstudent")



# show student----------------------------------------------------------------------------


# ---------------------------------admin logout---------------------------------------------
def logout(request):
    if 'adminid' in request.session:
        del request.session['adminid']
    return redirect('adminlogin1')
# ---------------------------------admin logout---------------------------------------------

# ---------------------------------student logout---------------------------------------------
def studentlogout(request):
    request.session.flush()
    return redirect('studentlogin')
# ---------------------------------student logout---------------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addstudent(request):
    if 'adminid' not in request.session:
        return redirect('adminlogin1')
    if request.method == "POST":
        tbll_student.objects.create(
            name=request.POST.get('name'),
            emailaddress=request.POST.get('emailaddress'),
            password=request.POST.get('password'),
            contact_no=request.POST.get('contact_no'),
            gender=request.POST.get('gender'),
            dob=request.POST.get('dob'),
        )
        name=request.POST.get('name')
        emailaddress=request.POST.get('emailaddress')
        password=request.POST.get('password')
        message = f"""
        Dear {name},

        🎉 Congratulations!

        Your registration has been completed successfully on the Biotech Park Admission Portal.

        You can now log in using the credentials below:

        ---------------------------------------
        User ID / Email : {emailaddress}
        Password        : {password}
        ---------------------------------------

        Next Steps:
        1. Login to the Admission Portal.
        2. Complete your Basic Information.
        3. Upload all required documents.
        4. Wait for document verification by the Admin.
        5. After verification, pay your admission fee.
        6. Once the payment is successful, your course will be allotted.
        
        Please keep this email safe for future login and admission-related communication.
        
        If you have any questions or need assistance, please contact the Admission Office.
        
        Regards,
        
        Biotech Park Admission Team
        """

        send_mail(
            "Registration Successful",
            message,
            settings.EMAIL_HOST_USER,
            [emailaddress],
            fail_silently=False
        )

    return render(request,'admin/addstudent.html')


# ===============================================Student Zone=================================================



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def studentdash(request):
    sid = request.session.get("studentid")

    if not sid:
        return redirect("studentlogin")

    student = tbll_student.objects.filter(emailaddress=sid).first()

    context = {
        "student": student
    }

    return render(request, "student/studentdash.html", context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def apply1(request):
    sid = request.session.get("studentid")

    if not sid:
        return redirect("studentlogin")
    data = tbll_student.objects.filter(emailaddress=sid).first()
    ab = tbl_course.objects.all()
    ad = session.objects.all()
   
   
    if request.method=="POST":
        # DATA GET
        f_name=request.POST.get('f_name')
        m_name=request.POST.get('m_name')
        address=request.POST.get('address')
        aadhar_no=request.POST.get('aadhar_no')
        Session=request.POST.get('session')
        course=request.POST.get('course')
        course_id = request.POST.get("course")

        cr = tbl_course.objects.get(id=course_id)

        data.f_name = f_name
        data.m_name = m_name
        data.address = address
        data.aadhar_no = aadhar_no

        # Automatically save from tbl_course
        data.course = cr.course_name
        data.session = cr.session_name
        data.course_duration = cr.duration
        data.fees = cr.fees

        data.save()

        messages.success(request, "Basic information saved successfully.")
        return redirect('apply2')


    context = {
        "data": data,
        "ab": ab
    }

    return render(request, "student/apply1.html", context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def apply3(request):
    sid = request.session.get("studentid")
    if not sid:
        return redirect("studentlogin")
    student = tbll_student.objects.filter(emailaddress=sid).first()
    return render(request, "student/apply3.html", {
        "student": student
    })

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def apply4(request):
    sid=request.session.get("studentid")
    if not sid:
        return redirect("studentlogin")
        
    data = tbll_student.objects.filter(emailaddress=sid).first()
    ab = tbl_course.objects.all()
    ad = session.objects.all()
    return render(request, "student/apply4.html")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def fees(request):
    sid=request.session.get("studentid")
    if not sid:
        return redirect("studentlogin")
    return render(request, "student/fees.html")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def enrolledstudent(request):
    return render(request, "student/enrolledstudent.html")


    # student = tbll_student.objects.filter(emailaddress=sid).first()
    # return render(request, "student/apply3.html", {
    #     "student": student
    # })


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def apply2(request):
    sid=request.session.get("studentid")
    if not sid:
        return redirect("studentlogin")
    data=tbll_student.objects.get(emailaddress=sid)
    student = tbll_student.objects.filter(emailaddress=sid).first()

    if request.method =="POST":
        hs_percentage=request.POST.get('hs_percentage')
        hs_marksheet=request.FILES.get('hs_marksheet')
        inter_percentage=request.POST.get('inter_percentage')
        inter_marksheet=request.FILES.get('inter_marksheet')
        aadhar_pic=request.FILES.get('aadhar_pic')
        profile_pic=request.FILES.get('profile_pic')
        sign=request.FILES.get('sign')

    #  set the data on model
        data.hs_percentage=hs_percentage
        data.hs_marksheet=hs_marksheet
        data.inter_percentage=inter_percentage
        data.inter_marksheet=inter_marksheet
        data.aadhar_pic=aadhar_pic
        data.profile_pic=profile_pic
        data.sign=sign
        data.application_status="DV"
        data.save()
        return redirect('apply3')
    
    return render(request, 'student/apply2.html', {
        "student": student
    })

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def review_student(request):
    if 'adminid' not in request.session:
        return redirect('adminlogin1')
    ab = tbll_student.objects.all()
    return render(request, 'admin/reviewstudent.html', {'ab': ab})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def details_review(request, emailaddress):
    if 'adminid' not in request.session:
        return redirect('adminlogin1')
    data = tbll_student.objects.get(emailaddress=emailaddress)
    return render(request, 'admin/details_review.html', {'data': data})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def verify(request,emailaddress):
    if 'adminid' not in request.session:
        return redirect('adminlogin1')
    data=tbll_student.objects.get(emailaddress=emailaddress)
    data.application_status="Verified"
    data.save()
    return redirect('review_student')


def get_login_student(request):
    sid = request.session.get('studentid')

    if sid:
        return tbll_student.objects.filter(emailaddress=sid).first()

    return None

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def student_fees_payment(request):

    student = get_login_student(request)

    if not student:
        return redirect('studentlogin')

    return render(request, 'student/student_fees_payment.html', {
        'student': student
    })


def payu_payment(request):

    student = get_login_student(request)

    if not student:
        return redirect("studentlogin")

    if student.application_status != "Verified":
        messages.error(request, "Your documents are not approved yet.")
        return redirect("student_fees_payment")

    if student.fees_status == "Paid":
        messages.success(request, "Fees already paid.")
        return redirect("student_enrolled_course")

    # Get Course Details
    course = tbl_course.objects.filter(course_name=student.course).first()

    if course:
        # amount = str(course.fees)
        # productinfo = course.course_name
        amount = "{:.2f}".format(float(course.fees))
        productinfo = "Admission Fee"

        # Student table me bhi update kar do
        student.fees = course.fees
        student.save()

    else:
        # Dummy values for testing
        amount = "1.00"
        productinfo = "Admission Fee"

    key = settings.PAYU_KEY
    salt = settings.PAYU_SALT
    payu_url = settings.PAYU_URL

    txnid = "TXN" + uuid.uuid4().hex[:10].upper()

    firstname = student.name
    email = student.emailaddress
    phone = str(student.contact_no)

    surl = request.build_absolute_uri("/payment_success/")
    furl = request.build_absolute_uri("/payment_failure/")

    hash_string = (
        f"{key}|{txnid}|{amount}|{productinfo}|{firstname}|{email}|||||||||||{salt}"
    )
    # print(repr(hash_string))

    hashh = hashlib.sha512(hash_string.encode()).hexdigest().lower()


    student.payment_id = txnid
    student.fees_status = "Pending"
    student.save()

    context = {
        "payu_url": payu_url,
        "key": key,
        "txnid": txnid,
        "amount": amount,
        "productinfo": productinfo,
        "firstname": firstname,
        "email": email,
        "phone": phone,
        "surl": surl,
        "furl": furl,
        "hash": hashh,
    }
    # print(context)
    return render(request, "student/payu_redirect.html", context)

@csrf_exempt
def payment_success(request):

    txnid = request.POST.get("txnid")
    mihpayid = request.POST.get("mihpayid")
    status = request.POST.get("status")

    student = tbll_student.objects.filter(payment_id=txnid).first()

    if not student:
        return redirect("studentlogin")

    if status == "success":

        student.fees_status = "Paid"
        student.payment_date = datetime.now()

        if mihpayid:
            student.payment_id = mihpayid

        student.save()
        message = f"""
Dear {student.name},

🎉 Congratulations!

Your admission fee has been received successfully and your admission has been confirmed.

==========================================================
            ADMISSION CONFIRMATION DETAILS
==========================================================

Student ID          : {student.sid}
Student Name        : {student.name}
Father's Name       : {student.f_name}
Mother's Name       : {student.m_name}
Email               : {student.emailaddress}
Mobile Number       : {student.contact_no}
Gender              : {student.gender}
Date of Birth       : {student.dob}
Address             : {student.address}
Aadhar Number       : {student.aadhar_no}

----------------------------------------------------------

Session             : {student.session}
Course              : {student.course}
Course Duration     : {student.course_duration}
Course Fee          : ₹{student.fees}

----------------------------------------------------------

Application Status  : {student.application_status}
Fee Status          : {student.fees_status}
Payment ID          : {student.payment_id}
Payment Date        : {student.payment_date}

==========================================================

Your admission has been successfully completed.

Please keep this email safely for future reference.

Regards,

Biotech Park Admission Team
"""

        send_mail(
        subject="Admission Confirmed - Payment Successful",
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[student.emailaddress],
        fail_silently=False,
        )
        messages.success(request, "Payment Successful.")

        return redirect("student_enrolled_course")

    student.fees_status = "Failed"
    student.save()

    messages.error(request, "Payment Failed.")

    return redirect("student_fees_payment")


@csrf_exempt
def payment_failure(request):

    txnid = request.POST.get("txnid")

    student = tbll_student.objects.filter(payment_id=txnid).first()

    if student:
        student.fees_status = "Failed"
        student.save()

    messages.error(request, "Payment Failed.")

    return redirect("student_fees_payment")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def student_enrolled_course(request):

    student = get_login_student(request)

    if not student:
        return redirect("studentlogin")

      # Fees check
    if student.fees_status != "Paid":
        messages.error(request, "Please pay your course fees first.")
        return redirect("student_fees_payment")

    return render(request, "student/student_enrolled_course.html", {
        "student": student
    })


