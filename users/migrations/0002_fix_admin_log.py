# users/migrations/0002_fix_admin_log.py
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('users', '0001_initial'),  # This references your last migration you showed
    ]

    operations = [
        migrations.RunSQL(
            """
            ALTER TABLE django_admin_log
            DROP CONSTRAINT IF EXISTS django_admin_log_user_id_c564eba6_fk_auth_user_id;
            
            ALTER TABLE django_admin_log
            ADD CONSTRAINT django_admin_log_user_id_fk
            FOREIGN KEY (user_id) REFERENCES custom_user(id)
            ON DELETE CASCADE;
            """,
            # Reverse SQL if you need to rollback
            """
            ALTER TABLE django_admin_log
            DROP CONSTRAINT IF EXISTS django_admin_log_user_id_fk;
            
            ALTER TABLE django_admin_log
            ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id
            FOREIGN KEY (user_id) REFERENCES auth_user(id)
            ON DELETE CASCADE;
            """
        ),
    ]