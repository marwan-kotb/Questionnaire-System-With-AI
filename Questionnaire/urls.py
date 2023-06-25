from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("LoginAdmin", views.login_admin, name="login_admin"),
    path("LoginStudent", views.login_student, name="login_student"),
    path("Courses", views.courses, name="courses"),
    path("course/<int:course_id>", views.course, name="course"),
    path("questionnaire/<int:course_id>", views.questionnaire, name="questionnaire"),
    path("Selects/<int:course_id>", views.selects, name="selects"),
    path("Final", views.final, name="final"),
    path("Options", views.options, name="options"),
    path("EditStudent", views.edit_student, name="edit_student"),
    path("EditDoctor", views.edit_doctor, name="edit_doctor"),
    path("EditCourse", views.edit_course, name="edit_course"),
    path("EditSemester", views.edit_semester, name="edit_semester"),
    path("Logout", views.logout_view, name="logout"),
    path("ForgotPassword/<str:type>", views.forgot_password, name="forgot_password"),
    path(
        "EditTeachingAssistant",
        views.edit_teaching_assistant,
        name="edit_teaching_assistant",
    ),
    path("ManageResults", views.manage_results, name="manage_results"),
    path("Result/<int:course_id>", views.result, name="result"),
    path(
        "FeedbackResultsSelectes",
        views.feedback_results_selectes,
        name="feedback_results_selectes",
    ),
    path("SuperAdmin", views.super_admin, name="super_admin"),
]
