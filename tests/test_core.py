from unittest import TestCase
from src.core import nest, merge, trans


class TestRelocate(TestCase):
    pass


class TestNest(TestCase):
    def test_1(self):
        target = {'sample': 'sample'}
        self.assertEqual(nest(target), [{'sample': 'sample'}])

    def test_2(self):
        target = {'sample.sample': 'sample'}
        self.assertEqual(nest(target), [{'sample': {'sample': 'sample'}}])

    def test_3(self):
        target = {'sample.sample.sample': 'sample'}
        self.assertEqual(nest(target), [{'sample': {'sample': {'sample': 'sample'}}}])

    def test_1_by_3(self):
        target = {'sample_a.sample': 'sample', 'sample_b': 'sample'}
        self.assertEqual(nest(target), [{'sample_a': {'sample': 'sample'}},
                                        {'sample_b': 'sample'}])

    def test_2_by_3(self):
        target = {'sample_a.sample': 'sample', 'sample_b.sample.sample': 'sample'}
        self.assertEqual(nest(target), [{'sample_a': {'sample': 'sample'}},
                                        {'sample_b': {'sample': {'sample': 'sample'}}}])

    def test_3_by_3(self):
        target = {'sample.sample_a.sample': 'sample', 'sample.sample_b.sample': 'sample'}
        self.assertEqual(nest(target), [{'sample': {'sample_a': {'sample': 'sample'}}},
                                        {'sample': {'sample_b': {'sample': 'sample'}}}])


class TestMerge(TestCase):
    def test_string(self):
        base = {'sample_str': 'sample_a'}
        update = {'sample_str': 'sample_b'}
        merge(base, update)
        self.assertEqual(base, {'sample_str': 'sample_b'})

    def test_string_marge(self):
        base = {'sample_str_a': 'sample_a'}
        update = {'sample_str_b': 'sample_b'}
        merge(base, update)
        self.assertEqual(base, {'sample_str_a': 'sample_a', 'sample_str_b': 'sample_b'})

    def test_int(self):
        base = {'sample_int': 1}
        update = {'sample_int': 2}
        merge(base, update)
        self.assertEqual(base, {'sample_int': 2})

    def test_int_marge(self):
        base = {'sample_int_a': 1}
        update = {'sample_int_b': 2}
        merge(base, update)
        self.assertEqual(base, {'sample_int_a': 1, 'sample_int_b': 2})

    def test_inst(self):
        class Sample:
            def __init__(self, name):
                self.name = name

        a = Sample('sample_a')
        b = Sample('sample_b')
        base = {'sample_inst': a}
        update = {'sample_inst': b}
        merge(base, update)
        self.assertEqual(base, {'sample_inst': b})

    def test_inst_merge(self):
        class Sample:
            def __init__(self, name):
                self.name = name

        a = Sample('sample_a')
        b = Sample('sample_b')
        base = {'sample_inst_a': a}
        update = {'sample_inst_b': b}
        merge(base, update)
        self.assertEqual(base, {'sample_inst_a': a, 'sample_inst_b': b})

    def test_dict(self):
        base = {'sample_dict': {'sample_dict_nest_a': 'sample_str_a'}}
        update = {'sample_dict': {'sample_dict_nest_a': 'sample_str_b'}}
        merge(base, update)
        self.assertEqual(base, {'sample_dict': {'sample_dict_nest_a': 'sample_str_b'}})

    def test_dict_merge(self):
        base = {'sample_dict': {'sample_dict_nest_a': 'sample_str_a'}}
        update = {'sample_dict': {'sample_dict_nest_b': 'sample_str_b'}}
        merge(base, update)
        self.assertEqual(base, {
            'sample_dict': {
                'sample_dict_nest_a': 'sample_str_a',
                'sample_dict_nest_b': 'sample_str_b'
            }
        })


class TestTrans(TestCase):
    def test(self):
        base = {'[0]': {'key_01': 'sample_key_01', 'key_02': 'sample_key_02'}}
        self.assertEqual(trans(base), [
            {'key_01': 'sample_key_01', 'key_02': 'sample_key_02'}
        ])

    def test_a(self):
        base = {'[0]': {'key_01': 'sample_key_01_01', 'key_02': 'sample_key_01_02'},
                '[1]': {'key_01': 'sample_key_02_01', 'key_02': 'sample_key_02_02'}}
        self.assertEqual(trans(base), [
            {'key_01': 'sample_key_01_01', 'key_02': 'sample_key_01_02'},
            {'key_01': 'sample_key_02_01', 'key_02': 'sample_key_02_02'}
        ])
