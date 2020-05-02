from django.db import models
from users.models import User
from book.models import Merchandise

# Create your models here.
class Cart(models.Model):
    id_user = models.ForeignKey('users.User', models.DO_NOTHING, db_column='id_user')
    id_merchandise = models.ForeignKey('book.Merchandise', models.DO_NOTHING, db_column='id_merchandise')
    quantity = models.IntegerField()
    expire_date = models.DateField()
    created_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'cart'



