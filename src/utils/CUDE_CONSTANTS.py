import os
# DEFAULTS
DEFAULT_SEC = "defaults"
HOME = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", '..'))
SRC = os.path.abspath(os.path.join(HOME , "src"))
# DATA
DATA_SEC = "data"
DATA = os.path.abspath(os.path.join(SRC , "data"))
DATASET = os.path.abspath(os.path.join(DATA, "dataset"))
PREPROCESSING = os.path.abspath(os.path.join(DATA , "preprocessing"))
PREPROCESSORS = os.path.abspath(os.path.join(PREPROCESSING , "preprocssors"))
DISRUPTORS = os.path.abspath(os.path.join(PREPROCESSING , "disruptors"))
# DECISION_MAKING
DECISION_MAKING_SEC = "decision_making"
DECISION_MAKING = os.path.abspath(os.path.join(SRC , "decision_making"))
ACTIONS = os.path.abspath(os.path.join(DECISION_MAKING , "actions"))
MECHANISMS = os.path.abspath(os.path.join(DECISION_MAKING , "mechanisms"))
PERFORMANCE_MEASUREMENTS = os.path.abspath(os.path.join(DECISION_MAKING , "performance_measurements"))
# RESULTS
RESULTS_SEC = "results"
RESULTS = os.path.abspath(os.path.join(SRC , "results"))
DUMPS = os.path.abspath(os.path.join(RESULTS , "dump"))
# INI CONFS
LEVEL_1_SECTIONS = [DEFAULT_SEC, DATA_SEC, DECISION_MAKING_SEC, RESULTS_SEC]


