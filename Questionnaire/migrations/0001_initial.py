# Generated by Django 4.1.5 on 2023-05-24 15:09

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CourseName', models.CharField(blank=True, max_length=64)),
                ('CourseCode', models.CharField(blank=True, max_length=64)),
                ('Objectives', models.TextField(blank=True)),
                ('Aims', models.TextField(blank=True)),
                ('Outcomes', models.TextField(blank=True)),
                ('CreditHours', models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)])),
                ('flagSec', models.BooleanField(default=False)),
                ('flagLab', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(help_text='Format: yyyy/yyyy', max_length=9)),
                ('semester', models.PositiveSmallIntegerField()),
            ],
            options={
                'ordering': ['year', 'semester'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_student', models.BooleanField(default=False)),
                ('is_instructor', models.BooleanField(default=False)),
                ('is_organisation', models.BooleanField(default=False)),
                ('username', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('is_teaching_assistant', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SemesterId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.semester')),
                ('course', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.course')),
                ('instructor_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.instructor')),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SemesterId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.semester')),
                ('course', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.course')),
                ('instructor_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.instructor')),
            ],
        ),
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SemesterId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.semester')),
                ('course', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.course')),
                ('instructor_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.instructor')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='SemID',
            field=models.ManyToManyField(related_name='Sem', to='Questionnaire.semester'),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('student_no', models.CharField(max_length=64, unique=True)),
                ('level', models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)])),
                ('organisation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='Questionnaire.organisation')),
            ],
        ),
        migrations.AddField(
            model_name='semester',
            name='organisation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='Questionnaire.organisation'),
        ),
        migrations.CreateModel(
            name='Selectes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question1', models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('question2', models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('question3', models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('question4', models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('question5', models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('question6', models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('question7', models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('question8', models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('question9', models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('question10', models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('question11', models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('question12', models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('question13', models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('question14', models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('question15', models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('question16', models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('question17', models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('question18', models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('question19', models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('question20', models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('question21', models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('question22', models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('question23', models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('question24', models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('question25', models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('question26', models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('question27', models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('question28', models.SmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('note', models.TextField(blank=True, null=True)),
                ('LabSelect', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='Questionnaire.lab')),
                ('LecSelect', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='Questionnaire.lecture')),
                ('SecSelect', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='Questionnaire.section')),
                ('stud_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.student')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ScoreLec', models.IntegerField(null=True)),
                ('ScoreLab', models.IntegerField(null=True)),
                ('ScoreSec', models.IntegerField(null=True)),
                ('ScoreLectuerer', models.IntegerField(null=True)),
                ('LabResult', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='Questionnaire.lab')),
                ('LecResult', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Questionnaire.lecture')),
                ('SecResult', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='Questionnaire.section')),
                ('LectuererResult', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='Questionnaire.instructor')),
            ],
        ),
        migrations.AddField(
            model_name='instructor',
            name='organisation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='Questionnaire.organisation'),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TextLec', models.TextField(blank=True)),
                ('TextLab', models.TextField(blank=True)),
                ('TextSec', models.TextField(blank=True)),
                ('TextLectuerer', models.TextField(blank=True)),
                ('LabFeedback', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='Questionnaire.lab')),
                ('LecFeedback', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='Questionnaire.lecture')),
                ('SecFeedback', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='Questionnaire.section')),
                ('stud_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Questionnaire.student')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='StudentID',
            field=models.ManyToManyField(related_name='Student', to='Questionnaire.student'),
        ),
        migrations.AlterUniqueTogether(
            name='semester',
            unique_together={('year', 'semester')},
        ),
    ]
