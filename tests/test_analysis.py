import json
import os
import unittest
from pathlib import Path

from numpy import isinf

from cilissa.core import ImageAnalyzer
from cilissa.images import Image, ImagePair
from cilissa.metrics import MSE, PSNR, SSIM


class TestImageAnalysis(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base_path = os.path.dirname(__file__)

        fp = open(Path(cls.base_path, "data", "data.json"))
        cls.metrics_data = json.load(fp)

    def test_metric_mse(self) -> None:
        mse = MSE()

        for m_type in self.metrics_data.values():
            for m in m_type:
                ref_image = Image(Path(self.base_path, m["reference"]))
                mea_image = Image(Path(self.base_path, m["measured"]))
                image_pair = ImagePair(ref_image, mea_image)

                result = mse.analyze(image_pair)

                self.assertAlmostEqual(result, m["metrics"]["mse"], delta=0.1)

    def test_metric_psnr(self) -> None:
        psnr = PSNR()

        for m_type in self.metrics_data.values():
            for m in m_type:
                ref_image = Image(Path(self.base_path, m["reference"]))
                mea_image = Image(Path(self.base_path, m["measured"]))
                image_pair = ImagePair(ref_image, mea_image)

                result = psnr.analyze(image_pair)

                if m["metrics"]["psnr"] is None:
                    self.assertTrue(isinf(result))
                else:
                    self.assertAlmostEqual(result, m["metrics"]["psnr"], delta=0.1)

    def test_metric_ssim(self) -> None:
        ssim = SSIM()

        for m_type in self.metrics_data.values():
            for m in m_type:
                ref_image = Image(Path(self.base_path, m["reference"]))
                mea_image = Image(Path(self.base_path, m["measured"]))
                image_pair = ImagePair(ref_image, mea_image)

                result = ssim.analyze(image_pair)

                self.assertAlmostEqual(result, m["metrics"]["ssim"], delta=0.5)

    def test_image_analyzer(self) -> None:
        mse, psnr, ssim = MSE(), PSNR(), SSIM()
        metrics = [mse, psnr, ssim]
        analyzer = ImageAnalyzer(metrics)

        row = self.metrics_data["jpeg"][0]
        ref_image = Image(Path(self.base_path, row["reference"]))
        mea_image = Image(Path(self.base_path, row["measured"]))
        image_pair = ImagePair(ref_image, mea_image)

        result = analyzer.analyze(image_pair)

        self.assertListEqual(list(result.keys()), [m.get_class_name() for m in metrics])
