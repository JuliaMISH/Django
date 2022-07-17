from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.cache import cache


class Author(models.Model):
    autorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.autorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()

    def __str__(self):
        #return '{}'.format(self.autorUser)
        return f'{self.autorUser} (рейтинг: {self.ratingAuthor})'


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subs = models.ManyToManyField(User, through='SubsUser')

    def __str__(self):
        #return '{}'.format(self.autorUser)
        return f'{self.name}'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOISES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOISES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[0:123]}...'

    def preview_mail(self):
        return f'{self.text[0:50]}...'

    def post_link(self):
        return f'https://testdjango-1.relyt2003.repl.co/news/{self.id}'

    def __str__(self):
        return f'{self.title.title()}: {self.text[:20]}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 
        cache.delete(f'post-{self.pk}') 


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):

        return f'{self.categoryThrough.name}'


class SubsUser(models.Model):
    subsThrough = models.ForeignKey(Category, on_delete=models.CASCADE)
    userThrough = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.userThrough.username} signed for {self.subsThrough.name}'


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()                            
