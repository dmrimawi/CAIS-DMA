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
HUMAN = "Human"
AUTONOMOUS = "Autonomous"
# STEADY_DISRUPTED_FIXED_ITERATIONS = (46, 82, 83)
STEADY_DISRUPTED_FIXED_ITERATIONS = (50, 100, 100)
FIX_AFTER_RECOVERED = True
CSV_FILE_NAME = "objects_colors_dataset.csv"
CSV_HUMAN_ACTION = "HumanAction.csv"
CSV_AUTONOMOUS_ACTION = "AutonomousAction.csv"
CSV_FINAL_DUMP = "actions_log.csv"
CSV_SMOOTHING_FACTOR_HEADERS = ["HumRed", "HumGreen", "HumBlue", "EstARMCO2", "EstARMTime", "EstHumCO2", "EstHumTime"]
CSV_FINAL_DUMP_HEADERS = ['ObjectID', 'Action', 'WithSupport', 'Target', 'HumanInteractions', 'CO2', 'Time', 'Missclassification', \
                          'PredictProb', 'Max', 'Min', 'MaxDiff', 'MinDiff', 'ObjectType'] + CSV_SMOOTHING_FACTOR_HEADERS
CSV_ACR_DUMP_FIELD_NAME = "ACR"
DISRUPTED_STATE_INDEX = 2
STATES_NAMES = ["None", "Steady", "Disrupted", "Final"]
CSV_COL_CLASS_TITLE = "box"
CSV_COL_ID = "id"
CSV_COL_ACTION_CO2 = "CO2"
CSV_COL_ACTION_TIME = "TIME"
CSV_COL_COLOR = 'color'
DISRUPTED_COL_TITLE = "disrupted"
FIELD_WITH_DATA_TITLE = "file_name"
ADAPTER_EXAMPLE_FILE_NAME = "ADAPTER_EXAMPLE"
PUBLISH_ADDRESS = "127.0.0.1"
SUBSCRIBE_ADDRESS = "localhost"
PUBLISH_PORT = "5556"
SUBSCRIBE_PORT = "5558"
SUBSCRIBE_UNCLS_PORT = "5559"
TEACHING_PORT = "5557"
DARKNESS_RATIO = -55
TIME_FRAME_SIZE = 5
ACR_DIAGRAM_FILENAME = "acr_diagram.pdf"
CLEAN_DATASET_FILES = True
SHOW_PLOT_DIAGRAM = True
VALUE_OF_DESIRED_TRUST_LEVEL = 0.45
# DECISION_MAKING
DECISION_MAKING_SEC = "actuator"
DECISION_MAKING = os.path.join(SRC , DECISION_MAKING_SEC)
ACTIONS = os.path.join(DECISION_MAKING , "actions")
MECHANISMS = os.path.join(DECISION_MAKING , "mechanisms")
PERFORMANCE_MEASUREMENTS = os.path.join(DECISION_MAKING , "performance_measurements")
INTERNAL_MECHANISM = "Internal"
SELECTED_MECHANISM = "Internal" # GRGame, GROpt, or Internal
SMOOTHING_CONSTANT = 0.5
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


