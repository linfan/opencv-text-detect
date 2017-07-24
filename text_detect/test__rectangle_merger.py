from unittest import TestCase

from text_detect.rectangle_merger import RectangleMerger as Merger
from text_detect.rectangle import Rectangle


class TestRectangleMerger(TestCase):
    rect_a = Rectangle.from_2_pos(1, 1, 10, 5)
    rect_b = Rectangle.from_2_pos(11, 1.2, 13, 5.2)
    rect_c = Rectangle.from_2_pos(2, 3, 20, 10)
    merger = Merger()

    def test__merge_rectangle_to_pool(self):
        self.assertTrue(self.merger._is_rectangles_overlapped(self.rect_a, self.rect_c))
        self.assertFalse(self.merger._is_rectangles_overlapped(self.rect_a, self.rect_b))

    def test__merge_2_rectangles(self):
        rect = self.merger._merge_2_rectangles(self.rect_a, self.rect_c)
        expect_rect = Rectangle.from_2_pos(1, 1, 20, 10)
        self.assertEqual(rect, expect_rect, "%s and %s not equal!" % (rect, expect_rect))

    def test__merge_all_rectangles(self):
        rects = [self.rect_a, self.rect_b, self.rect_c]
        merged_rects = self.merger.merge_rectangle_list(rects)
        expect_rects = [Rectangle.from_2_pos(1, 1, 13, 5.2), Rectangle.from_2_pos(2, 3, 20, 10)]
        self.assertListEqual(merged_rects, expect_rects, " ".join([r.__str__() for r in merged_rects]))

