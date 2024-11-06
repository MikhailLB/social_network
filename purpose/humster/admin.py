from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Humster, Category


class MarriedFilter(admin.SimpleListFilter):
    title = "Статус женщин"
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('married', 'Замужем'),
            ('single', 'Не замужем'),
        ]

    def queryset(self, request, queryset):
        if self.value() == "married":
            return queryset.filter(husband__isnull=False)
        elif self.value() == "single":
            return queryset.filter(husband__isnull=True)


@admin.register(Humster)
class WomenAdmin(admin.ModelAdmin):
    fields = ['title','photo', 'post_photo', "content", 'slug', "cat", 'husband', 'tags']
    #exclude = None исключает поля
    readonly_fields = ['post_photo']
    # prepopulated_fields = {"slug": ("title",) }
    # filter_horizontal = ['tags']
    filter_vertical = ['tags']
    list_display = ('title','post_photo', 'time_create', 'is_published', 'cat',)
    list_display_links = ('title',)
    ordering = ['time_create', 'title',]
    list_editable =('is_published',)
    list_per_page = 20
    actions = ['set_published', 'del_published']
    search_fields = ['title', 'cat__name']
    list_filter = [MarriedFilter, 'cat__name', 'is_published',]
    save_on_top = True

    @admin.display(description='Изображение', ordering='content')
    def post_photo(self, humster: Humster):
        if humster.photo:
            return mark_safe(f"<img src='{humster.photo.url}', width=50")
        return 'Нет фото.'
    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Humster.Status.PUBLISHED)
        self.message_user(request, f'Изменено {count} записей.')

    @admin.action(description='Скрыть выбранные записи')
    def del_published(self, request, queryset):
        count = queryset.update(is_published=Humster.Status.DRAFT)
        self.message_user(request, f'{count} сняты с публикации!', messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

