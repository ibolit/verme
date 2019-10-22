from django.db import models
from django.db.models import Count


class TreeManager(models.Manager):
    def _format_node(self, tree_node, children_dicts):
        return dict(
            id=tree_node.pk,
            name=tree_node.name,
            children=children_dicts
        )

    def _get_children(self, pk):
        children = self.get_queryset().filter(parent=pk).annotate(num_children=Count('tree'))

        children_list = []
        for child in children:

            grandchildren = [] if not child.num_children else self._get_children(child.pk)
            children_list.append(self._format_node(child, grandchildren))
        return children_list

    def get_subtree_dict(self, root):
        root_node = self.get_queryset().get(pk=root)
        return self._format_node(root_node, self._get_children(root_node))

    def get_tree_dict(self):
        return self._get_children(None)


class Tree(models.Model):
    parent = models.ForeignKey(
        'self', models.CASCADE, null=True, verbose_name='Родитель')
    name = models.CharField(max_length=255, verbose_name='Название')

    objects = TreeManager()
