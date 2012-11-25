# coding=UTF-8
from django.utils import unittest
from cr3components.cms.models import *


class CmsTest(unittest.TestCase):
    def setUp(self):
        Node.objects.get_or_create_path("d1/d2/d3/d4")
        Category.objects.get_or_create(slug="news")
            
    def tearDown(self):
        Node.objects.all().delete()
    
    def testTree(self):
        d1 = Node.objects.get(slug="d1")
        d2 = Node.objects.get(slug="d2")
        d3 = Node.objects.get(slug="d3")
        d4 = Node.objects.get(slug="d4")
        self.assertEqual(d4.path(),"d1/d2/d3/d4")
        self.assertEqual(d3.path(),"d1/d2/d3")
        self.assertEqual(d2.path(),"d1/d2")
        self.assertEqual(d1.path(),"d1")
        roots = Node.tree.root_nodes()
        self.assertEqual(roots[0],d1)
    
    def testInheritance(self):
        p1 = PageNode.objects.get_or_create_path("p1")
        p4 = PageNode.objects.get_or_create_path("d1/d2/p3/p4")
        self.assertEqual(p4.path(),"d1/d2/p3/p4")
        self.assertIsInstance(p4, PageNode)
        self.assertIsInstance(p1, PageNode)
        roots = Node.tree.root_nodes()
        roots2 = Node.objects.published().filter(parent__isnull=True)

        self.assertEquals(len(roots),2)
        self.assertEquals(len(roots2),2)
      
        self.assertEquals(Node.objects.all().count(),7)
        self.assertEquals(roots2[1],p1)
        self.assertIsInstance(roots2[1],PageNode)
        self.assertIsInstance(roots2[0],Node)

    def testFilters(self):
        cat = Category.objects.get(slug="news")
        (n1,c) = PostNode.objects.get_or_create(slug="n1",state="published")
        (n2,c) = PostNode.objects.get_or_create(slug="n2",state="published")
        (n3,c) = PostNode.objects.get_or_create(slug="n3",state="published")

        (f1,c) = FilterNode.objects.get_or_create(slug="f1",state="published",filter_category = cat)
        
        n1.categories.add(cat)
        n2.categories.add(cat)
        
        f1c = f1.get_children().all()
        self.assertEqual(f1c[0],n1)
        self.assertEqual(f1c[1],n2)
        self.assertEqual(len(f1c),2)

        