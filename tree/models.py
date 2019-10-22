from django.db import models


class TreeManager(models.Manager):
    def get_subtree_dict(self, root):
        queryset = self.get_queryset().filter(pk=root)
        queryset.prefetch_related('tree_set')
        if not queryset:
            raise Tree.DoesNotExist(root)
        node = queryset[0]
        subtree = dict(
            id=root,
            name=node.name,
            children=[self.get_subtree_dict(child.pk) for child in node.tree_set.all()]
        )
        return subtree


class Tree(models.Model):
    parent = models.ForeignKey(
        'self', models.CASCADE, null=True, verbose_name='Родитель')
    name = models.CharField(max_length=255, verbose_name='Название')

    objects = TreeManager()
