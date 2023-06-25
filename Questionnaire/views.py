import json
from datetime import datetime

import arabic_reshaper
import core.gmail as gmail
import core.nlp_models as nlp_models
from bidi.algorithm import get_display
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.db.models import Count, Max
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from Questionnaire.models import *


def is_arabic(text):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    for char in bidi_text:
        if "a" <= char <= "z" or "A" <= char <= "Z":
            return False
    return True


def index(request):
    return render(request, "Questionnaire/index.html", {"user": request.user})


@csrf_exempt
def login_student(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(email=email, password=password)

        check = User.objects.filter(email=email, is_student=True).exists()

        # Check if authentication successful
        if user is not None and check:
            login(request, user)
            return redirect("courses")
        else:
            return render(
                request,
                "Questionnaire/StudentLogin.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "Questionnaire/StudentLogin.html")


@csrf_exempt
def login_admin(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(email=email, password=password)
        check = User.objects.filter(email=email, is_organisation=True).exists()

        if user is not None and check:
            login(request, user)
            return redirect("options")
        else:
            print("Invalid username and/or password.")
            return render(
                request,
                "Questionnaire/AdminLogin.html",
                {"message": "Invalid username and/or password."},
            )

    else:
        return render(request, "Questionnaire/AdminLogin.html")


def logout_view(request):
    logout(request)
    return render(request, "Questionnaire/index.html")


@csrf_exempt
def forgot_password(request, type):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is not None:
            # generate new password
            new_password = User.objects.make_random_password()
            print(new_password)
            user.set_password(new_password)
            user.save()

            subject = "Password Reset"
            body = f"New Password: {new_password}"
            to_email = [user.email]

            gmail.send_email(to_list=to_email, subject=subject, body=body)

            print(request.POST, type)
            if type == "s":
                return render(
                    request,
                    "Questionnaire/StudentLogin.html",
                    {"message": "New password has been sent to your email address."},
                )
            elif type == "a":
                return render(
                    request,
                    "Questionnaire/AdminLogin.html",
                    {"message": "New password has been sent to your email address."},
                )

        return render(
            request,
            "Questionnaire/forgot_password.html",
            {
                "message": "Email does not exist.",
                "type": type,
            },
        )

    else:
        return render(
            request,
            "Questionnaire/forgot_password.html",
            {
                "type": type,
            },
        )


@login_required
def courses(request):
    user = request.user
    try:
        courses = Course.objects.filter(StudentID=Student.objects.get(user=user))
    except:
        courses = None

    return render(
        request,
        "Questionnaire/courses.html",
        {"courses": courses, "student": Student.objects.get(user=user)},
    )


@login_required
def course(request, course_id):
    course = Course.objects.get(pk=course_id)
    return render(
        request,
        "Questionnaire/sub.html",
        {
            "course": course,
        },
    )


@login_required
@csrf_exempt
def questionnaire(request, course_id):
    user = request.user
    course = Course.objects.get(pk=course_id)

    student = Student.objects.get(user=user)

    if student not in course.StudentID.all():
        return render(
            request,
            "Questionnaire/error.html",
            {"message": "You are not enrolled in this course."},
        )

    try:
        lec = Lecture.objects.get(course=course)
    except:
        lec = None

    if course.flagLab:
        lab = Lab.objects.get(course=course)
    else:
        lab = None
    if course.flagSec:
        sec = Section.objects.get(course=course)
    else:
        sec = None

    if request.method == "POST":
        textlec = request.POST.getlist("lec")

        if course.flagLab:
            textlab = request.POST.getlist("lab")
            for i in range(len(textlab)):
                if textlab[0] != "" and textlab[1] != "":
                    textlab = textlab[i]
                    break

                if textlab[0] == "" and textlab[1] == "":
                    textlab = ""
                    break

                if textlab[i] != "":
                    textlab = textlab[i]
                    break
                if textlab[i] == "":
                    continue
        else:
            textlab = ""
        if course.flagSec:
            textsec = request.POST.getlist("sec")
            for i in range(len(textsec)):
                if textsec[0] != "" and textsec[1] != "":
                    textsec = textsec[i]
                    break

                if textsec[0] == "" and textsec[1] == "":
                    textsec = ""
                    break

                if textsec[i] != "":
                    textsec = textsec[i]
                    break
                if textsec[i] == "":
                    continue
        else:
            textsec = ""

        textlectuerer = request.POST.getlist("lectuerer")

        for i in range(len(textlec)):
            if textlec[0] != "" and textlec[1] != "":
                textlec = textlec[i]
                break

            if textlec[0] == "" and textlec[1] == "":
                textlec = ""
                break

            if textlec[i] != "":
                textlec = textlec[i]
                break
            if textlec[i] == "":
                continue

        for i in range(len(textlectuerer)):
            if textlectuerer[0] != "" and textlectuerer[1] != "":
                textlectuerer = textlectuerer[i]
                break

            if textlectuerer[0] == "" and textlectuerer[1] == "":
                textlectuerer = ""
                break

            if textlectuerer[i] != "":
                textlectuerer = textlectuerer[i]
                break
            if textlectuerer[i] == "":
                continue

        F = Feedback.objects.create(
            stud_id=student,
            LecFeedback=lec,
            LabFeedback=lab,
            SecFeedback=sec,
            TextLec=textlec,
            TextLab=textlab,
            TextSec=textsec,
            TextLectuerer=textlectuerer,
        )

        if is_arabic(textlec):
            scoreLec = nlp_models.score_arabic(textlec)
        else:
            scoreLec = nlp_models.score_english(textlec)

        if is_arabic(textlab):
            scoreLab = nlp_models.score_arabic(textlab)
        else:
            scoreLab = nlp_models.score_english(textlab)

        if is_arabic(textsec):
            scoreSec = nlp_models.score_arabic(textsec)
        else:
            scoreSec = nlp_models.score_english(textsec)

        if is_arabic(textlectuerer):
            scoreLectuerer = nlp_models.score_arabic(textlectuerer)
        else:
            scoreLectuerer = nlp_models.score_english(textlectuerer)

        R = Result.objects.create(
            LecResult=lec,
            LabResult=lab,
            SecResult=sec,
            LectuererResult=Instructor.objects.get(user_id=lec.instructor_id),
            ScoreLec=scoreLec,
            ScoreLab=scoreLab,
            ScoreSec=scoreSec,
            ScoreLectuerer=scoreLectuerer,
        )

        return redirect("selects", course_id=course_id)

    return render(
        request,
        "Questionnaire/write_opinion.html",
        {
            "course": course,
            "lec": lec,
            "lab": lab,
            "sec": sec,
            "semester": list(course.SemID.all())[-1],
            "student": Student.objects.get(user=user),
        },
    )


@login_required
@csrf_exempt
def selects(request, course_id):
    user = request.user
    course = Course.objects.get(pk=course_id)

    student = Student.objects.get(user=user)

    if student not in course.StudentID.all():
        return render(
            request,
            "Questionnaire/error.html",
            {"message": "You are not enrolled in this course."},
        )

    try:
        lec = Lecture.objects.get(course=course)
    except:
        lec = None

    if course.flagLab:
        lab = Lab.objects.get(course=course)
    else:
        lab = None
    if course.flagSec:
        sec = Section.objects.get(course=course)
    else:
        sec = None

    if request.method == "POST":
        s = Selectes.objects.create(
            stud_id=student, LecSelect=lec, LabSelect=lab, SecSelect=sec
        )

        for key, value in request.POST.items():
            if key != "csrfmiddlewaretoken":
                s.__dict__[key] = value
                s.save()
        return redirect("final")

    return render(
        request,
        "Questionnaire/selectes.html",
        {
            "course": course,
        },
    )


def final(request):
    return render(request, "Questionnaire/final.html")


@login_required
def options(request):
    if Course.objects.filter(id=1).exists():
        course = True
    else:
        course = False

    if Semester.objects.filter(id=1).exists():
        semester = True
    else:
        semester = False

    if (
        Instructor.objects.filter(is_teaching_assistant=False).exists()
        and Instructor.objects.filter(is_teaching_assistant=True).exists()
    ):
        instructor = True
    else:
        instructor = False

    if Result.objects.filter(id=1).exists():
        result = True
    else:
        result = False

    if Selectes.objects.filter(id=1).exists():
        selects = True
    else:
        selects = False

    return render(
        request,
        "Questionnaire/options.html",
        {
            "course": course,
            "semester": semester,
            "instructor": instructor,
            "result": result,
            "selects": selects,
        },
    )


@login_required
@csrf_exempt
def edit_student(request):
    faculty = Organisation.objects.get(user=User.objects.get(id=request.user.id))
    courses = Course.objects.all()
    send_to = []

    if request.method == "POST":
        data4 = request.POST.getlist("courses")

        student_data = zip(
            request.POST.getlist("student_no"),
            request.POST.getlist("student_name"),
            request.POST.getlist("student_email"),
            request.POST.getlist("student_level"),
        )
        print(request.POST)
        for data in student_data:
            print(data)
            new_password = User.objects.make_random_password()
            print(new_password)
            flag = False
            if not User.objects.filter(email=data[2]).exists():
                flag = True
                try:
                    user = User.objects.create_user(
                        username=data[1],
                        email=data[2],
                        password=new_password,
                        is_student=True,
                    )
                except:
                    return render(
                        request,
                        "Questionnaire/EditStudents.html",
                        {
                            "faculty": faculty,
                            "courses": courses,
                            "message": "Student already exists.",
                        },
                    )
                try:
                    s = Student.objects.create(
                        user=user,
                        student_no=data[0],
                        level=data[3],
                        organisation=faculty,
                    )
                except:
                    user.delete()
                    return render(
                        request,
                        "Questionnaire/EditStudents.html",
                        {
                            "faculty": faculty,
                            "courses": courses,
                            "message": "Student already exists.",
                        },
                    )
            else:
                flag = False
                if User.objects.filter(email=data[2], is_student=False).exists():
                    return render(
                        request,
                        "Questionnaire/EditStudents.html",
                        {
                            "faculty": faculty,
                            "courses": courses,
                            "message": "This email already exists as an instructor or admin.",
                        },
                    )
                s = Student.objects.get(user=User.objects.get(email=data[2]))

            for course_id in data4:
                course = Course.objects.get(pk=course_id)
                course.StudentID.add(s)
                course.save()

            send_to.append(data[2])

        if s:
            if flag:
                gmail.send_email(
                    to_list=send_to,
                    subject="Your New Password of Questionnaire System",
                    body=f"PASSWORD: {new_password}",
                )
            return render(
                request,
                "Questionnaire/EditStudents.html",
                {
                    "faculty": faculty,
                    "courses": courses,
                    "message": "Student added successfully.",
                },
            )
        else:
            return render(
                request,
                "Questionnaire/EditStudents.html",
                {
                    "faculty": faculty,
                    "courses": courses,
                    "message": "Error adding student.",
                },
            )

    return render(
        request,
        "Questionnaire/EditStudents.html",
        {
            "faculty": faculty,
            "courses": courses,
        },
    )


@login_required
@csrf_exempt
def edit_doctor(request):
    faculty = Organisation.objects.get(user=User.objects.get(id=request.user.id))
    i = None

    if request.method == "POST":
        doctor_data = zip(
            request.POST.getlist("instructor_name"),
            request.POST.getlist("instructor_email"),
        )

        for data in doctor_data:
            new_password = User.objects.make_random_password()

            try:
                user = User.objects.create_user(
                    username=data[0],
                    email=data[1],
                    password=new_password,
                    is_instructor=True,
                )
            except:
                return render(
                    request,
                    "Questionnaire/EditDoctors.html",
                    {"faculty": faculty, "message": "Instructor already exists."},
                )
            i = Instructor.objects.create(
                user=user, organisation=faculty, is_teaching_assistant=False
            )

        if i:
            return render(
                request,
                "Questionnaire/EditDoctors.html",
                {"faculty": faculty, "message": "Instructor added successfully."},
            )
        else:
            return render(
                request,
                "Questionnaire/EditDoctors.html",
                {"faculty": faculty, "message": "Error adding instructor."},
            )

    return render(
        request,
        "Questionnaire/EditDoctors.html",
        {
            "faculty": faculty,
        },
    )


@login_required
@csrf_exempt
def edit_teaching_assistant(request):
    faculty = Organisation.objects.get(user=User.objects.get(id=request.user.id))
    i = None

    if request.method == "POST":
        ta_data = zip(
            request.POST.getlist("instructor_name"),
            request.POST.getlist("instructor_email"),
        )

        for data in ta_data:
            new_password = User.objects.make_random_password()

            try:
                user = User.objects.create_user(
                    username=data[0],
                    email=data[1],
                    password=new_password,
                    is_instructor=True,
                )
            except:
                return render(
                    request,
                    "Questionnaire/EditTeachingAssistants.html",
                    {
                        "faculty": faculty,
                        "message": "Teaching Assistant already exists.",
                    },
                )
            i = Instructor.objects.create(
                user=user, organisation=faculty, is_teaching_assistant=True
            )

        if i:
            return render(
                request,
                "Questionnaire/EditTeachingAssistants.html",
                {
                    "faculty": faculty,
                    "message": "Teaching Assistant added successfully.",
                },
            )
        else:
            return render(
                request,
                "Questionnaire/EditTeachingAssistants.html",
                {"faculty": faculty, "message": "Error adding Teaching Assistant."},
            )

    return render(
        request,
        "Questionnaire/EditTeachingAssistants.html",
        {
            "faculty": faculty,
        },
    )


@login_required
@csrf_exempt
def edit_course(request):
    has_lab = True
    has_sec = True
    # students = Student.objects.filter(organisation=Organisation.objects.get(user=User.objects.get(id=request.user.id)))
    instructors = Instructor.objects.filter(is_teaching_assistant=False)
    teaching_assistants = Instructor.objects.filter(is_teaching_assistant=True)
    semesters = Semester.objects.all()

    if request.method == "POST":
        semester_no = request.POST["semester_no"]
        course_name = request.POST["course_name"]
        course_code = request.POST["course_code"]
        lecturer_name = request.POST["lecturer_name"]
        objectives = request.POST["objectives"]
        credit_hours = request.POST["credit_hours"]
        outcomes = request.POST["outcomes"]
        aims = request.POST["aims"]
        # studentss = request.POST.getlist("studentss")
        instructor_lab = request.POST["instructor_lab"]
        instructor_sec = request.POST["instructor_sec"]

        if instructor_lab == "None":
            has_lab = False
        if instructor_sec == "None":
            has_sec = False

        semester = Semester.objects.get(id=semester_no)
        instructor = Instructor.objects.get(user_id=lecturer_name)

        try:
            course = Course.objects.get(CourseName=course_name, CourseCode=course_code)
            if course.SemID.filter(id=semester_no).exists():
                return render(
                    request,
                    "Questionnaire/EditCourse.html",
                    {
                        "message": "This course already exists in this semester.",
                        # "students": students,
                        "instructors": instructors,
                        "teaching_assistants": teaching_assistants,
                        "semesters": semesters,
                    },
                )
        except:
            pass

        course = Course.objects.create(
            CourseName=course_name,
            CourseCode=course_code,
            flagLab=has_lab,
            flagSec=has_sec,
            Objectives=objectives,
            Aims=aims,
            Outcomes=outcomes,
            CreditHours=credit_hours,
        )

        course.SemID.add(semester)
        lec = Lecture.objects.create(
            course=course, instructor_id=instructor, SemesterId=semester
        )

        if has_lab:
            lab = Lab.objects.create(
                course=course,
                instructor_id=Instructor.objects.get(user_id=instructor_lab),
                SemesterId=semester,
            )
        if has_sec:
            sec = Section.objects.create(
                course=course,
                instructor_id=Instructor.objects.get(user_id=instructor_sec),
                SemesterId=semester,
            )

        """ for student in studentss:
            course.StudentID.add(Student.objects.get(user_id=student))
            course.save() """

        return render(
            request,
            "Questionnaire/EditCourse.html",
            {
                "message": "Course added successfully",
                # "students": students,
                "instructors": instructors,
                "teaching_assistants": teaching_assistants,
                "semesters": semesters,
            },
        )

    return render(
        request,
        "Questionnaire/EditCourse.html",
        {
            # "students": students,
            "instructors": instructors,
            "teaching_assistants": teaching_assistants,
            "semesters": semesters,
        },
    )


@login_required
@csrf_exempt
def edit_semester(request):
    faculty = Organisation.objects.get(user=User.objects.get(id=request.user.id))

    if request.method == "POST":
        year = request.POST["year"]
        semester = request.POST["semester"]

        try:
            s = Semester.objects.create(
                year=year, semester=semester, organisation=faculty
            )
        except:
            return render(
                request,
                "Questionnaire/addSemester.html",
                {
                    "faculty": faculty,
                    "message": "Semester already exists",
                },
            )

        s.save()

        if s:
            return render(
                request,
                "Questionnaire/addSemester.html",
                {
                    "faculty": faculty,
                    "message": "Semester added successfully",
                },
            )
        else:
            return render(
                request,
                "Questionnaire/addSemester.html",
                {
                    "faculty": faculty,
                    "message": "Error adding semester",
                },
            )

    return render(
        request,
        "Questionnaire/addSemester.html",
        {
            "faculty": faculty,
        },
    )


@login_required
@csrf_exempt
def manage_results(request):
    semesters = Semester.objects.all()

    if request.method == "POST":
        id = request.POST["id"]
        id = int(id[0])

        courses = Course.objects.filter(SemID__in=[id])

        return render(
            request,
            "Questionnaire/manage-result.html",
            {
                "semesters": semesters,
                "courses": courses,
            },
        )

    return render(
        request,
        "Questionnaire/manage-result.html",
        {
            "semesters": semesters,
        },
    )


@login_required
def result(request, course_id):
    lab_percaentage_positive = 0
    lab_percaentage_neutral = 0
    lab_percaentage_negative = 0

    sec_percaentage_positive = 0
    sec_percaentage_neutral = 0
    sec_percaentage_negative = 0

    course = Course.objects.get(pk=course_id)
    lec = Lecture.objects.get(course=course)
    try:
        lab = Lab.objects.get(course=course)
    except:
        lab = None

    try:
        sec = Section.objects.get(course=course)
    except:
        sec = None

    lecturer = Instructor.objects.get(user_id=lec.instructor_id)

    try:
        total_results_lec = Result.objects.filter(LecResult=lec).count()
        if lab:
            total_results_lab = Result.objects.filter(LabResult=lab).count()
        if sec:
            total_results_sec = Result.objects.filter(SecResult=sec).count()
        total_results_lecturer = Result.objects.filter(LectuererResult=lecturer).count()

        lec_results_positive = Result.objects.filter(LecResult=lec, ScoreLec=1).count()
        if lab:
            lab_results_positive = Result.objects.filter(
                LabResult=lab, ScoreLab=1
            ).count()
        if sec:
            sec_results_positive = Result.objects.filter(
                SecResult=sec, ScoreSec=1
            ).count()
        lecturer_results_positive = Result.objects.filter(
            LectuererResult=lecturer, ScoreLectuerer=1
        ).count()

        lec_results_neutral = Result.objects.filter(LecResult=lec, ScoreLec=0).count()
        if lab:
            lab_results_neutral = Result.objects.filter(
                LabResult=lab, ScoreLab=0
            ).count()
        if sec:
            sec_results_neutral = Result.objects.filter(
                SecResult=sec, ScoreSec=0
            ).count()
        lecturer_results_neutral = Result.objects.filter(
            LectuererResult=lecturer, ScoreLectuerer=0
        ).count()

        lec_results_negative = Result.objects.filter(LecResult=lec, ScoreLec=-1).count()
        if lab:
            lab_results_negative = Result.objects.filter(
                LabResult=lab, ScoreLab=-1
            ).count()
        if sec:
            sec_results_negative = Result.objects.filter(
                SecResult=sec, ScoreSec=-1
            ).count()
        lecturer_results_negative = Result.objects.filter(
            LectuererResult=lecturer, ScoreLectuerer=-1
        ).count()
    except:
        return render(
            request, "Questionnaire/result.html", {"message": "No results found."}
        )

    try:
        lec_percaentage_positive = (lec_results_positive / total_results_lec) * 100
        if lab:
            lab_percaentage_positive = (lab_results_positive / total_results_lab) * 100
        if sec:
            sec_percaentage_positive = (sec_results_positive / total_results_sec) * 100
        lecturer_percaentage_positive = (
            lecturer_results_positive / total_results_lecturer
        ) * 100

        lec_percaentage_neutral = (lec_results_neutral / total_results_lec) * 100
        if lab:
            lab_percaentage_neutral = (lab_results_neutral / total_results_lab) * 100
        if sec:
            sec_percaentage_neutral = (sec_results_neutral / total_results_sec) * 100
        lecturer_percaentage_neutral = (
            lecturer_results_neutral / total_results_lecturer
        ) * 100

        lec_percaentage_negative = (lec_results_negative / total_results_lec) * 100
        if lab:
            lab_percaentage_negative = (lab_results_negative / total_results_lab) * 100
        if sec:
            sec_percaentage_negative = (sec_results_negative / total_results_sec) * 100
        lecturer_percaentage_negative = (
            lecturer_results_negative / total_results_lecturer
        ) * 100

    except:
        return render(
            request, "Questionnaire/result.html", {"message": "No results found."}
        )

    return render(
        request,
        "Questionnaire/result.html",
        {
            "lec_percaentage_positive": lec_percaentage_positive,
            "lab_percaentage_positive": lab_percaentage_positive,
            "sec_percaentage_positive": sec_percaentage_positive,
            "lecturer_percaentage_positive": lecturer_percaentage_positive,
            "lec_percaentage_neutral": lec_percaentage_neutral,
            "lab_percaentage_neutral": lab_percaentage_neutral,
            "sec_percaentage_neutral": sec_percaentage_neutral,
            "lecturer_percaentage_neutral": lecturer_percaentage_neutral,
            "lec_percaentage_negative": lec_percaentage_negative,
            "lab_percaentage_negative": lab_percaentage_negative,
            "sec_percaentage_negative": sec_percaentage_negative,
            "lecturer_percaentage_negative": lecturer_percaentage_negative,
            "lab": lab,
            "sec": sec,
        },
    )


@login_required
def feedback_results_selectes(request):
    # Get the total number of feedbacks
    total_feedbacks = Selectes.objects.count()

    # Initialize a dictionary to hold the percentages for each question
    question_percentages = {}

    # Loop through each question and get the count of each answer
    for i in range(1, 29):
        answers = Selectes.objects.values("question{}".format(i)).annotate(
            count=Count("id")
        )
        question_percentages[i] = {}
        for answer in answers:
            percent = round((answer["count"] / total_feedbacks) * 100)
            question_percentages[i][answer["question{}".format(i)]] = percent

    context = {"question_percentages": question_percentages}
    return render(request, "Questionnaire/feedback_results_selects.html", context)


@login_required
@csrf_exempt
def super_admin(request):
    admin_name = ["FCI"]

    if request.method == "POST":
        admin_email = request.POST["admin_email"]

        new_password = User.objects.make_random_password()

        try:
            user = User.objects.create_user(
                username=admin_name[0],
                email=admin_email,
                password=new_password,
                is_organisation=True,
            )
            o = Organisation.objects.create(user=user)
        except:
            return render(
                request,
                "Questionnaire/SuperAdmin.html",
                {"message": "Admin already exists."},
            )

        send_to = [admin_email]
        if o:
            gmail.send_email(
                to_list=send_to,
                subject="Your New Password of Questionnaire System As Admin",
                body=f"PASSWORD: {new_password}",
            )
            return render(
                request,
                "Questionnaire/SuperAdmin.html",
                {
                    "message": "Admin added successfully",
                },
            )

    return render(request, "Questionnaire/SuperAdmin.html")
