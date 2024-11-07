from rest_framework.serializers import ModelSerializer, SerializerMethodField
from materials.models import Course, Lesson
from materials.validators import NoLinkValidator


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [NoLinkValidator(field_name='content')]


class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = '__all__'
        validators = [NoLinkValidator(field_name='description')]


class CourseCreateWithLessonsSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Course
        fields = '__all__'
        validators = [NoLinkValidator(field_name='description')]

    def create(self, validated_data):
        lessons = validated_data.pop('lessons')
        course_object = Course.objects.create(**validated_data)
        for lesson in lessons:
            Lesson.objects.create(**lesson, course=course_object)
        return course_object

