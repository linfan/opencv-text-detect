from unittest import TestCase

from lib.rectangle_merger import RectangleMerger as Merger
from lib.rectangle import Rectangle


class TestRectangleMerger(TestCase):
    rect_a = Rectangle(1, 1, 3, 2)
    rect_b = Rectangle(2, 2, 3, 2)
    rect_c = Rectangle(4, 6, 3, 2)
    merger = Merger()

    def test_merge_rectangle_to_pool(self):
        self.assertTrue(self.merger._is_rectangles_overlapped(self.rect_a, self.rect_b))
        self.assertFalse(self.merger._is_rectangles_overlapped(self.rect_a, self.rect_c))

    def test_merge_2_rectangles(self):
        rect = self.merger._merge_2_rectangles(self.rect_a, self.rect_b)
        expect_rect = Rectangle(1, 1, 4, 3)
        self.assertEqual(rect, expect_rect, "%s and %s not equal!" % (rect, expect_rect))

    def test_merge_all_rectangles(self):
        rects = [self.rect_a, self.rect_b, self.rect_c]
        merged_rects = self.merger.merge_rectangle_list(rects)
        expect_rects = [Rectangle(1, 1, 4, 3), Rectangle(4, 6, 3, 2)]
        self.assertListEqual(merged_rects, expect_rects, " ".join([r.__str__() for r in merged_rects]))

