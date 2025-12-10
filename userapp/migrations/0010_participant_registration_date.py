from django.db import migrations, models
import datetime

def set_default_date(apps, schema_editor):
    Participant = apps.get_model("userapp", "Participant")
    for row in Participant.objects.all():
        row.registration_date = datetime.datetime.now()
        row.save()

class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0009_remove_eventregistration_attended_participant'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='registration_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.RunPython(set_default_date),
        migrations.AlterField(
            model_name='participant',
            name='registration_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
