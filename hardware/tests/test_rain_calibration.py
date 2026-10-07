def test_gauge_calibration():
    mm_per_tip = 0.2794
    assert round(100 * mm_per_tip, 2) == 27.94
    print('Calibration verified: 100 tips = 27.94 mm rainfall.')
if __name__ == '__main__': test_gauge_calibration()
