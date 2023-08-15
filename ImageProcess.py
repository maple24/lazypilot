import cv2
from typing import Optional
from loguru import logger


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

    def __repr__(self) -> str:
        return f"Image_compare({self.image_1}, {self.image_2})"

    def __str__(self) -> str:
        return "Compare two images and return the similarity."


if __name__ == "__main__":
    import os

    root = os.path.dirname(__file__)
    img1 = os.path.join(root, "tmp", "3.png")
    img2 = os.path.join(root, "tmp", "3_c.png")
    img1 = cv2.imread(img1, 1)
    img2 = cv2.imread(img2, 1)
    ImageProcess.compare_image(img1, img2)
