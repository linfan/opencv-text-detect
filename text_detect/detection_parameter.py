class DetectionParameter:

    def __init__(self, horizontal_only, threshold_delta, min_area, max_area, min_probability_1, non_max_suppression,
                 min_probability_diff, min_probability_2):
        self.horizontalOnly = horizontal_only
        self.thresholdDelta = threshold_delta
        self.minArea = min_area
        self.maxArea = max_area
        self.minProbability1 = min_probability_1
        self.nonMaxSuppression = non_max_suppression
        self.minProbabilityDiff = min_probability_diff
        self.minProbability2 = min_probability_2
