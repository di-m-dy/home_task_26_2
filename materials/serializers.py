from rest_framework.serializers import ModelSerializer, SerializerMethodField
from materials.models import Course, Lesson, Subscribe
from materials.validators import NoLinkValidator


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [NoLinkValidator(field_name='description')]


class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request:
            return obj.subscribes.filter(user=request.user).exists()

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = '__all__'
        validators = [NoLinkValidator(field_name='description')]


class LessonForCourseSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('title', 'description', 'owner')
        validators = [NoLinkValidator(field_name='description')]


class CourseCreateWithLessonsSerializer(ModelSerializer):
    lessons = LessonForCourseSerializer(many=True)

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


class SubscribeSerializer(ModelSerializer):
    class Meta:
        model = Subscribe
        fields = '__all__'
