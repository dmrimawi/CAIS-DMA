import os
# GENERAL
SUCCESS = 0
FAIL = 1
# DEFAULTS
DEFAULT_SEC = "defaults"
HOME = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", '..'))
SRC = os.path.join(HOME , "src")
# DATA
DATA_SEC = "simulator"
DATA = os.path.join(SRC , DATA_SEC)
DATASET = os.path.join(DATA, "dataset")
PREPROCESSING = os.path.join(DATA , "preprocessing")
ADAPTERS = os.path.join(PREPROCESSING , "adapters")
DISRUPTORS = os.path.join(PREPROCESSING , "disruptors")
CSV_FILE_NAME = "objects_colors_dataset.csv"
CSV_COL_CLASS_TITLE = "box"
DISRUPTED_COL_TITLE = "disrupted"
FIELD_WITH_DATA_TITLE = "file_name"
ADAPTER_EXAMPLE_FILE_NAME = "ADAPTER_EXAMPLE"
PUBLISH_ADDRESS = "127.0.0.1"
PUBLISH_PORT = "5556"
# DECISION_MAKING
DECISION_MAKING_SEC = "actuator"
DECISION_MAKING = os.path.join(SRC , DECISION_MAKING_SEC)
ACTIONS = os.path.join(DECISION_MAKING , "actions")
MECHANISMS = os.path.join(DECISION_MAKING , "mechanisms")
PERFORMANCE_MEASUREMENTS = os.path.join(DECISION_MAKING , "performance_measurements")
# RESULTS
RESULTS_SEC = "monitoring"
RESULTS = os.path.join(SRC , RESULTS_SEC)
DUMPS = os.path.join(RESULTS , "dump")
# INI CONFS
INI_FILE_PATH = os.path.join(SRC, "utils", "confs.ini")
LEVEL_1_SECTIONS = [DEFAULT_SEC, DATA_SEC, DECISION_MAKING_SEC, RESULTS_SEC]
DATA_DATASET_PATH_INI = "simulator.dataset.input.path"
ADAPTERS_LIST_INI = 'simulator.preprocessing.adapters.list'
DISRUPTORS_LIST_INI = 'simulator.preprocessing.disruptors.list'
DATASET_FEED_RANDOM_INI = 'simulator.random'
DATA_PATH_INI = 'simulator.path'
DATA_ALL_DATASETS_PATH_INI = 'simulator.dataset.path'
DATA_PREPROCESSING_PATH_INI = 'simulator.preprocessing.path'
DATA_ADAPTERS_PATH_INI = 'simulator.preprocessing.adapters.path'
DATA_DISRUPTORS_PATH_INI = 'simulator.preprocessing.disruptors.path'
RESULTS_DUMPS_PATH_INI = "monitoring.dumps.path"
SPLIT_DATA_VALUE_INI = 'simulator.data_split'


