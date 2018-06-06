import re
from typing import NamedTuple, Optional, List, Iterator, Callable

import numpy as np
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot

from lexos.helpers.definitions import get_words_with_right_boundary, \
    get_single_word_count_in_text
from lexos.models.base_model import BaseModel
from lexos.models.filemanager_model import FileManagerModel
from lexos.models.matrix_model import FileIDContentMap
from lexos.receivers.rolling_windows_receiver import RWAFrontEndOptions, \
    RollingWindowsReceiver, WindowUnitType, RWATokenType, RWARatioTokenOptions,\
    RWAAverageTokenOptions, RWAWindowOptions
from lexos.models.rolling_windows_model import RollingWindowsModel, \
    RWATestOptions


# --------------------test by ratio count-----------------------------------
test_option_one = RWATestOptions(file_id_content_map=
                                 {0: "ha ha ha ha la ta ha",
                                  2: "la la ta ta da da ha",
                                  3: "ta da ha"
                                  },
                                 rolling_windows_options=RWAFrontEndOptions
                                 (ratio_token_options=RWARatioTokenOptions
                                  (token_type=RWATokenType("string"),
                                   numerator_token="ta",
                                   denominator_token="ha"),
                                  average_token_options=RWAAverageTokenOptions
                                  (token_type=RWATokenType(None), tokens=
                                   List[None]), passage_file_id=1,
                                  window_options=RWAWindowOptions
                                  (window_size=3, window_unit=
                                   WindowUnitType("letter")), milestone=None))
