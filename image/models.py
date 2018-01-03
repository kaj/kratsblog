from django.db import models
from django.db.models import Max
from blog.models import Post
from django.utils.safestring import mark_safe
from textile import textile

class Image(models.Model):
    image = models.ImageField(upload_to='%Y/img')
    caption = models.TextField()
    post = models.ForeignKey(Post, db_index=True, on_delete=models.CASCADE)
    order = models.IntegerField(blank=True, db_index=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return u'%s %r' % (self.image, self.caption)
    
    def save(self, *args, **kwargs):
        if not self.order:
            others = Image.objects.filter(post=self.post)
            self.order = \
                (others.aggregate(Max('order'))['order__max'] or 0) + 10
        super(Image, self).save(*args, **kwargs)

    def caption_markup(self):
        return mark_safe(textile(self.caption))
