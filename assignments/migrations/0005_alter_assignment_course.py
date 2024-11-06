import django.db.models.deletion
from django.db import migrations, models

def set_default_course(apps, schema_editor):
    Assignment = apps.get_model('myapp', 'Assignment')
    Course = apps.get_model('courses', 'Course')
    default_course = Course.objects.first()  # Choose the first course or create a default course
    if default_course:
        Assignment.objects.filter(course__isnull=True).update(course=default_course)

class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
        ('myapp', '0004_assignment_course'),
    ]

    operations = [
        # Run the custom function to set a default course for NULL entries
        migrations.RunPython(set_default_course),
        
        # Alter the field to be non-nullable after setting a default
        migrations.AlterField(
            model_name='assignment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='courses.course'),
        ),
    ]
