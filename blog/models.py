# -*- encoding: utf-8; -*-
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from datetime import timedelta
from textile import textile

FMT_HELP = ('Formatering enligt Textile.  _kursiv_ *fet*, "länktext":url.  ' +
            'Tomrad för styckesbrytning ' +
            '(<a href="https://txstyle.org/" target="_new">mer hjälp</a>).')

class Post(models.Model):
    
    title = models.CharField(
        max_length=200,
        help_text=u'Om titel ändras kommer urlen fortfarande se ut'
        u' som gamla titeln.')
    content = models.TextField(help_text=FMT_HELP)
    
    posted_time = models.DateTimeField(
        null=True, blank=True, db_index=True,
        help_text=u'Lämna tomt för att lämna posten opublicerad.')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    slug = models.SlugField(db_index=True)

    class Meta:
        ordering = ['-posted_time']

    def save(self, *args, **kwargs):
        # Set a slug if necessary, make sure it is unique enough
        if self.title and self.posted_time and not self.slug:
            self.slug = slugify(self.title)
        if self.slug and self.posted_time:
            n = 1
            while self._duplicate_slugs():
                n = n + 1
                self.slug = '%s-%s' % (slugify(self.title), n)
        super().save(*args, **kwargs)

    def _duplicate_slugs(self):
        q = Post.objects
        if self.id:
            q = q.exclude(id=self.id)
        q = q.filter(slug=self.slug,
                     posted_time__year=self.posted_time.year,
                     posted_time__month=self.posted_time.month)
        return q.count()

    def __str__(self):
        return u'%s (%s)' % (self.title, self.posted_time)

    def get_absolute_url(self):
        if self.posted_time and self.slug:
            return '/%d/%02d/%s' % (self.posted_time.year,
                                    self.posted_time.month,
                                    self.slug)
    def linkedshort(self, maxlen=600):
        if len(self.content) < maxlen:
            return mark_safe(textile(self.content))
        
        paras = self.content.split('\r\n\r\n')
        lens = [len(p) for p in paras]

        def result(paras):
            return mark_safe(textile(
                u'%s ...\n\n"Läs mer":%s' % ('\n\n'.join(paras),
                                             self.get_absolute_url())))

        for n in range(1,len(paras)):
            if n > 1 and sum(lens[:n]) > maxlen:
                return result(paras[:n-1])
            if sum(lens[:n]) > maxlen/2:
                return result(paras[:n])
        
        return mark_safe(textile(self.content))

    def content_markup(self):
        return mark_safe(textile(self.content))

    @property
    def updated_later(self):
        # updated_at is set after posted_time, so allow some slack
        return self.updated_at > self.posted_time + timedelta(minutes=5)

    @property
    def first_image(self):
        # TODO Let the manager do this, so its (optionaly) joind in load?
        if self.image_set.count():
            return self.image_set.all()[0]
        else:
            return None
