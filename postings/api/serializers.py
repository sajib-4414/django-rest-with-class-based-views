from rest_framework import serializers
from postings.models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):#looks like forms.modelForm
    class Meta:
        model = BlogPost
        fields = [
            'pk',
            'user',
            'title',
            'content',
            'timestamp',
        ]
        read_only_fields = ['user']


    def validate_title(self,value):
        qs = BlogPost.objects.filter(title__iexact=value)#including instance

        if self.instance:
            qs = qs.exists(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError("The title has been already used")
        return value


#serializers do 2 things
#converts data to JSON
#validation for the data passed