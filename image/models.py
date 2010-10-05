from django.db import models
from django.db.models import Max
from blog.models import Post

class Image(models.Model):
    image = models.ImageField(upload_to='%Y/img')
    caption = models.TextField()
    post = models.ForeignKey(Post)
    order = models.IntegerField(blank=True)
    
    class Meta:
        ordering = ['order']
    
    def __unicode__(self):
        return u'%s' % self.image
    
    def save(self, *args, **kwargs):
        if not self.order:
            others = Image.objects.filter(post=self.post)
            self.order = others.aggregate(Max('order'))['order__max'] + 10
        super(Image, self).save(*args, **kwargs)
