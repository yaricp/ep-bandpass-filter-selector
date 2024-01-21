import os
import sys

from ep_bandpass_filter_selector import PassbandSelector
from eeg_filters import upload as eeg_filters_upload

from settings import (
    LFRL, LFRH, SLR, HFRL, HFRH, SHR, EXTREMUMS, NUMBER_CURVES
)
argv = sys.argv
if len(argv) < 2:
    print("Use main.py filepath")
    exit(0)
print(f"ARGV: {argv}")
filepath = os.path.join(
    os.getcwd(),
    argv[1]
)
if not filepath:
    print("Not works without file with eep data")
    exit(0)
print(f"Datafile path: {filepath}")
(
    fs,
    list_times,
    tick_times,
    list_data
) = eeg_filters_upload.prepare_data(filepath)

data_for_selector = []
for number in NUMBER_CURVES:
    data_for_selector.append(list_data[number])

print(f"tick_times: {tick_times}")
print(f"Data for selector: {len(data_for_selector)}")
print(f"extremums: {EXTREMUMS}")

selector = PassbandSelector(
    curves=data_for_selector,
    tick_times=tick_times,
    fsr=fs,
    max_search_range=EXTREMUMS["max"],
    min_search_range=EXTREMUMS["min"]
)
passband, heatmap = selector.start()

print(f"Passband: {passband}")
print()
print(f"Heatmap: {heatmap}")
