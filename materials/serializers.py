from rest_framework.serializers import ModelSerializer, SerializerMethodField
from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()

    def get_lessons_count(self, obj):
        return obj.lesson_set.count()

    class Meta:
        model = Course
        fields = '__all__'

class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
