# from django_filters import FilterSet
# from .models import Post
#
# class PosttFilter(FilterSet):
#    class Meta:
#        model = Post
#        fields = {
#            'author': ['contains'],
#            'title': ['contains'],
#            'created_at': [
#                'start_date',   #дата должна быть меньше или равна указанной
#                'end_date ',    #дата должна быть больше или равна указанной
#            ],
#        }