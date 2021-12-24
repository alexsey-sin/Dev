from django.test import TestCase
from tastypie.cache import SimpleCache


class CacheTestCase(TestCase):
    cache_name = 'resources'

    def test_cache(self):
        simple_cache = SimpleCache(cache_name=self.cache_name)
        simple_cache.set('foo', 'bar', 60)
        simple_cache.set('moof', 'baz', 1)

        self.assertEqual(simple_cache.get('foo'), 'bar')
        self.assertEqual(simple_cache.get('moof'), 'baz')
        self.assertEqual(simple_cache.get(''), None)
