from django.db import models
from django import forms

from modelcluster.fields import ParentalKey,ParentalManyToManyField
from wagtail.models import Page,Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel,MultiFieldPanel
from wagtail.snippets.models import register_snippet
class BlogIndexPage(Page):
    intro = RichTextField(blank=True)
    def get_context(self,request):
        context = super().get_context(request)
        blogpages=self.get_children().live().order_by('-first_published_at')
        context['blogpages']=blogpages
        return context
    content_panels= Page.content_panels + ["intro"]
    
class Blogpage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    authors= ParentalManyToManyField('blog.Author',blank=True)
    def main_image(self):
        gallery_item=self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None
    content_panels= Page.content_panels + [MultiFieldPanel(["date",FieldPanel("authors",widget=forms.CheckboxSelectMultiple),],heading="Blog information"),"intro","body","gallery_images"]

class BlogPageGalleryImage(Orderable):
    page= ParentalKey(Blogpage, on_delete=models.CASCADE,related_name='gallery_images')
    image= models.ForeignKey('wagtailimages.Image',on_delete=models.CASCADE,related_name='+')
    caption= models.CharField(blank=True,max_length=250)
    panels=["image","caption"]
    
@register_snippet
class Author(models.Model):
    name=models.CharField(max_length=250)
    author_image=models.ForeignKey(
        'wagtailimages.Image',null=True,blank=True,
        on_delete=models.SET_NULL,related_name="+"
    )
    panels=["name","author_image"]
    
    def __str__(self):
        return self.name
    
    class meta:
        verbose_name_plural='Authors'