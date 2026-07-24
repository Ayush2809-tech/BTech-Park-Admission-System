from django.db import models

# Create your models here.
class login(models.Model):
    id=models.IntegerField(primary_key=True,auto_created=True)
    username=models.CharField(max_length=225)
    password=models.CharField(max_length=16)
    status=models.CharField(max_length=20)

    def __str__(self):
        return self.username
    


class session(models.Model):
    id=models.IntegerField(primary_key=True,auto_created=True)
    session_name=models.CharField(max_length=20,unique=True)
    create_at=models.TimeField()

    def __str__(self):
        return self.session_name
    

class tbl_course(models.Model):
    id=models.IntegerField(primary_key=True,auto_created=True)
    session_name=models.CharField(max_length=20,)
    course_name=models.CharField(max_length=200)
    duration=models.CharField(max_length=100)
    fees=models.IntegerField()
    create_at=models.TimeField()

    def __str__(self):
        return self.course_name
        
    

class tbll_student(models.Model):
    sid=models.IntegerField(primary_key=True,auto_created=True)
    name=models.CharField(max_length=225)
    emailaddress=models.EmailField(max_length=225)
    password=models.CharField(max_length=16)
    contact_no=models.IntegerField()
    gender=models.CharField(max_length=2)
    dob=models.CharField(max_length=15)
    f_name=models.CharField(max_length=225,null=True)
    m_name=models.CharField(max_length=225,null=True)
    address=models.CharField(max_length=500,null=True)
    aadhar_no=models.IntegerField(max_length=15,null=True)
    aadhar_pic=models.FileField(upload_to='student_documents',null=True)
    session=models.CharField(max_length=50,null=True)
    course=models.CharField(max_length=500,null=True)
    course_duration=models.CharField(max_length=50,null=True)
    hs_percentage=models.CharField(max_length=20)
    hs_marksheet=models.FileField(upload_to='student_documents',null=True)
    inter_percentage=models.CharField(max_length=20,null=True)
    inter_marksheet=models.FileField(upload_to='student_documents',null=True)
    profile_pic=models.FileField(upload_to='student_documents',null=True)
    sign=models.FileField(upload_to='student_documents',null=True)
    fees=models.IntegerField(null=True)
    fees_status=models.CharField(max_length=20,default="Unpaid")
    payment_id=models.CharField(max_length=100,null=True,blank=True)
    payment_date=models.DateTimeField(null=True,blank=True)
    application_status = models.CharField(max_length=20,default="Pending")


    def __str__(self):
        return self.name


class tbl_payment(models.Model):
    student_email = models.EmailField()
    student_name = models.CharField(max_length=225)
    course = models.CharField(max_length=200)
    txnid = models.CharField(max_length=100)
    payu_payment_id = models.CharField(max_length=100, null=True, blank=True)
    amount = models.IntegerField()
    payment_status = models.CharField(max_length=20)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_name