from django.db import models


class Rawdata(models.Model):
    upload_datetime = models.DateTimeField('Дата/время запуска', auto_now_add=True)
    data = models.TextField('Данные',)


class Method(models.Model):
    method = models.CharField('Метод', max_length=30)

    def __str__(self):
        return self.method


class Psychotherapist(models.Model):    
    airtable_id = models.CharField('ID записи Airtable', max_length=18)
    name = models.CharField('Имя', max_length=30)
    image = models.ImageField("Фотография")
    tag = models.ManyToManyField(Method, verbose_name='Методы', related_name='psychotherapists_tag')

    def __str__(self):
        return self.name
