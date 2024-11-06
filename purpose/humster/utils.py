menu = [
    {'title': 'About site', "tag_name": 'about'},
    {'title': 'Add paragraph', "tag_name": 'add_par'},
    {'title': 'Take away', "tag_name": 'take_away',},
]

class DataMixin:
    title_page = None
    cat_selected = None
    extra_context = {}
    paginate_by = 4

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if self.cat_selected is not None:
            self.extra_context['cat_selected'] = self.cat_selected

    def get_mixin_context(self, context, **kwargs):
        context['cat_selected'] = None
        context.update(kwargs)
        return context