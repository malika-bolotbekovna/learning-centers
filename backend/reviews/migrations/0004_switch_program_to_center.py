from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ("reviews", "0003_add_center_to_review"),
    ]

    operations = [
        # 1) Снимаем старое ограничение (program, author)
        migrations.AlterUniqueTogether(
            name="review",
            unique_together=set(),
        ),
        # 2) Удаляем поле program
        migrations.RemoveField(
            model_name="review",
            name="program",
        ),
        # 3) Ставим новое ограничение (center, author)
        migrations.AlterUniqueTogether(
            name="review",
            unique_together={("center", "author")},
        ),
    ]
