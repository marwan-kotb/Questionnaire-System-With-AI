from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    is_organisation = models.BooleanField(default=False)
    username = models.CharField(max_length=30, unique=False)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        unique_together = None

    def __str__(self):
        return self.username


class Organisation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class Semester(models.Model):
    year = models.CharField(max_length=9, help_text="Format: yyyy/yyyy")
    semester = models.PositiveSmallIntegerField()
    organisation = models.ForeignKey(Organisation, on_delete=models.RESTRICT, null=True)

    class Meta:
        unique_together = (
            "year",
            "semester",
        )
        ordering = ["year", "semester"]

    def __str__(self):
        return f"{self.year} Semester {self.semester}"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    student_no = models.CharField(max_length=64, unique=True)
    level = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)], null=True
    )
    organisation = models.ForeignKey(Organisation, on_delete=models.RESTRICT, null=True)

    def __str__(self):
        return self.user.username


class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.RESTRICT, null=True)
    is_teaching_assistant = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Course(models.Model):
    CourseName = models.CharField(blank=True, max_length=64)
    CourseCode = models.CharField(blank=True, max_length=64)
    StudentID = models.ManyToManyField(Student, related_name="Student")
    Objectives = models.TextField(blank=True)
    Aims = models.TextField(blank=True)
    Outcomes = models.TextField(blank=True)
    CreditHours = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)], null=True
    )
    flagSec = models.BooleanField(default=False)
    flagLab = models.BooleanField(default=False)
    SemID = models.ManyToManyField(Semester, related_name="Sem")

    def __str__(self):
        return self.CourseName + " " + self.SemID.all().first().__str__()


class Lecture(models.Model):
    instructor_id = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True)
    course = models.OneToOneField(Course, on_delete=models.CASCADE, null=True)
    SemesterId = models.ForeignKey(Semester, on_delete=models.CASCADE)


class Lab(models.Model):
    instructor_id = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True)
    course = models.OneToOneField(Course, on_delete=models.CASCADE, null=True)
    SemesterId = models.ForeignKey(Semester, on_delete=models.CASCADE)


class Section(models.Model):
    instructor_id = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True)
    course = models.OneToOneField(Course, on_delete=models.CASCADE, null=True)
    SemesterId = models.ForeignKey(Semester, on_delete=models.CASCADE)


class Feedback(models.Model):
    stud_id = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    LecFeedback = models.ForeignKey(Lecture, on_delete=models.RESTRICT, null=True)
    LabFeedback = models.ForeignKey(Lab, on_delete=models.RESTRICT, null=True)
    SecFeedback = models.ForeignKey(Section, on_delete=models.RESTRICT, null=True)
    TextLec = models.TextField(blank=True)
    TextLab = models.TextField(blank=True)
    TextSec = models.TextField(blank=True)
    TextLectuerer = models.TextField(blank=True)


class Selectes(models.Model):
    stud_id = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    LecSelect = models.ForeignKey(Lecture, on_delete=models.RESTRICT, null=True)
    LabSelect = models.ForeignKey(Lab, on_delete=models.RESTRICT, null=True)
    SecSelect = models.ForeignKey(Section, on_delete=models.RESTRICT, null=True)
    question1 = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True
    )
    question2 = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True
    )
    question3 = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True
    )
    question4 = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True
    )
    question5 = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True
    )
    question6 = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True
    )
    question7 = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True
    )
    question8 = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True
    )
    question9 = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True
    )
    question10 = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True
    )
    question11 = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True
    )
    question12 = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True
    )
    question13 = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True
    )
    question14 = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True
    )
    question15 = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True
    )
    question16 = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True
    )
    question17 = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True
    )
    question18 = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True
    )
    question19 = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True
    )
    question20 = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True
    )
    question21 = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True
    )
    question22 = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True
    )
    question23 = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True
    )
    question24 = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True
    )
    question25 = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True
    )
    question26 = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True
    )
    question27 = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True
    )
    question28 = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True
    )


class Result(models.Model):
    LecResult = models.ForeignKey(Lecture, on_delete=models.RESTRICT)
    LabResult = models.ForeignKey(Lab, on_delete=models.RESTRICT, null=True)
    SecResult = models.ForeignKey(Section, on_delete=models.RESTRICT, null=True)
    LectuererResult = models.ForeignKey(Instructor, on_delete=models.RESTRICT)
    # Summary = models.TextField(blank=True)
    ScoreLec = models.IntegerField(null=True)
    ScoreLab = models.IntegerField(null=True)
    ScoreSec = models.IntegerField(null=True)
    ScoreLectuerer = models.IntegerField(null=True)
