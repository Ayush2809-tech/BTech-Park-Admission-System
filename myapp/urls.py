from django.urls import path
from .views import*

urlpatterns=[
    path('',home,name='home'),
    path('base/',base, name='base'),
    path('course/',course, name='course'),
    path('contact/',contact, name='contact'),
    path('about/',about, name='about'),
    path('adminlogin1/',adminlogin1,name='adminlogin1'),
    path('studentlogin/',studentlogin, name='studentlogin'),
    path('mainlogin/',mainlogin, name='mainlogin'),
    path('loginsave/',loginsave, name='loginsave'),
    path('dashboard/',dashboard, name='dashboard'),
    path('admindash/',admindash, name='admindash'),
    path('addsession/',addsession, name='addsession'),
    path('showsession/',showsession, name='showsession'),
    path('addcourse/',addcourse, name='addcourse'),
    path('showcourse/',showcourse, name='showcourse'),
    path('deletecourse/<int:id>/', deletecourse, name='deletecourse'),
    # path('addstudent/',addstudent, name='addstudent'),
    path('showstudent/',showstudent, name='showstudent'),
    path('verified_student/',verified_student, name='verified_student'),
    path('pending_student/',pending_student, name='pending_student'),
    path('enrolled_student/',enrolled_student, name='enrolled_student'),
    path('edit/<int:id>/', edit, name='edit'),
    path('update_session/<int:id>/', update_session, name='update_session'),
    path('deldata/<int:id>/', deldata, name='deldata'),
    path('delete_student/<int:sid>/', deletestudent, name='deletestudent'),
    path('update_student/<int:sid>/', updatestudent, name='updatestudent'),

    path('update_course/<int:id>/', update_course, name='update_course'),
    # path('delete_course/<int:id>/', delete_course, name='delete_course'),

    path('logout',logout,name='logout'),
    path('studentlogout',studentlogout,name='studentlogout'),
    path('addstudent',addstudent,name='addstudent'),
    path('review_student',review_student,name='review_student'),
    path('details_review/<str:emailaddress>/', details_review, name='details_review'),
    path('verify/<str:emailaddress>/', verify, name='verify'),

    path('verify_student/<int:sid>/', verify_student, name='verify_student'),
    path('reject_student/<int:sid>/', reject_student, name='reject_student'),


    # ------------------student zone--------------------
    path('studentdash/',studentdash,name='studentdash'),
    path('apply1/',apply1,name='apply1'),
    path('apply2/',apply2,name='apply2'),
    path('apply3/',apply3,name='apply3'),
    path('apply4/',apply4,name='apply4'),
    path('fees/',fees,name='fees'),
    path('enrolledstudent/',enrolledstudent,name='enrolledstudent'),

    path('student_fees_payment/',student_fees_payment, name='student_fees_payment'),
    path('payu_payment/', payu_payment, name='payu_payment'),
    path('payment_success/', payment_success, name='payment_success'),
    path('payment_failure/',payment_failure, name='payment_failure'),
    path('student_enrolled_course/',student_enrolled_course, name='student_enrolled_course'),


]