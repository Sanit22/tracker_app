from main import cache
from app.models import *


@cache.memoize(50)
def dashboard_data(user_email):
    user = User.query.filter_by(email=user_email).first()
    return user

