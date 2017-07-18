from lib.rectangle import Rectangle


class RectangleMerger:
    def _is_rectangles_overlapped(self, rect_1, rect_2):
        if rect_1.x2 < rect_2.x1 or rect_1.y2 < rect_2.y1 \
                or rect_1.x1 > rect_2.x2 or rect_1.y1 > rect_2.y2:
            return False
        else:
            return True

    def _merge_2_rectangles(self, rect_1, rect_2):
        return Rectangle.from_2_pos(rect_1.x1 < rect_2.x1 and rect_1.x1 or rect_2.x1,
                                    rect_1.y1 < rect_2.y1 and rect_1.y1 or rect_2.y1,
                                    rect_1.x2 > rect_2.x2 and rect_1.x2 or rect_2.x2,
                                    rect_1.y2 > rect_2.y2 and rect_1.y2 or rect_2.y2)

    def _merge_rectangle_to_pool(self, rect_pool):
        new_pool = []
        has_merge = False
        for rect in rect_pool:
            if len(new_pool) == 0:
                new_pool.append(rect)
                continue
            has_step_merge = False
            for i in range(0, len(new_pool)):
                if self._is_rectangles_overlapped(new_pool[i], rect):
                    new_pool[i] = self._merge_2_rectangles(new_pool[i], rect)
                    has_step_merge = True
                    break
            if not has_step_merge:
                new_pool.append(rect)
            has_merge |= has_step_merge
        return has_merge, new_pool

    def merge_rectangle_list(self, rectangle_list):
        has_merge = True
        while has_merge:
            has_merge = False
            m, rect_pool = self._merge_rectangle_to_pool(rectangle_list)
            has_merge |= m
            rectangle_list = rect_pool
        return rectangle_list
