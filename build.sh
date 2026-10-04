#!/usr/bin/env bash
#!/usr/bin/env bash

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate

python manage.py shell -c "import os; from django.contrib.auth import get_user_model; User=get_user_model(); username=os.environ.get('Husena'); password=os.environ.get('Hussu@123'); user,created=User.objects.get_or_create(username=username); user.set_password(password); user.is_staff=True; user.is_superuser=True; user.is_active=True; user.save(); print('Production admin created/updated:', username)"