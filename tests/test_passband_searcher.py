# import pytest
from loguru import logger

from eeg_filters.upload import prepare_data
from ep_bandpass_filter_selector import PassbandSelector
# , export_data


class TestPassbandSelector:
    """
    Class for testing of PassbandSelector methods.
    """

    data_folder_path = "tests/data/"
    data_file_path = "tests/data/test_eeg_data.txt"
    pbs = PassbandSelector(
        curves=[],
        tick_times=[],
        fsr=25,
        max_search_range=(0.01, 0.02),
        min_search_range=(0.03, 0.04),
    )

    def test_get_peak_cvc(self):
        """
        Tests peak variability curves
        """
        self.pbs.tick_times = [1, 2, 3, 4, 5]
        self.pbs.max_search_range = [0, 5]
        self.pbs.min_search_range = [0, 5]
        filtered_curves = [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]
        result = self.pbs.get_peak_cvc(filtered_curves)
        assert result == 0.0

    def test_get_curve_cvc(self):
        """
        Tests calculating of the average integrals.
        """
        self.pbs.tick_times = [1, 2, 3, 4, 5]
        self.pbs.max_search_range = [0, 5]
        self.pbs.min_search_range = [0, 5]
        filtered_curves = [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]
        result = self.pbs.get_curve_cvc(filtered_curves)
        assert result == 0.0

        filtered_curves = [[1, 2, 4, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 3, 5]]
        result = self.pbs.get_curve_cvc(filtered_curves)
        assert round(result, 2) == 1.33

    def test_p2p_coeff_by_base_region(self):
        """
        Tests peak to peak coefficient.
        """
        assert True

    def test_p2p_abs_coeff(self):
        """
        Tests calculating the average difference extrema.
        """
        self.pbs.tick_times = [1, 2, 3, 4, 5]
        self.pbs.max_search_range = [0, 5]
        self.pbs.min_search_range = [0, 5]

        filtered_curves = [[1, 1, 2, 0, 1], [0, 0, -2, 0, 0], [1, 1, -1, 1, 1]]
        result = self.pbs.p2p_abs_coeff(filtered_curves)
        assert result == 2.0

        filtered_curves = [[1, 1, 2, 0, 1], [1, 2, 4, 0, 1], [1, 2, 6, 0, 1]]
        result = self.pbs.p2p_abs_coeff(filtered_curves)
        assert result == 4.0

    def test_get_integral(self):
        """
        Tests calculating of the integrals.
        """
        curve1 = [1, 1, 1]
        curve2 = [1, 1, 1]
        assert self.pbs.get_integral(curve1, curve2) == 0.0

        curve1 = [1, 1, 1]
        curve2 = [1, 2, 1]
        assert self.pbs.get_integral(curve1, curve2) == 1.0

        curve1 = [1, 1, 1]
        curve2 = [1, 2, 2]
        assert self.pbs.get_integral(curve1, curve2) == 1.5

        curve1 = [1, 1, 1]
        curve2 = [1, 2, 3]
        assert self.pbs.get_integral(curve1, curve2) == 2.0

        curve1 = [1, 1, 1]
        curve2 = [1, 0, 1]
        assert self.pbs.get_integral(curve1, curve2) == 1.0

        curve1 = [1, 1, 1]
        curve2 = [1, 0, 0]
        assert self.pbs.get_integral(curve1, curve2) == 1.5

        curve1 = [1, 1, 1]
        curve2 = [1, 0, -1]
        assert self.pbs.get_integral(curve1, curve2) == 2.0

    def test_start(self):
        """
        Tests whole process of selecting filter bandpass.
        """
        # for filename in os.listdir(self.data_folder_path):
        #    filepath = os.path.join(self.data_folder_path, filename)
        extremums = {"min": (0.022, 0.028), "max": (0.016, 0.023)}
        selected_times = ["11:35:47", "11:40:46", "11:45:37", "11:49:36", "11:54:55"]
        (sample_rate, list_times, list_ticks, list_out) = prepare_data(
            self.data_file_path
        )

        selected_curves = []
        index = 0
        list_indexes = []
        for time_l in list_times:
            if time_l in selected_times:
                logger.info(f"time_l: {time_l}")
                list_indexes.append(index)
            index += 1
        for idx in list_indexes:
            # logger.info(f"len list_out[idx]: {len(list_out[idx])}")
            selected_curves.append(list_out[idx])

        # logger.info(f"len selected_curves: {len(selected_curves)}")
        # logger.info(f"selected_curves[0][0]: {selected_curves[0][0]}")
        self.pbs.curves = selected_curves
        self.pbs.tick_times = list_ticks
        self.pbs.frequency_sample_rate = sample_rate
        self.pbs.max_search_range = extremums["max"]
        self.pbs.min_search_range = extremums["min"]
        self.pbs.filter_low_limit_range = 5, 20
        self.pbs.step_low_filter = 5
        self.pbs.filter_high_limit_range = 100, 300
        self.pbs.step_high_filter = 50

        result = self.pbs.start()

        assert result[0] == (20, 200)
