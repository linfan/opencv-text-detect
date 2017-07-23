from text_detect.rectangle import Rectangle


class RectangleSelector:

    def _remove_slim_rectangles(self, rectangles):
        return [r for r in rectangles if r.get_width() > r.get_height()]

    def select_fat_and_large_rectangles(self, rectangles):
        rects = self._remove_slim_rectangles(rectangles)
        if len(rects) <= 4:
            return rects
        top_area_rects = sorted(rects, key=lambda r: r.get_area(), reverse=True)[:2]
        top_width_rects = sorted(rects, key=lambda r: r.get_width(), reverse=True)[:4]
        if top_area_rects[0] not in top_width_rects:
            top_width_rects[3] = top_area_rects[0]
        if top_area_rects[1] not in top_width_rects:
            top_width_rects[2] = top_area_rects[1]
        return top_width_rects
