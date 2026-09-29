# items/

Django app for the lost & found item records themselves — this is the
"ordinary CRUD" half of the project: models (Item, and probably separate
LostReport / FoundReport if you track them differently), views, URLs,
and the page that displays matching results.

Anticipates `python manage.py startapp items` from inside backend/.
