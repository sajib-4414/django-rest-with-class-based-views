from .serializers import BlogPostSerializer
from rest_framework import generics, mixins
from postings.models import BlogPost
from django.db.models import Q
from .permissions import IsOwnerOrReadOnly


class BlogPostApiView(mixins.CreateModelMixin, generics.ListAPIView):
    '''
    slug, id(?P<pk>\d+)
    '''
    lookup_field =  'pk'
    serializer_class = BlogPostSerializer
    # queryset = BlogPost.objects.all()

    def get_queryset(self):#overriding the contents of query_set
        qs =  BlogPost.objects.all()
        #this q means, url/?q=search_phrase
        #getting query means getting the search phrase
        query = self.request.GET.get('q')
        if query is not None:
            qs = qs.filter(Q(title__icontains=query) | Q(content__icontains=query)).distinct()
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    #this will add extra create funcionality even though it does not inherit from listapiview
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



class BlogPostRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field =  'pk'
    serializer_class = BlogPostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):#overriding the contents of query_set
        return BlogPost.objects.all()

    # def get_object(self):
    #     pk = self.kwargs.get("pk")
    #     return BlogPost.objects.get(pk=pk)


