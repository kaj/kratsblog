# -*- encoding: utf-8; -*-
from autoslug.fields import AutoSlugField
from django.db import models

class Post(models.Model):
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    posted_time = models.DateTimeField()
    slug = AutoSlugField(populate_from='title',
                         unique_with='posted_time__month')

    class Meta:
        ordering = ['-posted_time']
    
    def __unicode__(self):
        return u'%s (%s)' % (self.title, self.posted_time)

    def get_absolute_url(self):
        return '/%d/%02d/%s' % (self.posted_time.year, self.posted_time.month,
                                self.slug)
    def linkedshort(self, maxlen=600):
        if len(self.content) < maxlen:
            return self.content
        
        paras = self.content.split('\r\n\r\n')
        lens = [len(p) for p in paras]

        def result(paras):
            return u'%s ...\n\n"Läs mer":%s' % ('\n\n'.join(paras),
                                               self.get_absolute_url())
        
        for n in range(1,len(paras)):
            if n > 1 and sum(lens[:n]) > maxlen:
                return result(paras[:n-1])
            if sum(lens[:n]) > maxlen/2:
                return result(paras[:n])
        
        return self.content
