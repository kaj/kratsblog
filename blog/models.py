from autoslug.fields import AutoSlugField
from django.db import models

class Post(models.Model):
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    posted_time = models.DateTimeField()
    slug = AutoSlugField(populate_from='title',
                         unique_with='posted_time__month')

    def __unicode__(self):
        return u'%s (%s)' % (self.title, self.posted_time)

    def get_absolute_url(self):
        return '/%d/%02d/%s' % (self.posted_time.year,
                                self.posted_time.month,
                                self.slug)
