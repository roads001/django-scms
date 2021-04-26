from django.db import models
from users.models import CustomUser, Teacher, Accountant


# Create your models here.
class AttendanceStatus(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text='"Present" will not be saved but may show as a teacher option.')
    code = models.CharField(max_length=10, unique=True, help_text="Short code used on attendance reports. Ex: A might be the code for the name Absent")
    excused = models.BooleanField(default=False, )
    absent = models.BooleanField(default=False, help_text="Some statistics need to add various types of absent statuses, such as the number in parentheses in daily attendance.")
    tardy = models.BooleanField(default=False, help_text="Some statistics need to add various types of tardy statuses, such as the number in parentheses in daily attendance.")
    half = models.BooleanField(default=False, help_text="Half attendance when counting. DO NOT check off absent otherwise it will double count!")
    
    class Meta:
        verbose_name_plural = 'Attendance Statuses'
    
    def __str__(self):
        return self.name


class TeachersAttendance(models.Model):
    date = models.DateField(auto_now_add=False)
    teacher = models.ForeignKey(Teacher, blank=True, on_delete=models.CASCADE)
    time_in = models.TimeField(auto_now_add=False, blank=True)
    time_out = models.TimeField(auto_now_add=False, blank=True)
    status = models.ForeignKey(AttendanceStatus, blank=True, null=True, on_delete=models.CASCADE)
    notes = models.CharField(max_length=500, blank=True)

    class Meta:
        unique_together = (("teacher", "date", "status"),)
        ordering = ('-date', 'teacher')

    def __str__(self):
        return f"{self.teacher.first_name} - {self.date} {self.status} "

    @property
    def edit(self):
        return "Edit"
    
    def save(self, *args, **kwargs):
        """Don't save Present """
        present, created = AttendanceStatus.objects.get_or_create(name="Present")
        if self.status != present:
            super(TeachersAttendance, self).save(*args, **kwargs)
        else:
            try: self.delete()
            except: pass

class StudentAttendance(models.Model):
    """
    This is daily students attendance 
    """
    student = models.ForeignKey(Student, blank=True, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False, blank=True)
    ClassSection = models.ForeignKey('administration.ClassSection', on_delete=models.CASCADE, blank=True, null=True)
    status = models.ForeignKey(AttendanceStatus, blank=True, null=True, on_delete=models.CASCADE)
    notes = models.CharField(max_length=500, blank=True)

    class Meta:
        unique_together = (("student", "date", "status"),)
        ordering = ('-date', 'student')

    def __str__(self):
        return f"{self.student.fname} - {self.date} {self.status} "

    @property
    def edit(self):
        return "Edit"
    
    def save(self, *args, **kwargs):
        """Don't save Present """
        present, created = AttendanceStatus.objects.get_or_create(name="Present")
        if self.status != present:
            super(StudentAttendance, self).save(*args, **kwargs)
        else:
            try: self.delete()
            except: pass