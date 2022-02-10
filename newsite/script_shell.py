import datetime as dt
from polls.models import *

q = Question.objects.all()
q = q[3]
print()