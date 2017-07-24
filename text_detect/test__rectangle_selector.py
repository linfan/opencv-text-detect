from unittest import TestCase

from text_detect.rectangle_selector import RectangleSelector
from text_detect.rectangle import Rectangle


class TestRectangleSelector(TestCase):
    selector = RectangleSelector()
    rects = [Rectangle(0, 0, 6, 9, 0),
             Rectangle(0, 0, 4, 3, 1),
             Rectangle(0, 0, 9, 1, 0),
             Rectangle(0, 0, 1, 9, 1),
             Rectangle(0, 0, 5, 4, 0),
             Rectangle(0, 0, 8, 2, 0),
             Rectangle(0, 0, 1, 9, 3),
             Rectangle(0, 0, 7, 2, 0),
             Rectangle(0, 0, 6, 5, 2),
             Rectangle(0, 0, 6, 2, 0),
             Rectangle(0, 0, 3, 2, 3)]

    def test__select_fat_and_large_rectangles(self):
        top_rects = self.selector.select_fat_and_large_rectangles(self.rects)
        self.assertEquals(top_rects[0], Rectangle(0, 0, 9, 1), "index %d should not be %s" % (0, top_rects[0]))
        self.assertEquals(top_rects[1], Rectangle(0, 0, 8, 2), "index %d should not be %s" % (1, top_rects[1]))
        self.assertEquals(top_rects[2], Rectangle(0, 0, 5, 4), "index %d should not be %s" % (2, top_rects[2]))
        self.assertEquals(top_rects[3], Rectangle(0, 0, 6, 5), "index %d should not be %s" % (3, top_rects[3]))

    def test__select_most_merged_rectangles(self):
        top_rects = self.selector.select_according_to_merged_times(self.rects)
        self.assertEquals(top_rects[0], Rectangle(0, 0, 3, 2), "index %d should not be %s" % (0, top_rects[0]))
        self.assertEquals(top_rects[1], Rectangle(0, 0, 6, 5), "index %d should not be %s" % (1, top_rects[1]))
        self.assertEquals(top_rects[2], Rectangle(0, 0, 4, 3), "index %d should not be %s" % (2, top_rects[2]))
