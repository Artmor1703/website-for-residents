from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.conf import settings

# Create your models here.


class Feedback(models.Model): #Обратная связь
    title = models.CharField('Тема', max_length=255, default='Без темы')
    question = models.TextField('Вопрос')
    answer = models.TextField('Ответ', default='Сообщение доставлено')
    time_quest = models.DateTimeField('Время вопроса', auto_now=False)
    time_answer = models.DateTimeField('Время ответа', auto_now=True)

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'


class Question(models.Model):
    title = models.CharField('Название', max_length=4096)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тема голосования'
        verbose_name_plural = 'Темы голосования'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    title = models.CharField('Название', max_length=4096)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'


class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    choice = models.ForeignKey(Choice, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Голос'
        verbose_name_plural = 'Голоса'


class CustomAccountManager(BaseUserManager): #Создание пользователей
    def create_user(self, email, apartment, password):
        user = self.model(email=email, apartment=apartment, password=password)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, apartment, password):
        email = 'admin@admin.ad'
        user = self.create_user(
            email=email,
            password=password,
            apartment=apartment,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, apartment_):
        print(apartment_)
        return self.get(apartment=apartment_)


class CustomUser(AbstractBaseUser): #Пользователи

    email = models.EmailField('Почта', default='user@email.ru')
    telenum = models.CharField('Телефон', max_length=11, default='80000000000')
    apartment = models.CharField('Квартира', max_length=4, unique=True)

    quadrature = models.IntegerField('Квадратура', default=0)
    fio = models.CharField('ФИО', max_length=255, default='Пользователь')
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'apartment'
    objects = CustomAccountManager()

    def get_short_name(self):
        return self.apartment

    def natural_key(self):
        return self.apartment

    def __str__(self):
        return str(self.apartment)

    def has_perm(self, perm, obj=None):
        # "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


    def has_module_perms(self, app_label):
    #"Does the user have permissions to view the app `app_label`?"
    # Simplest possible answer: Yes, always
        return True


    @property
    def is_staff(self):
    #"Is the user a member of staff?"
    # Simplest possible answer: All admins are staff
        return self.is_admin


class News(models.Model): #Новостная база
    title = models.CharField('Название', max_length=255)
    descr = models.TextField('Описание')
    time = models.DateTimeField('Время', auto_now=True)

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Category(models.Model): #Для ввода данных (login )
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']
