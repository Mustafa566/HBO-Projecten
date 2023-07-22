# Code inspired by
# https://www.educative.io/courses/django-admin-web-developers/RLPEYWRpDPV
# https://faker.readthedocs.io/en/stable/
# https://gist.github.com/isaqueprofeta/83b8bc9824b55b63012fa975e7264c25
# https://suyojtamrakar.medium.com/how-to-provide-initial-data-in-django-models-2422aaf3c09a

"""
Instructions:

When database is empty:

1. Load JSON data into database:

Run command: `python manage.py loaddata courses.json, teachers.json, classes.json`

2. Then Run this Python file to populate the student database.
"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
import django

django.setup()
import json

from faker import Faker
from attendanceItems.models import *
from model_bakery.recipe import baker
from django.contrib.auth.admin import User


def populate_student_db():
    fake = Faker()

    # Loads JSON classe instances into this file
    json_file_path = os.path.abspath('attendanceItems/fixtures/classes.json')
    with open(json_file_path) as f:
        classe_data = json.load(f)

    classes_total = len(classe_data)
    students_total = 92
    students_per_classe = students_total // classes_total

    for c in classe_data:
        classe_id = c['fields']['classe_id']
        classe = Classe.objects.get(classe_id=classe_id)

        for s in range(students_per_classe):
            student_id = fake.unique.zipcode()
            email_domain = '@hr.nl'
            email = f"{''.join(student_id)}{email_domain}"
            last_name = fake.last_name()
            first_name = fake.first_name()

            student = baker.make(Student,
                                 student_id=student_id,
                                 email=email,
                                 classe=classe,
                                 last_name=last_name,
                                 first_name=first_name,
                                 project_group=fake.company(),
                                 )

            student.save()

            student_user = baker.make(User,
                                      username=f"{student_id}",
                                      # password=,
                                      email=f"{email}",
                                      last_name=f"{last_name}",
                                      first_name=f"{first_name}",
                                      )

            student_user.save()

        remaining_students = students_total - (students_per_classe * classes_total)
        if s == (students_per_classe - 1) and remaining_students > 0:
            for i in range(remaining_students):
                student = baker.make(Student,
                                     student_id=student_id,
                                     email=f"{''.join(student_id)}{email_domain}",
                                     classe=classe,
                                     last_name=fake.last_name(),
                                     first_name=fake.first_name(),
                                     project_group=fake.company(),
                                     )

                student.save()

                student_user = baker.make(User,
                                          username=f"{student_id}",
                                          # password=,
                                          email=f"{email}",
                                          last_name=f"{last_name}",
                                          first_name=f"{first_name}",
                                          )

                student_user.save()


populate_student_db()
