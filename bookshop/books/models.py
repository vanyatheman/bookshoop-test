from django.db import models


class Book(models.Model):
    title = models.CharField(max_length = 150)
    author = models.CharField(max_length = 100)
    price = models.FloatField(null=True, blank=True)
    publish_date = models.DateField()
    publisher = models.CharField(max_length=150)
    description = models.TextField(max_length = 500, default=None, blank=True)
    # isbn = models.CharField()
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    book_available = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Order(models.Model):
	product = models.ForeignKey(Book, max_length=200, null=True, blank=True, on_delete = models.SET_NULL)
	created =  models.DateTimeField(auto_now_add=True) 

	def __str__(self):
		return self.product.title
