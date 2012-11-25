# coding=UTF-8
from django.utils import unittest
from cr3components.banners.models import *


class CmsTest(unittest.TestCase):
    def setUp(self):
        (self.fb, created) = BannerRoll.objects.get_or_create(slug="front-banner")
        fb = self.fb
        bi1 = BannerImage(banner_roll=fb,sequence=1,state="published").save()
        bi2 = BannerImage(banner_roll=fb,sequence=2).save()
        bf1 = BannerFlash(banner_roll=fb,sequence=3,state="published",width=100,height=100,flash_ver=10).save()
        bf2 = BannerFlash(banner_roll=fb,sequence=4,width=100,height=100,flash_ver=10).save()

    def tearDown(self):
        BannerRoll.objects.all().delete()
        Banner.objects.all().delete()

    
    def testModelCasting(self):
        fb = self.fb
        self.assertIsNotNone(fb)
 
        #TODO: test number of executions
        banners = fb.banners
        self.assertIsInstance(banners[0], BannerImage)
        self.assertIsInstance(banners[1], BannerFlash)
        self.assertEqual(len(banners),2)

    def testModelNotCasted(self):
        fb = self.fb
        self.assertIsNotNone(fb)

        all = fb.banner_set.all()
        self.assertIsInstance(all[0], Banner)
        self.assertFalse(isinstance(all[0], BannerImage))
        self.assertEqual(len(all),4)
        self.assertEqual(len(BannerImage.objects.all()),2)
        self.assertEqual(len(BannerFlash.objects.all()),2)

        
    def testTemplate(self):
        #TODO
        pass