from django.test import TestCase

from tree.models import Tree


class TestTreeModel(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        t0 = Tree(name='Корень', parent=None)
        t0.save()
        t1 = Tree(name='Ветвь 1', parent=t0)
        t1.save()
        t2 = Tree(name='Ветвь 2', parent=t0)
        t2.save()
        t1_1 = Tree(name='Подветвь 1', parent=t1)
        t1_1.save()

    def test_get_subtree(self):
        subtree = Tree.objects.get_subtree_dict(1)
        self.assertDictEqual(
            subtree,
            {'id': 1, 'name': 'Корень', 'children':
                [
                    {'id': 2, 'name': 'Ветвь 1', 'children':
                        [
                            {'id': 4, 'name': 'Подветвь 1', 'children': []}
                        ]
                    },
                    {'id': 3, 'name': 'Ветвь 2', 'children': []}
                ]
            }
        )

    def test_get_nonexisting_subtree(self):
        self.assertRaises(Tree.DoesNotExist, Tree.objects.get_subtree_dict, 8)


    def test_get_tree(self):
        subtree = Tree.objects.get_tree_dict()
        self.assertListEqual(
            subtree,
            [
                {'id': 1, 'name': 'Корень', 'children':
                    [
                        {'id': 2, 'name': 'Ветвь 1', 'children':
                            [
                                {'id': 4, 'name': 'Подветвь 1', 'children': []}
                            ]
                        },
                        {'id': 3, 'name': 'Ветвь 2', 'children': []}
                    ]
                }
            ]
        )
