from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ("reviews", "0002_initial"),
        ("core", "0003_remove_program_price_max_remove_program_price_min_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="center",
            field=models.ForeignKey(
                to="core.center",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reviews",
                null=True,
                blank=True,
            ),
        ),
    ]
