# Generated by Django 2.0.1 on 2018-03-11 01:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=-1)),
                ('grade', models.DecimalField(decimal_places=2, default=0, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200)),
                ('votes', models.IntegerField(default=0)),
                ('correct', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ClassQuizResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('average', models.IntegerField(default=0)),
                ('median', models.IntegerField(default=0)),
                ('std_dev', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200)),
                ('course_description', models.CharField(max_length=200)),
                ('size', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('correct', models.BooleanField(default=False)),
                ('correct_answer', models.IntegerField(default=-1)),
                ('selected_answer', models.IntegerField(default=-2)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_text', models.CharField(max_length=200)),
                ('quiz_text', models.CharField(max_length=200)),
                ('number_correct', models.IntegerField(default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Course')),
            ],
            options={
                'verbose_name': 'Better Quiz',
                'verbose_name_plural': 'Better Quizzes',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('courses', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Course')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Quiz'),
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(to='polls.Student'),
        ),
        migrations.AddField(
            model_name='classquizresults',
            name='course',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='polls.Course'),
        ),
        migrations.AddField(
            model_name='classquizresults',
            name='quiz',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='polls.Quiz'),
        ),
        migrations.AddField(
            model_name='classquizresults',
            name='teacher',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='polls.Teacher'),
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Question'),
        ),
        migrations.AddField(
            model_name='answerset',
            name='answers',
            field=models.ManyToManyField(to='polls.Choice'),
        ),
        migrations.AddField(
            model_name='answerset',
            name='quiz',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='polls.Quiz'),
        ),
        migrations.AddField(
            model_name='answerset',
            name='student',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='polls.Student'),
        ),
    ]
