from modeltranslation.translator import register, TranslationOptions
from home.models import *

@register(Information)
class InformationTranslationOptions(TranslationOptions):
    fields = ('about_us',)

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title','description_full',)

@register(Faq)
class FaqTranslationOptions(TranslationOptions):
    fields = ('question','response',)

@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title','short_description','description',)