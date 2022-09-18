import unittest
from utils.utils import *

"""
TESTS FOR ALL FUNCTIONALITIES RELATED TO UTILS
"""


class TestIterableStructure(unittest.TestCase):
    def setUp(self) -> None:
        self._iterable_structure = IterableStructure()

    def tearDown(self) -> None:
        pass

    def test_get_list(self):
        self.assertEqual(self._iterable_structure.get_list(), [])
        self._iterable_structure.append(1)
        self._iterable_structure.append(2)
        self.assertEqual(self._iterable_structure.get_list(), [1, 2])

    def test_append(self):
        self.assertEqual(self._iterable_structure.__len__(), 0)
        self._iterable_structure.append(1)
        self.assertEqual(self._iterable_structure[0], 1)
        self.assertEqual(self._iterable_structure.__len__(), 1)
        self._iterable_structure.append(2)
        self.assertEqual(self._iterable_structure[1], 2)
        self.assertEqual(self._iterable_structure.__len__(), 2)
        self._iterable_structure.clear()
        self.assertEqual(self._iterable_structure.__len__(), 0)

    def test_delete(self):
        self.assertEqual(self._iterable_structure.__len__(), 0)
        self._iterable_structure.append(1)
        self._iterable_structure.append(2)
        self.assertEqual(self._iterable_structure.__len__(), 2)
        self._iterable_structure.__delitem__(1)
        self.assertEqual(self._iterable_structure.__len__(), 1)
        self._iterable_structure.__delitem__(0)
        self.assertEqual(self._iterable_structure.__len__(), 0)

    def test_get_item(self):
        self._iterable_structure.append(1)
        self._iterable_structure.append(2)
        self.assertEqual(self._iterable_structure.__getitem__(0), 1)
        self.assertEqual(self._iterable_structure.__getitem__(1), 2)

    def test_set_item(self):
        self._iterable_structure.append(1)
        self._iterable_structure.append(2)
        self.assertEqual(self._iterable_structure.__getitem__(0), 1)
        self.assertEqual(self._iterable_structure.__getitem__(1), 2)
        self._iterable_structure.__setitem__(0, 10)
        self._iterable_structure.__setitem__(1, 20)
        self.assertEqual(self._iterable_structure.__getitem__(0), 10)
        self.assertEqual(self._iterable_structure.__getitem__(1), 20)

    def test_next(self):
        self._iterable_structure.append(10)
        self._iterable_structure.append(20)
        self._iterable_structure.append(30)
        self._iterable_structure.append(40)
        self.assertEqual(self._iterable_structure.__next__(), 20)
        self.assertEqual(self._iterable_structure.__next__(), 30)
        self.assertEqual(self._iterable_structure.__next__(), 40)
        with self.assertRaises(StopIteration) as e:
            self._iterable_structure.__next__()
        self.assertEqual(str(e.exception), "")

    def test_iter(self):
        self._iterable_structure.append(10)
        self._iterable_structure.append(20)
        self._iterable_structure.append(30)
        self._iterable_structure.append(40)
        numbers_iter = self._iterable_structure.__iter__()
        self.assertEqual(numbers_iter.__next__(), 10)
        self.assertEqual(numbers_iter.__next__(), 20)
        self.assertEqual(numbers_iter.__next__(), 30)
        self.assertEqual(numbers_iter.__next__(), 40)
        with self.assertRaises(StopIteration):
            numbers_iter.__next__()
        self._iterable_structure.__delitem__(3)
        self._iterable_structure.__delitem__(2)
        self._iterable_structure.__delitem__(1)
        self._iterable_structure.__delitem__(0)
        self.assertEqual(self._iterable_structure.__len__(), 0)
        self._iterable_structure.append(0)
        self._iterable_structure.append(0)
        self._iterable_structure.append(0)
        self._iterable_structure.append(0)
        for index in range(len(self._iterable_structure)):
            self.assertEqual(self._iterable_structure[index], 0)


class TestSort(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @staticmethod
    def greater(item1, item2):
        return float(item1) >= float(item2)

    @staticmethod
    def smaller(item1, item2):
        return float(item1) < float(item2)

    def test_comb_sort(self):
        listt = [3.80, 7.80, 2.00, 7, 9, 10, 8.70, 4, 80, 23, 9.60, 7.90]
        comb_sort(listt, self.smaller)
        self.assertEqual(listt, [2.00, 3.80, 4, 7, 7.80, 7.90, 8.70, 9, 9.60, 10, 23, 80])
        listt = [3.80, 7.80, 2.00, 7, 9, 10, 8.70, 4, 80, 23, 9.60, 7.90]
        comb_sort(listt, self.greater)
        self.assertEqual(listt, [80, 23, 10, 9.60, 9, 8.70, 7.90, 7.80, 7, 4, 3.80, 2.00])


class TestFilter(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @staticmethod
    def criteria1(item):
        return len(item) > 2

    @staticmethod
    def criteria2(item):
        return isinstance(item, int)

    def test_filter(self):
        listt = ['abc', '', 'da', 'nu', 'okay', 'json', 'csv', 'bin', 'x']
        listt = filter_list(listt, self.criteria1)
        self.assertEqual(listt, ['abc', 'okay', 'json', 'csv', 'bin'])
        listt = [1.90, 7, 8.9, 3, 'abc', 8.90, 2.80, 2, 5, 79, 0.90, '900', 'io']
        listt = filter_list(listt, self.criteria2)
        self.assertEqual(listt, [7, 3, 2, 5, 79])


if __name__ == "__main__":
    unittest.main()
