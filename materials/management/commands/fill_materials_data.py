import json

from django.core.management import BaseCommand

from config.settings import BASE_DIR
from materials.serializers import CourseCreateWithLessonsSerializer, LessonSerializer, CourseSerializer


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(BASE_DIR / 'default_data/materials_data.json') as file:
            data = json.load(file)

        for course in data:
            lessons = course.pop('lessons')
            valid_lessons = []
            for lesson in lessons:
                lesson['owner'] = 1
                serialize_lesson = LessonSerializer(data=lesson)
                if serialize_lesson.is_valid():
                    valid_lessons.append(lesson)


            course['owner'] = 1
            serialize = CourseSerializer(data=course)
            if serialize.is_valid(raise_exception=True):
                course['lessons'] = valid_lessons
                new_serialize = CourseCreateWithLessonsSerializer(data=course)
                new_serialize.is_valid()
                new_serialize.save()
            else:
                print(f"Error")
