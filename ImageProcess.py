import cv2
from typing import Optional
from loguru import logger
import numpy as np


class ImageProcess:
    """
    Description: compare similarity of two images
    """

    def __init__(self) -> None:
        ...

    @staticmethod
    def compare_image(
        image_1: str, image_2: str, area: Optional[list] = None, thre: float = 0.01
    ) -> bool:
        if area:
            image_1 = image_1[area[0] : area[1], area[2] : area[3]]
            image_2 = image_2[area[0] : area[1], area[2] : area[3]]
        minimum_commutative_image_diff_threshold = thre
        commutative_image_diff = ImageProcess.get_image_difference(image_1, image_2)
        if commutative_image_diff < minimum_commutative_image_diff_threshold:
            logger.success(
                f"Matched, Diff: {commutative_image_diff}, Thre: {minimum_commutative_image_diff_threshold}"
            )
            return True
        logger.warning(
            f"Unmatched, Diff: {commutative_image_diff}, Thre: {minimum_commutative_image_diff_threshold}"
        )
        return False

    @staticmethod
    def get_image_difference(image_1, image_2) -> int:
        # range (0.0, 1.1)
        first_image_hist = cv2.calcHist([image_1], [0], None, [256], [0, 256])
        second_image_hist = cv2.calcHist([image_2], [0], None, [256], [0, 256])
        # if images are the same, histmatch return 0
        img_hist_diff = cv2.compareHist(
            first_image_hist, second_image_hist, cv2.HISTCMP_BHATTACHARYYA
        )
        # if images are the same, templatematch return 1
        img_template_probability_match = cv2.matchTemplate(
            first_image_hist, second_image_hist, cv2.TM_CCORR_NORMED
        )[0][0]
        img_template_diff = 1 - img_template_probability_match

        # taking only 10% of histogram diff, since it's less accurate than template method
        commutative_image_diff = (img_hist_diff / 10) + img_template_diff
        return commutative_image_diff

    @staticmethod
    def image_compare(image_1, image_2, thre: float = 0.9):
        method = cv2.TM_CCOEFF_NORMED
        temp_matcher = cv2.matchTemplate(image_2, image_1, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(temp_matcher)
        matchedValue = round(min_val, 2)
        if thre < matchedValue:
            logger.success(
                f"Matched, Rate: {matchedValue}, Thre: {thre}"
            )
            return True
        logger.warning(
            f"Unmatched, Rate: {matchedValue}, Thre: {thre}"
        )
        return False
    
    @staticmethod
    def image_compare_by_feature(image_1, image_2, thre: float = 0.9):
        # sift = cv2.SIFT_create()
        orb = cv2.ORB_create()
        # Find keypoints and descriptors
        keypoints1, descriptors1 = orb.detectAndCompute(image_1, None)
        keypoints2, descriptors2 = orb.detectAndCompute(image_2, None)

        # Initialize BFMatcher (Brute Force Matcher)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        # Match descriptors
        try:
            matches = bf.match(descriptors1, descriptors2)
        except:
            logger.error("Image have different size!")
            return False

        # Sort them in ascending order of distance
        matches = sorted(matches, key=lambda x: x.distance)
        # Extract matched keypoints
        matched_keypoints1 = np.array([keypoints1[match.queryIdx].pt for match in matches])
        matched_keypoints2 = np.array([keypoints2[match.trainIdx].pt for match in matches])

        # Calculate Fundamental matrix using RANSAC
        fundamental_matrix, mask = cv2.findFundamentalMat(matched_keypoints1, matched_keypoints2, cv2.FM_RANSAC)
        # Calculate inlier ratio
        inlier_ratio = round(np.sum(mask) / len(matches), 2)
        if thre < inlier_ratio:
            logger.success(
                f"Matched, Rate: {inlier_ratio}, Thre: {thre}"
            )
            return True
        logger.warning(
            f"Unmatched, Rate: {inlier_ratio}, Thre: {thre}"
        )
        return False

    def __repr__(self) -> str:
        return f"Image_compare({self.image_1}, {self.image_2})"

    def __str__(self) -> str:
        return "Compare two images and return the similarity."


if __name__ == "__main__":
    import os

    root = os.path.dirname(__file__)
    img1 = os.path.join(root, "tmp", "Android_Home_b.png")
    img2 = os.path.join(root, "tmp", "Android_Home_d.png")
    img1 = cv2.imread(img1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img2, cv2.IMREAD_GRAYSCALE)
    ImageProcess.image_compare_by_feature(img1, img2)
