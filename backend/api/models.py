from django.db import models

# Create your models here.
class Customer(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=30, unique=True)
    sex = models.BooleanField()
    birth_date = models.DateField()

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Teacher(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=30, unique=True)
    sex = models.BooleanField()
    birth_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Language(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    additional_info = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    customers = models.ManyToManyField(Customer, through='Payment')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    payment_date = models.DateField()
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES)
    grade = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        unique_together = ['customer', 'course', 'payment_date']

    def __str__(self):
        return f"{self.customer} - {self.course} ({self.payment_date})"


class TeacherLanguage(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.teacher} - {self.language}"
