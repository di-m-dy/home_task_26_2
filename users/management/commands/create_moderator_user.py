from django.contrib.auth.models import Permission, Group
from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        permission_code_names = (
            'change_course',
            'view_course',
            'change_lesson',
            'view_lesson'
        )
        permissions = Permission.objects.filter(codename__in=permission_code_names).all()
        group, created = Group.objects.get_or_create(name='moderator')
        for permission in permissions:
            group.permissions.add(permission)
        user = User.objects.create(
            email='moderator@example.com',
            first_name='Moderator',
            last_name='Moderator Courses & Lessons'
        )
        user.groups.add(group)
        user.set_password('qweasd')
        user.save()
