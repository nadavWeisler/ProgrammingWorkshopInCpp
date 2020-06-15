#!/usr/bin/env python3
################################################################################
#                                                                              #
#                   Written by Ariel Terkeltoub, June 2020.                    #
#             Song recommendation of the day: "The Wall" by Kansas             #
#                    So Long, and Thanks for All the Fish.                     #
#                                                                              #
################################################################################
import numpy as np
import sys
import subprocess as sp
import os, shutil
import tqdm
import itertools
import difflib

def _supports_color():
    """
    Returns True if the running system's terminal supports color, and False
    otherwise.
    """
    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or
                                                  'ANSICON' in os.environ)
    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    return supported_platform and is_a_tty

SUPPORTS_COLOR = _supports_color()

CRUCIAL_DATA_FILENAME = "crucial_data"

TESTS_SOURCE = "_tests.cpp"
TESTS_BIN = ["./" + os.path.splitext(TESTS_SOURCE)[0]]

HEADERS = ["Matrix.h", "Activation.h", "Dense.h", "MlpNetwork.h", "Digit.h"]
SOURCES = ["Matrix.cpp", "Activation.cpp", "Dense.cpp", "MlpNetwork.cpp"]

CXX = "g++"
CXXFLAGS = ["-std=c++17", "-Wall", "-Wextra", "-Wvla", "-lm", "-o", TESTS_BIN[0]]
FAST = False

PERSIST = False
PERSIST_USED = ""

USE_VALGRIND = False # Don't change this! To use Valgrind, pass "--valgrind" in the command-line
USE_VALGRIND_EXTRA = False # Whether to run under Valgrind early exits (bad matrix operations, etc.) as well
VALGRIND_LOGFILE = "valgrind.log"
VALGRIND_BIN = "valgrind"
VALGRIND_LOGFILE_INFO = f"""The Valgrind log can also be found in \"{VALGRIND_LOGFILE}\".\n"""

EXPECTED_RESULTS_FILE = "expected"
ACTUAL_RESULTS_FILE = "actual"
STDOUT_DUMP_FILE = "actual_stdout"
STDERR_DUMP_FILE = "actual_stderr"
DUMP_FILES_INFO = f"The expected matrix has been dumped textually into the file \"{EXPECTED_RESULTS_FILE}\", and the actual matrix into \"{ACTUAL_RESULTS_FILE}\". " + \
                   "These can be viewed as text and loaded in Python with np.loadtxt().\n"
DIGIT_DUMP_FILES_INFO = f"The expected (school) result can be found in the file \"{EXPECTED_RESULTS_FILE}\", and the actual result in \"{ACTUAL_RESULTS_FILE}\".\n"
STDERR_FILE_INFO = f"Standard error has been dumped into the file \"{STDERR_DUMP_FILE}\".\n"
STDIO_FILES_INFO = f"Standard output has been dumped into the file \"{STDOUT_DUMP_FILE}\"; Standard error was dumped into \"{STDERR_DUMP_FILE}\".\n"

INP_FILE = "inp"
INP_FILE_INFO = f"The matrix used for the test has been dumped textually into the file \"{INP_FILE}\". It can be viewed as text and loaded in Python with np.loadtxt().\n"
INP_FILE_SHORT_INFO = f"The matrix used for the test has been dumped textually into the file \"{INP_FILE}\".\n"

def title(text):
    return ("\033[1m" if SUPPORTS_COLOR else "") + f"{'=' * 5} {text} {'=' * 5}\n" + ("\033[0m" if SUPPORTS_COLOR else "")

def red(text, bold = False):
    return f"""\033[31{";1" if bold else ""}m{text}\033[0m""" if SUPPORTS_COLOR else text

def green(text, bold = False):
    return f"""\033[32{";1" if bold else ""}m{text}\033[0m""" if SUPPORTS_COLOR else text

def yellow(text, bold = False):
    return f"""\033[33{";1" if bold else ""}m{text}\033[0m""" if SUPPORTS_COLOR else text

def TEST_FAILED(test_name):
    global PERSIST_USED
    sys.stderr.flush()
    fail_msg = f"Test \"{test_name}\" failed."
    persist_msg = " Persisting tests.\n" if PERSIST else ""
    sys.stdout.write(red(f"""{fail_msg}{persist_msg}\n"""))
    if not PERSIST:
        sys.exit(1)
    PERSIST_USED += fail_msg + '\n'

def TEST_PASSED(test_name):
    sys.stderr.flush()
    sys.stdout.flush()
    sys.stdout.write(green(f"""Test \"{test_name}\" passed.{" No memory problems detected by Valgrind." if USE_VALGRIND else ""}\n"""))

def decode_bytes(s):
    return bytes.decode(s) if s else ""

class TestsIntegrity:
    TESTS_DIRS = ["model", "mnist_data", "mnist_school_results"]

    TESTS_FILES = ["_tests.cpp", "crucial_data", "model/w1", "model/w2", "model/w3", "model/w4", "model/b1", "model/b2", "model/b3", "model/b4",
    "mnist_data/8707", "mnist_data/6265", "mnist_data/1984", "mnist_data/2861", "mnist_data/5986", "mnist_data/8400", "mnist_data/2020", "mnist_data/7608", "mnist_data/6111", "mnist_data/6166", "mnist_data/3457", "mnist_data/8635", "mnist_data/9269", "mnist_data/8284", "mnist_data/7764", "mnist_data/4769", "mnist_data/1925", "mnist_data/8436", "mnist_data/1686", "mnist_data/4644", "mnist_data/729", "mnist_data/1745", "mnist_data/1988", "mnist_data/1465", "mnist_data/1123", "mnist_data/475", "mnist_data/2566", "mnist_data/663", "mnist_data/4424", "mnist_data/7880", "mnist_data/1161", "mnist_data/5927", "mnist_data/2971", "mnist_data/3059", "mnist_data/3131", "mnist_data/8283", "mnist_data/8864", "mnist_data/9075", "mnist_data/79", "mnist_data/8881", "mnist_data/6455", "mnist_data/2035", "mnist_data/4342", "mnist_data/2675", "mnist_data/7055", "mnist_data/4602", "mnist_data/6736", "mnist_data/880", "mnist_data/3282", "mnist_data/5911", "mnist_data/2763", "mnist_data/7535", "mnist_data/9229", "mnist_data/6725", "mnist_data/6021", "mnist_data/1864", "mnist_data/7300", "mnist_data/6016", "mnist_data/4165", "mnist_data/1046", "mnist_data/3396", "mnist_data/2156", "mnist_data/6630", "mnist_data/5405", "mnist_data/5101", "mnist_data/8157", "mnist_data/5913", "mnist_data/8291", "mnist_data/8681", "mnist_data/127", "mnist_data/5840", "mnist_data/5896", "mnist_data/8700", "mnist_data/7905", "mnist_data/7639", "mnist_data/7331", "mnist_data/1949", "mnist_data/1909", "mnist_data/1139", "mnist_data/9495", "mnist_data/8596", "mnist_data/3410", "mnist_data/4762", "mnist_data/3752", "mnist_data/7044", "mnist_data/634", "mnist_data/4674", "mnist_data/5510", "mnist_data/4975", "mnist_data/1720", "mnist_data/9652", "mnist_data/5558", "mnist_data/4075", "mnist_data/284", "mnist_data/8841", "mnist_data/4115", "mnist_data/1643", "mnist_data/2185", "mnist_data/9109", "mnist_data/7948", "mnist_data/408", "mnist_data/3818", "mnist_data/1508", "mnist_data/715", "mnist_data/8938", "mnist_data/4496", "mnist_data/382", "mnist_data/9459", "mnist_data/3979", "mnist_data/1901", "mnist_data/7791", "mnist_data/3097", "mnist_data/9282", "mnist_data/2827", "mnist_data/4066", "mnist_data/4770", "mnist_data/5934", "mnist_data/2182", "mnist_data/8785", "mnist_data/5421", "mnist_data/6444", "mnist_data/8303", "mnist_data/4106", "mnist_data/6068", "mnist_data/5402", "mnist_data/4733", "mnist_data/8452", "mnist_data/4607", "mnist_data/2877", "mnist_data/8458", "mnist_data/1372", "mnist_data/9468", "mnist_data/5052", "mnist_data/4266", "mnist_data/3176", "mnist_data/1084", "mnist_data/2726", "mnist_data/7062", "mnist_data/7043", "mnist_data/500", "mnist_data/4221", "mnist_data/3391", "mnist_data/8962", "mnist_data/1143", "mnist_data/7722", "mnist_data/8912", "mnist_data/7112", "mnist_data/582", "mnist_data/3949", "mnist_data/430", "mnist_data/6994", "mnist_data/2908", "mnist_data/5181", "mnist_data/9", "mnist_data/1907", "mnist_data/7205", "mnist_data/113", "mnist_data/6686", "mnist_data/2278", "mnist_data/2251", "mnist_data/3429", "mnist_data/2191", "mnist_data/8416", "mnist_data/503", "mnist_data/3104", "mnist_data/1499", "mnist_data/6989", "mnist_data/1489", "mnist_data/7389", "mnist_data/3075", "mnist_data/8117", "mnist_data/9765", "mnist_data/7915", "mnist_data/750", "mnist_data/9402", "mnist_data/940", "mnist_data/4685", "mnist_data/8519", "mnist_data/2995", "mnist_data/2139", "mnist_data/5716", "mnist_data/7469", "mnist_data/6375", "mnist_data/4008", "mnist_data/8859", "mnist_data/8391", "mnist_data/7073", "mnist_data/7879", "mnist_data/1131", "mnist_data/7999", "mnist_data/6424", "mnist_data/9266", "mnist_data/7185", "mnist_data/774", "mnist_data/4887", "mnist_data/6823", "mnist_data/5663", "mnist_data/9520", "mnist_data/6733", "mnist_data/1807", "mnist_data/4699", "mnist_data/8990", "mnist_data/3518", "mnist_data/4575", "mnist_data/8822", "mnist_data/7547", "mnist_data/3063", "mnist_data/7454", "mnist_data/1991", "mnist_data/4318", "mnist_data/6130", "mnist_data/9677", "mnist_data/3080", "mnist_data/5089", "mnist_data/9042", "mnist_data/2418", "mnist_data/6851", "mnist_data/5296", "mnist_data/9595", "mnist_data/1077", "mnist_data/8604", "mnist_data/4748", "mnist_data/5636", "mnist_data/9712", "mnist_data/1753", "mnist_data/8829", "mnist_data/3274", "mnist_data/8425", "mnist_data/6933", "mnist_data/3439", "mnist_data/8439", "mnist_data/5707", "mnist_data/5677", "mnist_data/385", "mnist_data/9371", "mnist_data/9223", "mnist_data/5285", "mnist_data/1524", "mnist_data/2244", "mnist_data/2701", "mnist_data/9481", "mnist_data/375", "mnist_data/3540", "mnist_data/9438", "mnist_data/8200", "mnist_data/100", "mnist_data/7515", "mnist_data/9090", "mnist_data/5397", "mnist_data/6523", "mnist_data/136", "mnist_data/8978", "mnist_data/7343", "mnist_data/1865", "mnist_data/209", "mnist_data/2392", "mnist_data/6341", "mnist_data/5789", "mnist_data/7485", "mnist_data/7086", "mnist_data/272", "mnist_data/5371", "mnist_data/3470", "mnist_data/865", "mnist_data/7774", "mnist_data/4724", "mnist_data/302", "mnist_data/8273", "mnist_data/2452", "mnist_data/6582", "mnist_data/2003", "mnist_data/1284", "mnist_data/3432", "mnist_data/5034", "mnist_data/5186", "mnist_data/2537", "mnist_data/9494", "mnist_data/5816", "mnist_data/5168", "mnist_data/337", "mnist_data/9251", "mnist_data/4236", "mnist_data/1594", "mnist_data/212", "mnist_data/6609", "mnist_data/8834", "mnist_data/1375", "mnist_data/7835", "mnist_data/3483", "mnist_data/198", "mnist_data/8225", "mnist_data/9329", "mnist_data/5772", "mnist_data/4225", "mnist_data/9188", "mnist_data/3841", "mnist_data/9626", "mnist_data/6283", "mnist_data/6409", "mnist_data/3345", "mnist_data/6631", "mnist_data/7022", "mnist_data/4708", "mnist_data/6354", "mnist_data/6153", "mnist_data/1", "mnist_data/6908", "mnist_data/2259", "mnist_data/3191", "mnist_data/5979", "mnist_data/6335", "mnist_data/8948", "mnist_data/1794", "mnist_data/8007", "mnist_data/7641", "mnist_data/7967", "mnist_data/3461", "mnist_data/4015", "mnist_data/9761", "mnist_data/5796", "mnist_data/9839", "mnist_data/2823", "mnist_data/8712", "mnist_data/1393", "mnist_data/7768", "mnist_data/4604", "mnist_data/9835", "mnist_data/9702", "mnist_data/6648", "mnist_data/6758", "mnist_data/2503", "mnist_data/6643", "mnist_data/2811", "mnist_data/7585", "mnist_data/2742", "mnist_data/7232", "mnist_data/4791", "mnist_data/1804", "mnist_data/5064", "mnist_data/6865", "mnist_data/1444", "mnist_data/5980", "mnist_data/9896", "mnist_data/5372", "mnist_data/9857", "mnist_data/6112", "mnist_data/2466", "mnist_data/5537", "mnist_data/1664", "mnist_data/6787", "mnist_data/3622", "mnist_data/2985", "mnist_data/809", "mnist_data/7156", "mnist_data/1033", "mnist_data/4650", "mnist_data/1791", "mnist_data/1266", "mnist_data/4917", "mnist_data/9826", "mnist_data/8633", "mnist_data/8549", "mnist_data/7089", "mnist_data/1637", "mnist_data/1542", "mnist_data/9889", "mnist_data/2821", "mnist_data/7128", "mnist_data/6978", "mnist_data/9663", "mnist_data/4750", "mnist_data/5736", "mnist_data/2598", "mnist_data/7795", "mnist_data/283", "mnist_data/5640", "mnist_data/2202", "mnist_data/9584", "mnist_data/8875", "mnist_data/1765", "mnist_data/7462", "mnist_data/6919", "mnist_data/9004", "mnist_data/7868", "mnist_data/8126", "mnist_data/3140", "mnist_data/6036", "mnist_data/8156", "mnist_data/1644", "mnist_data/6907", "mnist_data/6397", "mnist_data/7685", "mnist_data/4939", "mnist_data/8683", "mnist_data/456", "mnist_data/7200", "mnist_data/3666", "mnist_data/618", "mnist_data/1556", "mnist_data/3035", "mnist_data/7014", "mnist_data/8833", "mnist_data/2247", "mnist_data/3311", "mnist_data/8211", "mnist_data/2231", "mnist_data/769", "mnist_data/115", "mnist_data/4386", "mnist_data/806", "mnist_data/9756", "mnist_data/2161", "mnist_data/6864", "mnist_data/260", "mnist_data/223", "mnist_data/1076", "mnist_data/4536", "mnist_data/2470", "mnist_data/9727", "mnist_data/2629", "mnist_data/7293", "mnist_data/7961", "mnist_data/112", "mnist_data/2372", "mnist_data/7366", "mnist_data/6004", "mnist_data/6184", "mnist_data/6050", "mnist_data/6277", "mnist_data/4581", "mnist_data/7632", "mnist_data/8290", "mnist_data/3639", "mnist_data/42", "mnist_data/6724", "mnist_data/8316", "mnist_data/288", "mnist_data/5452", "mnist_data/3567", "mnist_data/5752", "mnist_data/7243", "mnist_data/2079", "mnist_data/5948", "mnist_data/8698", "mnist_data/6122", "mnist_data/8205", "mnist_data/998", "mnist_data/2677", "mnist_data/5281", "mnist_data/1048", "mnist_data/1627", "mnist_data/3170", "mnist_data/6800", "mnist_data/8492", "mnist_data/2377", "mnist_data/6656", "mnist_data/7015", "mnist_data/405", "mnist_data/1623", "mnist_data/6161", "mnist_data/3239", "mnist_data/3155", "mnist_data/5852", "mnist_data/184", "mnist_data/2093", "mnist_data/2580", "mnist_data/5652", "mnist_data/9345", "mnist_data/319", "mnist_data/3411", "mnist_data/7741", "mnist_data/4565", "mnist_data/401", "mnist_data/8248", "mnist_data/7646", "mnist_data/4088", "mnist_data/4451", "mnist_data/4295", "mnist_data/2272", "mnist_data/7852", "mnist_data/6562", "mnist_data/4255", "mnist_data/8234", "mnist_data/7593", "mnist_data/7766", "mnist_data/6154", "mnist_data/4404", "mnist_data/4877", "mnist_data/2761", "mnist_data/34", "mnist_data/8984", "mnist_data/9244", "mnist_data/7114", "mnist_data/5570", "mnist_data/4147", "mnist_data/7777", "mnist_data/7012", "mnist_data/5868", "mnist_data/9646", "mnist_data/6922", "mnist_data/6436", "mnist_data/4849", "mnist_data/4713", "mnist_data/1343", "mnist_data/9005", "mnist_data/1502", "mnist_data/488", "mnist_data/93", "mnist_data/4371", "mnist_data/8873", "mnist_data/4334", "mnist_data/565", "mnist_data/8691", "mnist_data/4053", "mnist_data/9185", "mnist_data/5811", "mnist_data/8774", "mnist_data/1707", "mnist_data/7439", "mnist_data/2581", "mnist_data/814", "mnist_data/1927", "mnist_data/1783", "mnist_data/3660", "mnist_data/2523", "mnist_data/4530", "mnist_data/2718", "mnist_data/2344", "mnist_data/4355", "mnist_data/7058", "mnist_data/2276", "mnist_data/3242", "mnist_data/2619", "mnist_data/2526", "mnist_data/7460", "mnist_data/1338", "mnist_data/4852", "mnist_data/3886", "mnist_data/2772", "mnist_data/3933", "mnist_data/5065", "mnist_data/2904", "mnist_data/8790", "mnist_data/3509", "mnist_data/3440", "mnist_data/3265", "mnist_data/6794", "mnist_data/4546", "mnist_data/3355", "mnist_data/398", "mnist_data/8194", "mnist_data/5808", "mnist_data/5634", "mnist_data/1478", "mnist_data/3992", "mnist_data/9053", "mnist_data/8341", "mnist_data/1965", "mnist_data/5712", "mnist_data/7562", "mnist_data/2490", "mnist_data/6774", "mnist_data/2012", "mnist_data/1599", "mnist_data/6777", "mnist_data/3375", "mnist_data/3", "mnist_data/5246", "mnist_data/6594", "mnist_data/7732", "mnist_data/4608", "mnist_data/1843", "mnist_data/2108", "mnist_data/7528", "mnist_data/4719", "mnist_data/2144", "mnist_data/2973", "mnist_data/1235", "mnist_data/5995", "mnist_data/6092", "mnist_data/772", "mnist_data/8237", "mnist_data/3425", "mnist_data/4092", "mnist_data/975", "mnist_data/9129", "mnist_data/5291", "mnist_data/3043", "mnist_data/8308", "mnist_data/9858", "mnist_data/8497", "mnist_data/2068", "mnist_data/5514", "mnist_data/8472", "mnist_data/6451", "mnist_data/6937", "mnist_data/2856", "mnist_data/7986", "mnist_data/7931", "mnist_data/6946", "mnist_data/5892", "mnist_data/1722", "mnist_data/5375", "mnist_data/9051", "mnist_data/818", "mnist_data/9418", "mnist_data/2209", "mnist_data/7599", "mnist_data/942", "mnist_data/2431", "mnist_data/6776", "mnist_data/6198", "mnist_data/9056", "mnist_data/8279", "mnist_data/515", "mnist_data/3462", "mnist_data/1759", "mnist_data/3792", "mnist_data/5380", "mnist_data/525", "mnist_data/2733", "mnist_data/9504", "mnist_data/8672", "mnist_data/1947", "mnist_data/4408", "mnist_data/3027", "mnist_data/5658", "mnist_data/8769", "mnist_data/4228", "mnist_data/2456", "mnist_data/5209", "mnist_data/3340", "mnist_data/8918", "mnist_data/6139", "mnist_data/959", "mnist_data/4817", "mnist_data/2867", "mnist_data/9043", "mnist_data/9579", "mnist_data/7688", "mnist_data/796", "mnist_data/4379", "mnist_data/6844", "mnist_data/4406", "mnist_data/6786", "mnist_data/8583", "mnist_data/4459", "mnist_data/3839", "mnist_data/4979", "mnist_data/7104", "mnist_data/950", "mnist_data/6137", "mnist_data/8680", "mnist_data/7160", "mnist_data/426", "mnist_data/9853", "mnist_data/7695", "mnist_data/6232", "mnist_data/5674", "mnist_data/303", "mnist_data/2223", "mnist_data/3768", "mnist_data/6519", "mnist_data/6799", "mnist_data/7480", "mnist_data/2384", "mnist_data/9787", "mnist_data/7761", "mnist_data/5023", "mnist_data/7504", "mnist_data/9215", "mnist_data/5430", "mnist_data/861", "mnist_data/2498", "mnist_data/1292", "mnist_data/6598", "mnist_data/1135", "mnist_data/7827", "mnist_data/6668", "mnist_data/279", "mnist_data/3266", "mnist_data/8376", "mnist_data/501", "mnist_data/4012", "mnist_data/3107", "mnist_data/6678", "mnist_data/7792", "mnist_data/7834", "mnist_data/5660", "mnist_data/9537", "mnist_data/9320", "mnist_data/5382", "mnist_data/706", "mnist_data/4309", "mnist_data/5575", "mnist_data/7326", "mnist_data/9378", "mnist_data/4825", "mnist_data/8640", "mnist_data/1186", "mnist_data/3968", "mnist_data/528", "mnist_data/7057", "mnist_data/4717", "mnist_data/9180", "mnist_data/7252", "mnist_data/5206", "mnist_data/4525", "mnist_data/1422", "mnist_data/2103", "mnist_data/7081", "mnist_data/2095", "mnist_data/2282", "mnist_data/2340", "mnist_data/7796", "mnist_data/9083", "mnist_data/4081", "mnist_data/9779", "mnist_data/2266", "mnist_data/6817", "mnist_data/7119", "mnist_data/9995", "mnist_data/1293", "mnist_data/5814", "mnist_data/5545", "mnist_data/3475", "mnist_data/9388", "mnist_data/4729", "mnist_data/3955", "mnist_data/2884", "mnist_data/59", "mnist_data/8396", "mnist_data/5618", "mnist_data/7475", "mnist_data/5804", "mnist_data/6932", "mnist_data/208", "mnist_data/3998", "mnist_data/376", "mnist_data/4002", "mnist_data/4052", "mnist_data/7042", "mnist_data/9845", "mnist_data/1326", "mnist_data/8362", "mnist_data/2578", "mnist_data/5368", "mnist_data/5032", "mnist_data/5645", "mnist_data/9136", "mnist_data/9367", "mnist_data/1717", "mnist_data/2083", "mnist_data/1045", "mnist_data/7351", "mnist_data/4677", "mnist_data/6911", "mnist_data/4449", "mnist_data/9983", "mnist_data/4068", "mnist_data/2085", "mnist_data/8053", "mnist_data/7337", "mnist_data/3195", "mnist_data/5072", "mnist_data/133", "mnist_data/3032", "mnist_data/696", "mnist_data/4658", "mnist_data/7798", "mnist_data/4113", "mnist_data/7142", "mnist_data/7654", "mnist_data/6863", "mnist_data/5311", "mnist_data/3761", "mnist_data/1244", "mnist_data/2422", "mnist_data/1912", "mnist_data/8172", "mnist_data/778", "mnist_data/7023", "mnist_data/3034", "mnist_data/7725", "mnist_data/8340", "mnist_data/4985", "mnist_data/6526", "mnist_data/9001", "mnist_data/162", "mnist_data/4411", "mnist_data/7249", "mnist_data/8056", "mnist_data/1877", "mnist_data/888", "mnist_data/2825", "mnist_data/4790", "mnist_data/8275", "mnist_data/5549", "mnist_data/2228", "mnist_data/4400", "mnist_data/8358", "mnist_data/9946", "mnist_data/5297", "mnist_data/8064", "mnist_data/1026", "mnist_data/5006", "mnist_data/8979", "mnist_data/1963", "mnist_data/6351", "mnist_data/7423", "mnist_data/9785", "mnist_data/8133", "mnist_data/3599", "mnist_data/8003", "mnist_data/4967", "mnist_data/9691", "mnist_data/1893", "mnist_data/4211", "mnist_data/7495", "mnist_data/7194", "mnist_data/5655", "mnist_data/4191", "mnist_data/756", "mnist_data/5520", "mnist_data/7953", "mnist_data/1611", "mnist_data/4361", "mnist_data/7836", "mnist_data/6048", "mnist_data/7181", "mnist_data/1456", "mnist_data/4409", "mnist_data/7338", "mnist_data/7412", "mnist_data/6822", "mnist_data/339", "mnist_data/2502", "mnist_data/8388", "mnist_data/4490", "mnist_data/4786", "mnist_data/6540", "mnist_data/2665", "mnist_data/6150", "mnist_data/6697", "mnist_data/9862", "mnist_data/9692", "mnist_data/958", "mnist_data/8722", "mnist_data/6862", "mnist_data/6355", "mnist_data/3133", "mnist_data/1908", "mnist_data/6607", "mnist_data/6947", "mnist_data/9350", "mnist_data/3625", "mnist_data/2049", "mnist_data/7997", "mnist_data/1777", "mnist_data/5560", "mnist_data/371", "mnist_data/7111", "mnist_data/4206", "mnist_data/4628", "mnist_data/6710", "mnist_data/4606", "mnist_data/2686", "mnist_data/2078", "mnist_data/1248", "mnist_data/7453", "mnist_data/3905", "mnist_data/3306", "mnist_data/2641", "mnist_data/1147", "mnist_data/2210", "mnist_data/540", "mnist_data/5325", "mnist_data/8453", "mnist_data/3386", "mnist_data/842", "mnist_data/9281", "mnist_data/5155", "mnist_data/9545", "mnist_data/3532", "mnist_data/3654", "mnist_data/1934", "mnist_data/1058", "mnist_data/7394", "mnist_data/6102", "mnist_data/3685", "mnist_data/782", "mnist_data/138", "mnist_data/8449", "mnist_data/8360", "mnist_data/3652", "mnist_data/4248", "mnist_data/9399", "mnist_data/7592", "mnist_data/5344", "mnist_data/948", "mnist_data/4278", "mnist_data/7199", "mnist_data/6568", "mnist_data/7990", "mnist_data/9915", "mnist_data/5527", "mnist_data/8350", "mnist_data/7754", "mnist_data/7091", "mnist_data/8514", "mnist_data/6894", "mnist_data/3693", "mnist_data/3945", "mnist_data/2662", "mnist_data/5057", "mnist_data/8268", "mnist_data/4760", "mnist_data/7358", "mnist_data/9401", "mnist_data/1551", "mnist_data/3348", "mnist_data/6718", "mnist_data/5933", "mnist_data/5293", "mnist_data/8174", "mnist_data/5145", "mnist_data/4264", "mnist_data/4780", "mnist_data/3591", "mnist_data/7628", "mnist_data/5565", "mnist_data/9140", "mnist_data/6027", "mnist_data/5490", "mnist_data/1296", "mnist_data/1403", "mnist_data/9984", "mnist_data/1936", "mnist_data/8116", "mnist_data/6125", "mnist_data/4722", "mnist_data/5384", "mnist_data/9810", "mnist_data/7611", "mnist_data/9653", "mnist_data/5131", "mnist_data/259", "mnist_data/7432", "mnist_data/9224", "mnist_data/276", "mnist_data/7420", "mnist_data/3423", "mnist_data/4894", "mnist_data/2041", "mnist_data/8235", "mnist_data/580", "mnist_data/7707", "mnist_data/5077", "mnist_data/5129", "mnist_data/2331", "mnist_data/6244", "mnist_data/4622", "mnist_data/1840", "mnist_data/5893", "mnist_data/6782", "mnist_data/5404", "mnist_data/9021", "mnist_data/4813", "mnist_data/3397", "mnist_data/5122", "mnist_data/7017", "mnist_data/5298", "mnist_data/1350", "mnist_data/9744", "mnist_data/6493", "mnist_data/4273", "mnist_data/5750", "mnist_data/8610", "mnist_data/497", "mnist_data/5099", "mnist_data/3053", "mnist_data/6757", "mnist_data/9430", "mnist_data/1468", "mnist_data/6635", "mnist_data/8560", "mnist_data/8236", "mnist_data/2402", "mnist_data/3444", "mnist_data/568", "mnist_data/4009", "mnist_data/2053", "mnist_data/7361", "mnist_data/7233", "mnist_data/952", "mnist_data/1868", "mnist_data/5467", "mnist_data/1770", "mnist_data/1064", "mnist_data/2271",
    "mnist_school_results/8707", "mnist_school_results/6265", "mnist_school_results/1984", "mnist_school_results/2861", "mnist_school_results/5986", "mnist_school_results/8400", "mnist_school_results/2020", "mnist_school_results/7608", "mnist_school_results/6111", "mnist_school_results/6166", "mnist_school_results/3457", "mnist_school_results/8635", "mnist_school_results/9269", "mnist_school_results/8284", "mnist_school_results/7764", "mnist_school_results/4769", "mnist_school_results/1925", "mnist_school_results/8436", "mnist_school_results/1686", "mnist_school_results/4644", "mnist_school_results/729", "mnist_school_results/1745", "mnist_school_results/1988", "mnist_school_results/1465", "mnist_school_results/1123", "mnist_school_results/475", "mnist_school_results/2566", "mnist_school_results/663", "mnist_school_results/4424", "mnist_school_results/7880", "mnist_school_results/1161", "mnist_school_results/5927", "mnist_school_results/2971", "mnist_school_results/3059", "mnist_school_results/3131", "mnist_school_results/8283", "mnist_school_results/8864", "mnist_school_results/9075", "mnist_school_results/79", "mnist_school_results/8881", "mnist_school_results/6455", "mnist_school_results/2035", "mnist_school_results/4342", "mnist_school_results/2675", "mnist_school_results/7055", "mnist_school_results/4602", "mnist_school_results/6736", "mnist_school_results/880", "mnist_school_results/3282", "mnist_school_results/5911", "mnist_school_results/2763", "mnist_school_results/7535", "mnist_school_results/9229", "mnist_school_results/6725", "mnist_school_results/6021", "mnist_school_results/1864", "mnist_school_results/7300", "mnist_school_results/6016", "mnist_school_results/4165", "mnist_school_results/1046", "mnist_school_results/3396", "mnist_school_results/2156", "mnist_school_results/6630", "mnist_school_results/5405", "mnist_school_results/5101", "mnist_school_results/8157", "mnist_school_results/5913", "mnist_school_results/8291", "mnist_school_results/8681", "mnist_school_results/127", "mnist_school_results/5840", "mnist_school_results/5896", "mnist_school_results/8700", "mnist_school_results/7905", "mnist_school_results/7639", "mnist_school_results/7331", "mnist_school_results/1949", "mnist_school_results/1909", "mnist_school_results/1139", "mnist_school_results/9495", "mnist_school_results/8596", "mnist_school_results/3410", "mnist_school_results/4762", "mnist_school_results/3752", "mnist_school_results/7044", "mnist_school_results/634", "mnist_school_results/4674", "mnist_school_results/5510", "mnist_school_results/4975", "mnist_school_results/1720", "mnist_school_results/9652", "mnist_school_results/5558", "mnist_school_results/4075", "mnist_school_results/284", "mnist_school_results/8841", "mnist_school_results/4115", "mnist_school_results/1643", "mnist_school_results/2185", "mnist_school_results/9109", "mnist_school_results/7948", "mnist_school_results/408", "mnist_school_results/3818", "mnist_school_results/1508", "mnist_school_results/715", "mnist_school_results/8938", "mnist_school_results/4496", "mnist_school_results/382", "mnist_school_results/9459", "mnist_school_results/3979", "mnist_school_results/1901", "mnist_school_results/7791", "mnist_school_results/3097", "mnist_school_results/9282", "mnist_school_results/2827", "mnist_school_results/4066", "mnist_school_results/4770", "mnist_school_results/5934", "mnist_school_results/2182", "mnist_school_results/8785", "mnist_school_results/5421", "mnist_school_results/6444", "mnist_school_results/8303", "mnist_school_results/4106", "mnist_school_results/6068", "mnist_school_results/5402", "mnist_school_results/4733", "mnist_school_results/8452", "mnist_school_results/4607", "mnist_school_results/2877", "mnist_school_results/8458", "mnist_school_results/1372", "mnist_school_results/9468", "mnist_school_results/5052", "mnist_school_results/4266", "mnist_school_results/3176", "mnist_school_results/1084", "mnist_school_results/2726", "mnist_school_results/7062", "mnist_school_results/7043", "mnist_school_results/500", "mnist_school_results/4221", "mnist_school_results/3391", "mnist_school_results/8962", "mnist_school_results/1143", "mnist_school_results/7722", "mnist_school_results/8912", "mnist_school_results/7112", "mnist_school_results/582", "mnist_school_results/3949", "mnist_school_results/430", "mnist_school_results/6994", "mnist_school_results/2908", "mnist_school_results/5181", "mnist_school_results/9", "mnist_school_results/1907", "mnist_school_results/7205", "mnist_school_results/113", "mnist_school_results/6686", "mnist_school_results/2278", "mnist_school_results/2251", "mnist_school_results/3429", "mnist_school_results/2191", "mnist_school_results/8416", "mnist_school_results/503", "mnist_school_results/3104", "mnist_school_results/1499", "mnist_school_results/6989", "mnist_school_results/1489", "mnist_school_results/7389", "mnist_school_results/3075", "mnist_school_results/8117", "mnist_school_results/9765", "mnist_school_results/7915", "mnist_school_results/750", "mnist_school_results/9402", "mnist_school_results/940", "mnist_school_results/4685", "mnist_school_results/8519", "mnist_school_results/2995", "mnist_school_results/2139", "mnist_school_results/5716", "mnist_school_results/7469", "mnist_school_results/6375", "mnist_school_results/4008", "mnist_school_results/8859", "mnist_school_results/8391", "mnist_school_results/7073", "mnist_school_results/7879", "mnist_school_results/1131", "mnist_school_results/7999", "mnist_school_results/6424", "mnist_school_results/9266", "mnist_school_results/7185", "mnist_school_results/774", "mnist_school_results/4887", "mnist_school_results/6823", "mnist_school_results/5663", "mnist_school_results/9520", "mnist_school_results/6733", "mnist_school_results/1807", "mnist_school_results/4699", "mnist_school_results/8990", "mnist_school_results/3518", "mnist_school_results/4575", "mnist_school_results/8822", "mnist_school_results/7547", "mnist_school_results/3063", "mnist_school_results/7454", "mnist_school_results/1991", "mnist_school_results/4318", "mnist_school_results/6130", "mnist_school_results/9677", "mnist_school_results/3080", "mnist_school_results/5089", "mnist_school_results/9042", "mnist_school_results/2418", "mnist_school_results/6851", "mnist_school_results/5296", "mnist_school_results/9595", "mnist_school_results/1077", "mnist_school_results/8604", "mnist_school_results/4748", "mnist_school_results/5636", "mnist_school_results/9712", "mnist_school_results/1753", "mnist_school_results/8829", "mnist_school_results/3274", "mnist_school_results/8425", "mnist_school_results/6933", "mnist_school_results/3439", "mnist_school_results/8439", "mnist_school_results/5707", "mnist_school_results/5677", "mnist_school_results/385", "mnist_school_results/9371", "mnist_school_results/9223", "mnist_school_results/5285", "mnist_school_results/1524", "mnist_school_results/2244", "mnist_school_results/2701", "mnist_school_results/9481", "mnist_school_results/375", "mnist_school_results/3540", "mnist_school_results/9438", "mnist_school_results/8200", "mnist_school_results/100", "mnist_school_results/7515", "mnist_school_results/9090", "mnist_school_results/5397", "mnist_school_results/6523", "mnist_school_results/136", "mnist_school_results/8978", "mnist_school_results/7343", "mnist_school_results/1865", "mnist_school_results/209", "mnist_school_results/2392", "mnist_school_results/6341", "mnist_school_results/5789", "mnist_school_results/7485", "mnist_school_results/7086", "mnist_school_results/272", "mnist_school_results/5371", "mnist_school_results/3470", "mnist_school_results/865", "mnist_school_results/7774", "mnist_school_results/4724", "mnist_school_results/302", "mnist_school_results/8273", "mnist_school_results/2452", "mnist_school_results/6582", "mnist_school_results/2003", "mnist_school_results/1284", "mnist_school_results/3432", "mnist_school_results/5034", "mnist_school_results/5186", "mnist_school_results/2537", "mnist_school_results/9494", "mnist_school_results/5816", "mnist_school_results/5168", "mnist_school_results/337", "mnist_school_results/9251", "mnist_school_results/4236", "mnist_school_results/1594", "mnist_school_results/212", "mnist_school_results/6609", "mnist_school_results/8834", "mnist_school_results/1375", "mnist_school_results/7835", "mnist_school_results/3483", "mnist_school_results/198", "mnist_school_results/8225", "mnist_school_results/9329", "mnist_school_results/5772", "mnist_school_results/4225", "mnist_school_results/9188", "mnist_school_results/3841", "mnist_school_results/9626", "mnist_school_results/6283", "mnist_school_results/6409", "mnist_school_results/3345", "mnist_school_results/6631", "mnist_school_results/7022", "mnist_school_results/4708", "mnist_school_results/6354", "mnist_school_results/6153", "mnist_school_results/1", "mnist_school_results/6908", "mnist_school_results/2259", "mnist_school_results/3191", "mnist_school_results/5979", "mnist_school_results/6335", "mnist_school_results/8948", "mnist_school_results/1794", "mnist_school_results/8007", "mnist_school_results/7641", "mnist_school_results/7967", "mnist_school_results/3461", "mnist_school_results/4015", "mnist_school_results/9761", "mnist_school_results/5796", "mnist_school_results/9839", "mnist_school_results/2823", "mnist_school_results/8712", "mnist_school_results/1393", "mnist_school_results/7768", "mnist_school_results/4604", "mnist_school_results/9835", "mnist_school_results/9702", "mnist_school_results/6648", "mnist_school_results/6758", "mnist_school_results/2503", "mnist_school_results/6643", "mnist_school_results/2811", "mnist_school_results/7585", "mnist_school_results/2742", "mnist_school_results/7232", "mnist_school_results/4791", "mnist_school_results/1804", "mnist_school_results/5064", "mnist_school_results/6865", "mnist_school_results/1444", "mnist_school_results/5980", "mnist_school_results/9896", "mnist_school_results/5372", "mnist_school_results/9857", "mnist_school_results/6112", "mnist_school_results/2466", "mnist_school_results/5537", "mnist_school_results/1664", "mnist_school_results/6787", "mnist_school_results/3622", "mnist_school_results/2985", "mnist_school_results/809", "mnist_school_results/7156", "mnist_school_results/1033", "mnist_school_results/4650", "mnist_school_results/1791", "mnist_school_results/1266", "mnist_school_results/4917", "mnist_school_results/9826", "mnist_school_results/8633", "mnist_school_results/8549", "mnist_school_results/7089", "mnist_school_results/1637", "mnist_school_results/1542", "mnist_school_results/9889", "mnist_school_results/2821", "mnist_school_results/7128", "mnist_school_results/6978", "mnist_school_results/9663", "mnist_school_results/4750", "mnist_school_results/5736", "mnist_school_results/2598", "mnist_school_results/7795", "mnist_school_results/283", "mnist_school_results/5640", "mnist_school_results/2202", "mnist_school_results/9584", "mnist_school_results/8875", "mnist_school_results/1765", "mnist_school_results/7462", "mnist_school_results/6919", "mnist_school_results/9004", "mnist_school_results/7868", "mnist_school_results/8126", "mnist_school_results/3140", "mnist_school_results/6036", "mnist_school_results/8156", "mnist_school_results/1644", "mnist_school_results/6907", "mnist_school_results/6397", "mnist_school_results/7685", "mnist_school_results/4939", "mnist_school_results/8683", "mnist_school_results/456", "mnist_school_results/7200", "mnist_school_results/3666", "mnist_school_results/618", "mnist_school_results/1556", "mnist_school_results/3035", "mnist_school_results/7014", "mnist_school_results/8833", "mnist_school_results/2247", "mnist_school_results/3311", "mnist_school_results/8211", "mnist_school_results/2231", "mnist_school_results/769", "mnist_school_results/115", "mnist_school_results/4386", "mnist_school_results/806", "mnist_school_results/9756", "mnist_school_results/2161", "mnist_school_results/6864", "mnist_school_results/260", "mnist_school_results/223", "mnist_school_results/1076", "mnist_school_results/4536", "mnist_school_results/2470", "mnist_school_results/9727", "mnist_school_results/2629", "mnist_school_results/7293", "mnist_school_results/7961", "mnist_school_results/112", "mnist_school_results/2372", "mnist_school_results/7366", "mnist_school_results/6004", "mnist_school_results/6184", "mnist_school_results/6050", "mnist_school_results/6277", "mnist_school_results/4581", "mnist_school_results/7632", "mnist_school_results/8290", "mnist_school_results/3639", "mnist_school_results/42", "mnist_school_results/6724", "mnist_school_results/8316", "mnist_school_results/288", "mnist_school_results/5452", "mnist_school_results/3567", "mnist_school_results/5752", "mnist_school_results/7243", "mnist_school_results/2079", "mnist_school_results/5948", "mnist_school_results/8698", "mnist_school_results/6122", "mnist_school_results/8205", "mnist_school_results/998", "mnist_school_results/2677", "mnist_school_results/5281", "mnist_school_results/1048", "mnist_school_results/1627", "mnist_school_results/3170", "mnist_school_results/6800", "mnist_school_results/8492", "mnist_school_results/2377", "mnist_school_results/6656", "mnist_school_results/7015", "mnist_school_results/405", "mnist_school_results/1623", "mnist_school_results/6161", "mnist_school_results/3239", "mnist_school_results/3155", "mnist_school_results/5852", "mnist_school_results/184", "mnist_school_results/2093", "mnist_school_results/2580", "mnist_school_results/5652", "mnist_school_results/9345", "mnist_school_results/319", "mnist_school_results/3411", "mnist_school_results/7741", "mnist_school_results/4565", "mnist_school_results/401", "mnist_school_results/8248", "mnist_school_results/7646", "mnist_school_results/4088", "mnist_school_results/4451", "mnist_school_results/4295", "mnist_school_results/2272", "mnist_school_results/7852", "mnist_school_results/6562", "mnist_school_results/4255", "mnist_school_results/8234", "mnist_school_results/7593", "mnist_school_results/7766", "mnist_school_results/6154", "mnist_school_results/4404", "mnist_school_results/4877", "mnist_school_results/2761", "mnist_school_results/34", "mnist_school_results/8984", "mnist_school_results/9244", "mnist_school_results/7114", "mnist_school_results/5570", "mnist_school_results/4147", "mnist_school_results/7777", "mnist_school_results/7012", "mnist_school_results/5868", "mnist_school_results/9646", "mnist_school_results/6922", "mnist_school_results/6436", "mnist_school_results/4849", "mnist_school_results/4713", "mnist_school_results/1343", "mnist_school_results/9005", "mnist_school_results/1502", "mnist_school_results/488", "mnist_school_results/93", "mnist_school_results/4371", "mnist_school_results/8873", "mnist_school_results/4334", "mnist_school_results/565", "mnist_school_results/8691", "mnist_school_results/4053", "mnist_school_results/9185", "mnist_school_results/5811", "mnist_school_results/8774", "mnist_school_results/1707", "mnist_school_results/7439", "mnist_school_results/2581", "mnist_school_results/814", "mnist_school_results/1927", "mnist_school_results/1783", "mnist_school_results/3660", "mnist_school_results/2523", "mnist_school_results/4530", "mnist_school_results/2718", "mnist_school_results/2344", "mnist_school_results/4355", "mnist_school_results/7058", "mnist_school_results/2276", "mnist_school_results/3242", "mnist_school_results/2619", "mnist_school_results/2526", "mnist_school_results/7460", "mnist_school_results/1338", "mnist_school_results/4852", "mnist_school_results/3886", "mnist_school_results/2772", "mnist_school_results/3933", "mnist_school_results/5065", "mnist_school_results/2904", "mnist_school_results/8790", "mnist_school_results/3509", "mnist_school_results/3440", "mnist_school_results/3265", "mnist_school_results/6794", "mnist_school_results/4546", "mnist_school_results/3355", "mnist_school_results/398", "mnist_school_results/8194", "mnist_school_results/5808", "mnist_school_results/5634", "mnist_school_results/1478", "mnist_school_results/3992", "mnist_school_results/9053", "mnist_school_results/8341", "mnist_school_results/1965", "mnist_school_results/5712", "mnist_school_results/7562", "mnist_school_results/2490", "mnist_school_results/6774", "mnist_school_results/2012", "mnist_school_results/1599", "mnist_school_results/6777", "mnist_school_results/3375", "mnist_school_results/3", "mnist_school_results/5246", "mnist_school_results/6594", "mnist_school_results/7732", "mnist_school_results/4608", "mnist_school_results/1843", "mnist_school_results/2108", "mnist_school_results/7528", "mnist_school_results/4719", "mnist_school_results/2144", "mnist_school_results/2973", "mnist_school_results/1235", "mnist_school_results/5995", "mnist_school_results/6092", "mnist_school_results/772", "mnist_school_results/8237", "mnist_school_results/3425", "mnist_school_results/4092", "mnist_school_results/975", "mnist_school_results/9129", "mnist_school_results/5291", "mnist_school_results/3043", "mnist_school_results/8308", "mnist_school_results/9858", "mnist_school_results/8497", "mnist_school_results/2068", "mnist_school_results/5514", "mnist_school_results/8472", "mnist_school_results/6451", "mnist_school_results/6937", "mnist_school_results/2856", "mnist_school_results/7986", "mnist_school_results/7931", "mnist_school_results/6946", "mnist_school_results/5892", "mnist_school_results/1722", "mnist_school_results/5375", "mnist_school_results/9051", "mnist_school_results/818", "mnist_school_results/9418", "mnist_school_results/2209", "mnist_school_results/7599", "mnist_school_results/942", "mnist_school_results/2431", "mnist_school_results/6776", "mnist_school_results/6198", "mnist_school_results/9056", "mnist_school_results/8279", "mnist_school_results/515", "mnist_school_results/3462", "mnist_school_results/1759", "mnist_school_results/3792", "mnist_school_results/5380", "mnist_school_results/525", "mnist_school_results/2733", "mnist_school_results/9504", "mnist_school_results/8672", "mnist_school_results/1947", "mnist_school_results/4408", "mnist_school_results/3027", "mnist_school_results/5658", "mnist_school_results/8769", "mnist_school_results/4228", "mnist_school_results/2456", "mnist_school_results/5209", "mnist_school_results/3340", "mnist_school_results/8918", "mnist_school_results/6139", "mnist_school_results/959", "mnist_school_results/4817", "mnist_school_results/2867", "mnist_school_results/9043", "mnist_school_results/9579", "mnist_school_results/7688", "mnist_school_results/796", "mnist_school_results/4379", "mnist_school_results/6844", "mnist_school_results/4406", "mnist_school_results/6786", "mnist_school_results/8583", "mnist_school_results/4459", "mnist_school_results/3839", "mnist_school_results/4979", "mnist_school_results/7104", "mnist_school_results/950", "mnist_school_results/6137", "mnist_school_results/8680", "mnist_school_results/7160", "mnist_school_results/426", "mnist_school_results/9853", "mnist_school_results/7695", "mnist_school_results/6232", "mnist_school_results/5674", "mnist_school_results/303", "mnist_school_results/2223", "mnist_school_results/3768", "mnist_school_results/6519", "mnist_school_results/6799", "mnist_school_results/7480", "mnist_school_results/2384", "mnist_school_results/9787", "mnist_school_results/7761", "mnist_school_results/5023", "mnist_school_results/7504", "mnist_school_results/9215", "mnist_school_results/5430", "mnist_school_results/861", "mnist_school_results/2498", "mnist_school_results/1292", "mnist_school_results/6598", "mnist_school_results/1135", "mnist_school_results/7827", "mnist_school_results/6668", "mnist_school_results/279", "mnist_school_results/3266", "mnist_school_results/8376", "mnist_school_results/501", "mnist_school_results/4012", "mnist_school_results/3107", "mnist_school_results/6678", "mnist_school_results/7792", "mnist_school_results/7834", "mnist_school_results/5660", "mnist_school_results/9537", "mnist_school_results/9320", "mnist_school_results/5382", "mnist_school_results/706", "mnist_school_results/4309", "mnist_school_results/5575", "mnist_school_results/7326", "mnist_school_results/9378", "mnist_school_results/4825", "mnist_school_results/8640", "mnist_school_results/1186", "mnist_school_results/3968", "mnist_school_results/528", "mnist_school_results/7057", "mnist_school_results/4717", "mnist_school_results/9180", "mnist_school_results/7252", "mnist_school_results/5206", "mnist_school_results/4525", "mnist_school_results/1422", "mnist_school_results/2103", "mnist_school_results/7081", "mnist_school_results/2095", "mnist_school_results/2282", "mnist_school_results/2340", "mnist_school_results/7796", "mnist_school_results/9083", "mnist_school_results/4081", "mnist_school_results/9779", "mnist_school_results/2266", "mnist_school_results/6817", "mnist_school_results/7119", "mnist_school_results/9995", "mnist_school_results/1293", "mnist_school_results/5814", "mnist_school_results/5545", "mnist_school_results/3475", "mnist_school_results/9388", "mnist_school_results/4729", "mnist_school_results/3955", "mnist_school_results/2884", "mnist_school_results/59", "mnist_school_results/8396", "mnist_school_results/5618", "mnist_school_results/7475", "mnist_school_results/5804", "mnist_school_results/6932", "mnist_school_results/208", "mnist_school_results/3998", "mnist_school_results/376", "mnist_school_results/4002", "mnist_school_results/4052", "mnist_school_results/7042", "mnist_school_results/9845", "mnist_school_results/1326", "mnist_school_results/8362", "mnist_school_results/2578", "mnist_school_results/5368", "mnist_school_results/5032", "mnist_school_results/5645", "mnist_school_results/9136", "mnist_school_results/9367", "mnist_school_results/1717", "mnist_school_results/2083", "mnist_school_results/1045", "mnist_school_results/7351", "mnist_school_results/4677", "mnist_school_results/6911", "mnist_school_results/4449", "mnist_school_results/9983", "mnist_school_results/4068", "mnist_school_results/2085", "mnist_school_results/8053", "mnist_school_results/7337", "mnist_school_results/3195", "mnist_school_results/5072", "mnist_school_results/133", "mnist_school_results/3032", "mnist_school_results/696", "mnist_school_results/4658", "mnist_school_results/7798", "mnist_school_results/4113", "mnist_school_results/7142", "mnist_school_results/7654", "mnist_school_results/6863", "mnist_school_results/5311", "mnist_school_results/3761", "mnist_school_results/1244", "mnist_school_results/2422", "mnist_school_results/1912", "mnist_school_results/8172", "mnist_school_results/778", "mnist_school_results/7023", "mnist_school_results/3034", "mnist_school_results/7725", "mnist_school_results/8340", "mnist_school_results/4985", "mnist_school_results/6526", "mnist_school_results/9001", "mnist_school_results/162", "mnist_school_results/4411", "mnist_school_results/7249", "mnist_school_results/8056", "mnist_school_results/1877", "mnist_school_results/888", "mnist_school_results/2825", "mnist_school_results/4790", "mnist_school_results/8275", "mnist_school_results/5549", "mnist_school_results/2228", "mnist_school_results/4400", "mnist_school_results/8358", "mnist_school_results/9946", "mnist_school_results/5297", "mnist_school_results/8064", "mnist_school_results/1026", "mnist_school_results/5006", "mnist_school_results/8979", "mnist_school_results/1963", "mnist_school_results/6351", "mnist_school_results/7423", "mnist_school_results/9785", "mnist_school_results/8133", "mnist_school_results/3599", "mnist_school_results/8003", "mnist_school_results/4967", "mnist_school_results/9691", "mnist_school_results/1893", "mnist_school_results/4211", "mnist_school_results/7495", "mnist_school_results/7194", "mnist_school_results/5655", "mnist_school_results/4191", "mnist_school_results/756", "mnist_school_results/5520", "mnist_school_results/7953", "mnist_school_results/1611", "mnist_school_results/4361", "mnist_school_results/7836", "mnist_school_results/6048", "mnist_school_results/7181", "mnist_school_results/1456", "mnist_school_results/4409", "mnist_school_results/7338", "mnist_school_results/7412", "mnist_school_results/6822", "mnist_school_results/339", "mnist_school_results/2502", "mnist_school_results/8388", "mnist_school_results/4490", "mnist_school_results/4786", "mnist_school_results/6540", "mnist_school_results/2665", "mnist_school_results/6150", "mnist_school_results/6697", "mnist_school_results/9862", "mnist_school_results/9692", "mnist_school_results/958", "mnist_school_results/8722", "mnist_school_results/6862", "mnist_school_results/6355", "mnist_school_results/3133", "mnist_school_results/1908", "mnist_school_results/6607", "mnist_school_results/6947", "mnist_school_results/9350", "mnist_school_results/3625", "mnist_school_results/2049", "mnist_school_results/7997", "mnist_school_results/1777", "mnist_school_results/5560", "mnist_school_results/371", "mnist_school_results/7111", "mnist_school_results/4206", "mnist_school_results/4628", "mnist_school_results/6710", "mnist_school_results/4606", "mnist_school_results/2686", "mnist_school_results/2078", "mnist_school_results/1248", "mnist_school_results/7453", "mnist_school_results/3905", "mnist_school_results/3306", "mnist_school_results/2641", "mnist_school_results/1147", "mnist_school_results/2210", "mnist_school_results/540", "mnist_school_results/5325", "mnist_school_results/8453", "mnist_school_results/3386", "mnist_school_results/842", "mnist_school_results/9281", "mnist_school_results/5155", "mnist_school_results/9545", "mnist_school_results/3532", "mnist_school_results/3654", "mnist_school_results/1934", "mnist_school_results/1058", "mnist_school_results/7394", "mnist_school_results/6102", "mnist_school_results/3685", "mnist_school_results/782", "mnist_school_results/138", "mnist_school_results/8449", "mnist_school_results/8360", "mnist_school_results/3652", "mnist_school_results/4248", "mnist_school_results/9399", "mnist_school_results/7592", "mnist_school_results/5344", "mnist_school_results/948", "mnist_school_results/4278", "mnist_school_results/7199", "mnist_school_results/6568", "mnist_school_results/7990", "mnist_school_results/9915", "mnist_school_results/5527", "mnist_school_results/8350", "mnist_school_results/7754", "mnist_school_results/7091", "mnist_school_results/8514", "mnist_school_results/6894", "mnist_school_results/3693", "mnist_school_results/3945", "mnist_school_results/2662", "mnist_school_results/5057", "mnist_school_results/8268", "mnist_school_results/4760", "mnist_school_results/7358", "mnist_school_results/9401", "mnist_school_results/1551", "mnist_school_results/3348", "mnist_school_results/6718", "mnist_school_results/5933", "mnist_school_results/5293", "mnist_school_results/8174", "mnist_school_results/5145", "mnist_school_results/4264", "mnist_school_results/4780", "mnist_school_results/3591", "mnist_school_results/7628", "mnist_school_results/5565", "mnist_school_results/9140", "mnist_school_results/6027", "mnist_school_results/5490", "mnist_school_results/1296", "mnist_school_results/1403", "mnist_school_results/9984", "mnist_school_results/1936", "mnist_school_results/8116", "mnist_school_results/6125", "mnist_school_results/4722", "mnist_school_results/5384", "mnist_school_results/9810", "mnist_school_results/7611", "mnist_school_results/9653", "mnist_school_results/5131", "mnist_school_results/259", "mnist_school_results/7432", "mnist_school_results/9224", "mnist_school_results/276", "mnist_school_results/7420", "mnist_school_results/3423", "mnist_school_results/4894", "mnist_school_results/2041", "mnist_school_results/8235", "mnist_school_results/580", "mnist_school_results/7707", "mnist_school_results/5077", "mnist_school_results/5129", "mnist_school_results/2331", "mnist_school_results/6244", "mnist_school_results/4622", "mnist_school_results/1840", "mnist_school_results/5893", "mnist_school_results/6782", "mnist_school_results/5404", "mnist_school_results/9021", "mnist_school_results/4813", "mnist_school_results/3397", "mnist_school_results/5122", "mnist_school_results/7017", "mnist_school_results/5298", "mnist_school_results/1350", "mnist_school_results/9744", "mnist_school_results/6493", "mnist_school_results/4273", "mnist_school_results/5750", "mnist_school_results/8610", "mnist_school_results/497", "mnist_school_results/5099", "mnist_school_results/3053", "mnist_school_results/6757", "mnist_school_results/9430", "mnist_school_results/1468", "mnist_school_results/6635", "mnist_school_results/8560", "mnist_school_results/8236", "mnist_school_results/2402", "mnist_school_results/3444", "mnist_school_results/568", "mnist_school_results/4009", "mnist_school_results/2053", "mnist_school_results/7361", "mnist_school_results/7233", "mnist_school_results/952", "mnist_school_results/1868", "mnist_school_results/5467", "mnist_school_results/1770", "mnist_school_results/1064", "mnist_school_results/2271"]

    MISSING_TESTS_FILE = "TESTS NOT INTACT: A file belonging to the tests is missing: \"{}\"\nPlease make sure you have fully extracted the TAR to the right place.\n"
    MISSING_DIR_FILE = "TESTS NOT INTACT: A directory belonging to the tests is missing: \"{}/\"\nPlease make sure you have fully extracted the TAR to the right place.\n"

    def __init__(self):
        sys.stdout.write(title("CHECKING TESTS INTEGRITY"))
        for dirname in TestsIntegrity.TESTS_DIRS:
            if not os.path.isdir(dirname):
                sys.stderr.write(red(TestsIntegrity.MISSING_TESTS_DIR.format(dirname), bold = True))
                sys.exit(1)
        for filename in TestsIntegrity.TESTS_FILES:
            if not os.path.isfile(filename):
                sys.stderr.write(red(TestsIntegrity.MISSING_TESTS_FILE.format(filename), bold = True))
                sys.exit(1)

        sys.stdout.write("Tests intact.\n")


class Compile:
    def __init__(self, headers, sources):
        sys.stdout.write(title(f"""COMPILATION{" (OPTIMIZED)" if FAST else ""}{" (WITH VALGRIND)" if USE_VALGRIND else ""}"""))
        if shutil.which(CXX) is None:
            sys.stderr.write(red(f"Compiler \"{CXX}\" not found. Aborting tests.\n", bold = True))
            sys.exit(1)

        if FAST:
            sys.stderr.write(yellow("WARNING: using extreme compile-time optimizations can considerably increase floating-point arithmetic deviations to the point of falsifying the test results.\n"))

        for header in headers:
            if not os.path.isfile(header):
                sys.stderr.write(red(f"Header file \"{header}\" not found. Aborting tests.\n", bold = True))
                sys.exit(1)

        for source in sources:
            if not os.path.isfile(source):
                sys.stderr.write(red(f"Source file \"{source}\" not found. Aborting tests.\n", bold = True))
                sys.exit(1)

        compile_cmd = [CXX, *CXXFLAGS, *SOURCES, TESTS_SOURCE]
        sys.stderr.write(' '.join(compile_cmd) + '\n')
        if sp.Popen(compile_cmd).wait() != 0:
            sys.stderr.write(red("Compilation failed. Aborting tests.\n", bold = True))
            sys.exit(1)

        sys.stdout.write(green("Compilation successful.\n"))

class MatrixTests:
    @staticmethod
    def load_text_matrix(mat_text):
        return np.array([list(map(MatrixTests.MAT_DTYPE, row.split())) for row in mat_text.splitlines()])

    @staticmethod
    def randint(low, high, size = None):
        if low == high:
            if size == None:
                return low
            else:
                return np.full(size, low, dtype = int)
        else:
            return np.random.randint(low, high, size)

    @staticmethod
    def randmat(dim_bounds, entry_bounds, rows = None, cols = None):
        return np.random.uniform(*entry_bounds, size = MatrixTests.randint(*dim_bounds, size = 2) if rows is None else
                                                           (rows, MatrixTests.randint(*dim_bounds) if cols is None else cols)).astype(MatrixTests.MAT_DTYPE)

    @staticmethod
    def matctor0():
        test_name = MatrixTests.VALID_MATCTOR_TEST_NAME.format(0)
        test_cmd = [*TESTS_BIN, "matctor0"]
        proc = sp.Popen(test_cmd, stdout = sp.PIPE, stderr = sp.PIPE)
        result_out_text, result_err_text = map(decode_bytes, (proc.stdout.read(), proc.stderr.read()))
        actual_mat = MatrixTests.load_text_matrix(result_out_text)

        retcode = proc.wait()
        if retcode != 0:
            sys.stderr.write(red(f"Default-construction of a matrix caused your code to exit with code {retcode}.\n"))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            if USE_VALGRIND:
                sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            TEST_FAILED(test_name)
            return True

        elif actual_mat.size != 1:
            sys.stderr.write(red(f"Default-construction of a matrix yielded a matrix with dimensions {actual_mat.shape}.\n"))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

        if result_err_text:
            sys.stderr.write(red(f"Default-construction of a matrix caused your code to print to standard error.\n"))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

        if USE_VALGRIND and os.path.isfile(VALGRIND_LOGFILE) and os.stat(VALGRIND_LOGFILE).st_size > 0:
            sys.stderr.write(red(f"Valgrind has detected a memory problem while running test \"{test_name}\":\n"))
            with open(VALGRIND_LOGFILE, 'r') as valgrind_logfile_rfd:
                valgrind_log_lines = valgrind_logfile_rfd.read().splitlines()
            sys.stderr.write('\n'.join('\t' + valgrind_log_line for valgrind_log_line in valgrind_log_lines))
            sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

    @staticmethod
    def matctor1():
        test_name = MatrixTests.VALID_MATCTOR_TEST_NAME.format(1)
        mat = MatrixTests.randmat(MatrixTests.MATCTOR_DIM_BOUNDS, MatrixTests.MATCTOR_ENTRY_BOUNDS)

        test_cmd = [*TESTS_BIN, "matctor1", *map(str, mat.shape)]
        proc = sp.Popen(test_cmd, stdin = sp.PIPE, stdout = sp.PIPE, stderr = sp.PIPE)
        result_out_text, result_err_text = map(decode_bytes, proc.communicate(mat.tobytes()))
        retcode = proc.wait()
        if retcode != 0:
            sys.stderr.write(red(f"Copy-construction of a matrix with dimensions {mat.shape} caused your code to exit with code {retcode}.\n"))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            if USE_VALGRIND:
                sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            TEST_FAILED(test_name)
            return True

        actual_mat = MatrixTests.load_text_matrix(result_out_text)
        if not np.allclose(mat, actual_mat, rtol = MatrixTests.MATCTOR_REL_DEV, atol = MatrixTests.MATCTOR_ABS_DEV):
            avg_dev = np.abs(np.average(mat - actual_mat))
            sys.stderr.write(red(f"Copy-construction of a matrix with dimensions {mat.shape} yielded a highly deviant results (abs avg dev = {avg_dev}).\n"))

            np.savetxt(EXPECTED_RESULTS_FILE, mat)
            np.savetxt(ACTUAL_RESULTS_FILE, actual_mat)
            sys.stderr.write(DUMP_FILES_INFO)

            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

        if result_err_text:
            sys.stderr.write(red(f"Copy-construction of a matrix with dimensions {mat.shape} caused your code to print to standard error.\n"))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

        if USE_VALGRIND and os.path.isfile(VALGRIND_LOGFILE) and os.stat(VALGRIND_LOGFILE).st_size > 0:
            sys.stderr.write(red(f"Valgrind has detected a memory problem while running test \"{test_name}\":\n"))
            with open(VALGRIND_LOGFILE, 'r') as valgrind_logfile_rfd:
                valgrind_log_lines = valgrind_logfile_rfd.read().splitlines()
            sys.stderr.write('\n'.join('\t' + valgrind_log_line for valgrind_log_line in valgrind_log_lines))
            with open(VALGRIND_LOGFILE, 'r') as valgrind_logfile_rfd:
                valgrind_log_lines = valgrind_logfile_rfd.read().splitlines()
            sys.stderr.write('\n'.join('\t' + valgrind_log_line for valgrind_log_line in valgrind_log_lines))

            sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

    @staticmethod
    def valid_matctor2():
        test_name = MatrixTests.VALID_MATCTOR_TEST_NAME.format(2)
        dims = tuple(MatrixTests.randint(*MatrixTests.MATCTOR_DIM_BOUNDS, size = 2))
        test_cmd = [*TESTS_BIN, "matctor2", *map(str, dims)]
        proc = sp.Popen(test_cmd, stdout = sp.PIPE, stderr = sp.PIPE)
        result_out_text, result_err_text = map(decode_bytes, (proc.stdout.read(), proc.stderr.read()))
        retcode = proc.wait()

        if retcode != 0:
            sys.stderr.write(red(f"Construction of a matrix with valid dimensions {dims} caused your code to exit with code {retcode}.\n"))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            if USE_VALGRIND:
                sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            TEST_FAILED(test_name)
            return True

        actual_mat = MatrixTests.load_text_matrix(result_out_text)
        if actual_mat.shape != dims:
            sys.stderr.write(red(f"Construction of a matrix with valid dimensions {dims} yielded a matrix with dimensions {actual_mat.shape}.\n"))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

        if result_err_text:
            sys.stderr.write(red(f"Construction of a matrix with valid dimensions {dims} caused your code to print to standard error.\n"))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

        if USE_VALGRIND and os.path.isfile(VALGRIND_LOGFILE) and os.stat(VALGRIND_LOGFILE).st_size > 0:
            sys.stderr.write(red(f"Valgrind has detected a memory problem while running test \"{test_name}\":\n"))
            with open(VALGRIND_LOGFILE, 'r') as valgrind_logfile_rfd:
                valgrind_log_lines = valgrind_logfile_rfd.read().splitlines()
            sys.stderr.write('\n'.join('\t' + valgrind_log_line for valgrind_log_line in valgrind_log_lines))
            sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

    @staticmethod
    def premature_eof():
        test_name = MatrixTests.MATIO_PREMATURE_EOF_TEST_NAME
        mat = MatrixTests.randmat(MatrixTests.MATIO_DIM_BOUNDS, MatrixTests.MATIO_ENTRY_BOUNDS)
        bad_shape = tuple(MatrixTests.randint(*MatrixTests.MATIO_DIM_BOUNDS, size = 2))
        while bad_shape[0] * bad_shape[1] <= mat.size: # Guarantee we try to load more data than we provide
            bad_shape = tuple(MatrixTests.randint(*MatrixTests.MATIO_DIM_BOUNDS, size = 2))

        test_cmd = [*TESTS_BIN, "matload", *map(str, bad_shape)]
        proc = sp.Popen(test_cmd, stdin = sp.PIPE, stdout = sp.PIPE, stderr = sp.PIPE)
        result_out_text, result_err_text = map(decode_bytes, proc.communicate(mat.tobytes()))
        retcode = proc.wait()

        if retcode != 1:
            sys.stderr.write(red(f"Premature EOF when loading {bad_shape[0] * bad_shape[1]} elements "\
                                 f"into a matrix with dimensions {mat.shape} (streaming less data than reported) didn't cause an exit with code 1 (but rather {retcode}).\n"))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            if USE_VALGRIND:
                sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            TEST_FAILED(test_name)
            return True

        if result_out_text:
            sys.stderr.write(red(f"Upon a premature EOF when loading {bad_shape[0] * bad_shape[1]} elements "\
                                 f"into a matrix with dimensions {mat.shape} (streaming less data than reported), your code printed to standard output.\n"))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

        if not (result_err_text.startswith("Error:") and result_err_text.endswith('\n')):
            sys.stderr.write(red(f"Upon a premature EOF when loading {bad_shape[0] * bad_shape[1]} elements "\
                                 f"into a matrix with dimensions {mat.shape} (streaming less data than reported), your code should print to standard error " \
                                  "a message starting with \"Error:\" and ending with a newline.\n"))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

        if USE_VALGRIND_EXTRA and os.path.isfile(VALGRIND_LOGFILE) and os.stat(VALGRIND_LOGFILE).st_size > 0:
            sys.stderr.write(red(f"Valgrind has detected a memory problem while running test \"{test_name}\":\n"))
            with open(VALGRIND_LOGFILE, 'r') as valgrind_logfile_rfd:
                valgrind_log_lines = valgrind_logfile_rfd.read().splitlines()
            sys.stderr.write('\n'.join('\t' + valgrind_log_line for valgrind_log_line in valgrind_log_lines))
            sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

    @staticmethod
    def missing_eof():
        test_name = MatrixTests.MATIO_MISSING_EOF_TEST_NAME
        mat = MatrixTests.randmat(MatrixTests.MATIO_DIM_BOUNDS, MatrixTests.MATIO_ENTRY_BOUNDS)
        bad_shape = tuple(MatrixTests.randint(*MatrixTests.MATIO_DIM_BOUNDS, size = 2))
        while bad_shape[0] * bad_shape[1] >= mat.size: # Guarantee we try to load more data than we provide
            bad_shape = tuple(MatrixTests.randint(*MatrixTests.MATIO_DIM_BOUNDS, size = 2))

        test_cmd = [*TESTS_BIN, "matload", *map(str, bad_shape)]
        proc = sp.Popen(test_cmd, stdin = sp.PIPE, stdout = sp.PIPE, stderr = sp.PIPE)
        result_out_text, result_err_text = map(decode_bytes, proc.communicate(mat.tobytes()))
        retcode = proc.wait()

        if retcode != 1:
            sys.stderr.write(red(f"Missing EOF when loading {bad_shape[0] * bad_shape[1]} elements "\
                                 f"into a matrix with dimensions {mat.shape} (streaming more data than reported) didn't cause an exit with code 1 (but rather {retcode}).\n"))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            if USE_VALGRIND:
                sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            TEST_FAILED(test_name)
            return True

        if result_out_text:
            sys.stderr.write(red(f"Upon withholding EOF when loading {bad_shape[0] * bad_shape[1]} elements "\
                                 f"into a matrix with dimensions {mat.shape} (streaming more data than reported), your code printed to standard output.\n"))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

        if not (result_err_text.startswith("Error:") and result_err_text.endswith('\n')):
            sys.stderr.write(red(f"Upon withholding EOF when loading {bad_shape[0] * bad_shape[1]} elements "\
                                 f"into a matrix with dimensions {mat.shape} (streaming more data than reported), your code should print to standard error " \
                                  "a message starting with \"Error:\" and ending with a newline.\n"))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

        if USE_VALGRIND_EXTRA and os.path.isfile(VALGRIND_LOGFILE) and os.stat(VALGRIND_LOGFILE).st_size > 0:
            sys.stderr.write(red(f"Valgrind has detected a memory problem while running test \"{test_name}\":\n"))
            with open(VALGRIND_LOGFILE, 'r') as valgrind_logfile_rfd:
                valgrind_log_lines = valgrind_logfile_rfd.read().splitlines()
            sys.stderr.write('\n'.join('\t' + valgrind_log_line for valgrind_log_line in valgrind_log_lines))
            sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

    @staticmethod
    def matassign():
        test_name = MatrixTests.MATASSIGN_TEST_NAME
        mat1 = MatrixTests.randmat(MatrixTests.MATASSIGN_DIM_BOUNDS, MatrixTests.MATASSIGN_ENTRY_BOUNDS)
        mat2 = MatrixTests.randmat(MatrixTests.MATASSIGN_DIM_BOUNDS, MatrixTests.MATASSIGN_ENTRY_BOUNDS)

        test_cmd = [*TESTS_BIN, "matassign", *map(str, mat1.shape + mat2.shape)]
        proc = sp.Popen(test_cmd, stdin = sp.PIPE, stdout = sp.PIPE, stderr = sp.PIPE)
        result_out_text, result_err_text = map(decode_bytes, proc.communicate(mat1.tobytes() + mat2.tobytes()))
        retcode = proc.wait()
        if retcode != 0:
            sys.stderr.write(red(f"Assignment of matrices with dimensions {mat1.shape} = {mat2.shape} caused your code to exit with code {retcode}.\n"))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            if USE_VALGRIND:
                sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            TEST_FAILED(test_name)
            return True

        if result_err_text:
            sys.stderr.write(red(f"Assignment of matrices with dimensions {mat1.shape} = {mat2.shape} caused your code to print to standard error.\n"))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

        if USE_VALGRIND and os.path.isfile(VALGRIND_LOGFILE) and os.stat(VALGRIND_LOGFILE).st_size > 0:
            sys.stderr.write(red(f"Valgrind has detected a memory problem while running test \"{test_name}\":\n"))
            with open(VALGRIND_LOGFILE, 'r') as valgrind_logfile_rfd:
                valgrind_log_lines = valgrind_logfile_rfd.read().splitlines()
            sys.stderr.write('\n'.join('\t' + valgrind_log_line for valgrind_log_line in valgrind_log_lines))
            sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

        expected_mat = mat2.astype(MatrixTests.MAT_DTYPE)
        actual_mat = MatrixTests.load_text_matrix(result_out_text)

        if not np.allclose(expected_mat, actual_mat, rtol = MatrixTests.MATASSIGN_REL_DEV, atol = MatrixTests.MATASSIGN_ABS_DEV):
            avg_dev = np.abs(np.average(expected_mat - actual_mat))
            sys.stderr.write(red(f"Assignment of matrices with dimensions {mat1.shape} = {mat2.shape} yielded a highly deviant results (abs avg dev = {avg_dev}).\n"))

            np.savetxt(EXPECTED_RESULTS_FILE, expected_mat)
            np.savetxt(ACTUAL_RESULTS_FILE, actual_mat)

            sys.stderr.write(DUMP_FILES_INFO)
            TEST_FAILED(test_name)
            return True

    @staticmethod
    def valid_matmul():
        test_name = MatrixTests.VALID_MATMUL_TEST_NAME

        mat1 = MatrixTests.randmat(MatrixTests.MATMUL_DIM_BOUNDS, MatrixTests.MATMUL_ENTRY_BOUNDS)
        mat2 = MatrixTests.randmat(MatrixTests.MATMUL_DIM_BOUNDS, MatrixTests.MATMUL_ENTRY_BOUNDS, rows = mat1.shape[1])

        test_cmd = [*TESTS_BIN, "matmul", *map(str, mat1.shape + mat2.shape)]
        proc = sp.Popen(test_cmd, stdin = sp.PIPE, stdout = sp.PIPE, stderr = sp.PIPE)
        result_out_text, result_err_text = map(decode_bytes, proc.communicate(mat1.tobytes() + mat2.tobytes()))
        retcode = proc.wait()
        if retcode != 0:
            sys.stderr.write(red(f"Multiplication of compatible matrices with dimensions {mat1.shape} * {mat2.shape} caused your code to exit with code {retcode}.\n"))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            if USE_VALGRIND:
                sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            TEST_FAILED(test_name)
            return True

        if result_err_text:
            sys.stderr.write(red(f"Multiplication of compatible matrices with dimensions {mat1.shape} * {mat2.shape} caused your code to print to standard error.\n"))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

        if USE_VALGRIND and os.path.isfile(VALGRIND_LOGFILE) and os.stat(VALGRIND_LOGFILE).st_size > 0:
            sys.stderr.write(red(f"Valgrind has detected a memory problem while running test \"{test_name}\":\n"))
            with open(VALGRIND_LOGFILE, 'r') as valgrind_logfile_rfd:
                valgrind_log_lines = valgrind_logfile_rfd.read().splitlines()
            sys.stderr.write('\n'.join('\t' + valgrind_log_line for valgrind_log_line in valgrind_log_lines))
            sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

        expected_mat = (mat1 @ mat2).astype(MatrixTests.MAT_DTYPE)
        actual_mat = MatrixTests.load_text_matrix(result_out_text)

        if not np.allclose(expected_mat, actual_mat, rtol = MatrixTests.MATMUL_REL_DEV, atol = MatrixTests.MATMUL_ABS_DEV):
            avg_dev = np.abs(np.average(expected_mat - actual_mat))
            sys.stderr.write(red(f"Multiplication of compatible matrices with dimensions {mat1.shape} * {mat2.shape} yielded a highly deviant results (abs avg dev = {avg_dev}).\n"))

            np.savetxt(EXPECTED_RESULTS_FILE, expected_mat)
            np.savetxt(ACTUAL_RESULTS_FILE, actual_mat)

            sys.stderr.write(DUMP_FILES_INFO)
            TEST_FAILED("valid_matmul")

    @staticmethod
    def valid_matadd(inplace = False):
        test_name = MatrixTests.VALID_MATADD_TEST_NAME.format("_inplace" if inplace else "")

        mat1 = MatrixTests.randmat(MatrixTests.MATADD_DIM_BOUNDS, MatrixTests.MATADD_ENTRY_BOUNDS)
        mat2 = MatrixTests.randmat(MatrixTests.MATADD_DIM_BOUNDS, MatrixTests.MATADD_ENTRY_BOUNDS, *mat1.shape)

        test_cmd = [*TESTS_BIN, "matadd_inplace" if inplace else "matadd", *map(str, mat1.shape + mat2.shape)]
        proc = sp.Popen(test_cmd, stdin = sp.PIPE, stdout = sp.PIPE, stderr = sp.PIPE)
        result_out_text, result_err_text = map(decode_bytes, proc.communicate(mat1.tobytes() + mat2.tobytes()))
        retcode = proc.wait()
        if retcode != 0:
            sys.stderr.write(red(f"""{"In-place a" if inplace else "A"}ddition of compatible matrices with dimensions {mat1.shape} + {mat2.shape} caused your code to exit with code {retcode}.\n"""))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            if USE_VALGRIND:
                sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            TEST_FAILED(test_name)
            return True

        if result_err_text:
            sys.stderr.write(red(f"""{"In-place a" if inplace else "A"}ddition of compatible matrices with dimensions {mat1.shape} + {mat2.shape} caused your code to print to standard error.\n"""))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

        if USE_VALGRIND and os.path.isfile(VALGRIND_LOGFILE) and os.stat(VALGRIND_LOGFILE).st_size > 0:
            sys.stderr.write(red(f"Valgrind has detected a memory problem while running test \"{test_name}\":\n"))
            with open(VALGRIND_LOGFILE, 'r') as valgrind_logfile_rfd:
                valgrind_log_lines = valgrind_logfile_rfd.read().splitlines()
            sys.stderr.write('\n'.join('\t' + valgrind_log_line for valgrind_log_line in valgrind_log_lines))
            sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

        expected_mat = (mat1 + mat2).astype(MatrixTests.MAT_DTYPE)
        actual_mat = MatrixTests.load_text_matrix(result_out_text)

        if not np.allclose(expected_mat, actual_mat, rtol = MatrixTests.MATMUL_REL_DEV, atol = MatrixTests.MATMUL_ABS_DEV):
            avg_dev = np.abs(np.average(expected_mat - actual_mat))
            sys.stderr.write(red(f"""{"In-place a" if inplace else "A"} of compatible matrices with dimensions {mat1.shape} + {mat2.shape} yielded a highly deviant results (abs avg dev = {avg_dev}).\n"""))

            np.savetxt(EXPECTED_RESULTS_FILE, expected_mat)
            np.savetxt(ACTUAL_RESULTS_FILE, actual_mat)

            sys.stderr.write(DUMP_FILES_INFO)
            TEST_FAILED(test_name)
            return True

    @staticmethod
    def valid_scalar_mat_mul(left = True):
        test_name = MatrixTests.VALID_SCALAR_MAT_MUL_TEST_NAME.format('l' if left else 'r')

        mat = MatrixTests.randmat(MatrixTests.SCALAR_MAT_MUL_DIM_BOUNDS, MatrixTests.SCALAR_MAT_MUL_ENTRY_BOUNDS)
        scalar = MatrixTests.MAT_DTYPE(np.random.uniform(*MatrixTests.SCALAR_BOUNDS))

        test_cmd = [*TESTS_BIN, f"scalar_mat_{'l' if left else 'r'}mul", *map(str, mat.shape)]
        proc = sp.Popen(test_cmd, stdin = sp.PIPE, stdout = sp.PIPE, stderr = sp.PIPE)
        result_out_text, result_err_text = map(decode_bytes, proc.communicate(np.array([scalar], dtype = MatrixTests.MAT_DTYPE).tobytes() + mat.tobytes()))
        retcode = proc.wait()
        if retcode != 0:
            sys.stderr.write(red(f"Multiplication of matrix with dimensions {mat.shape} with scalar caused your code to exit with code {retcode}.\n"))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            if USE_VALGRIND:
                sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            TEST_FAILED(test_name)
            return True

        if result_err_text:
            sys.stderr.write(red(f"Multiplication of matrix with dimensions {mat.shape} with scalar caused your code to print to standard error.\n"))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

        if USE_VALGRIND and os.path.isfile(VALGRIND_LOGFILE) and os.stat(VALGRIND_LOGFILE).st_size > 0:
            sys.stderr.write(red(f"Valgrind has detected a memory problem while running test \"{test_name}\":\n"))
            with open(VALGRIND_LOGFILE, 'r') as valgrind_logfile_rfd:
                valgrind_log_lines = valgrind_logfile_rfd.read().splitlines()
            sys.stderr.write('\n'.join('\t' + valgrind_log_line for valgrind_log_line in valgrind_log_lines))
            sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

        expected_mat = (scalar * mat).astype(MatrixTests.MAT_DTYPE)
        actual_mat = MatrixTests.load_text_matrix(result_out_text)

        if not np.allclose(expected_mat, actual_mat, rtol = MatrixTests.SCALAR_MAT_MUL_REL_DEV, atol = MatrixTests.SCALAR_MAT_MUL_ABS_DEV):
            avg_dev = np.abs(np.average(expected_mat - actual_mat))
            if left:
                sys.stderr.write(red(f"Multiplication of matrix with dimensions {mat.shape} with scalar yielded a highly deviant results (abs avg dev = {avg_dev}).\n"))
            else:
                sys.stderr.write(red(f"Multiplication of scalar with matrix with dimensions {mat.shape} yielded a highly deviant results (abs avg dev = {avg_dev}).\n"))

            np.savetxt(EXPECTED_RESULTS_FILE, expected_mat)
            np.savetxt(ACTUAL_RESULTS_FILE, actual_mat)

            sys.stderr.write(DUMP_FILES_INFO)
            TEST_FAILED(test_name)
            return True

    @staticmethod
    def valid_getitem(flat = False):
        test_name = MatrixTests.VALID_GETITEM_TEST_NAME.format("flat_" if flat else "")

        mat = MatrixTests.randmat(MatrixTests.GETITEM_DIM_BOUNDS, MatrixTests.GETITEM_ENTRY_BOUNDS)
        indices = MatrixTests.randint(low = 0, high = mat.size - 1, size = MatrixTests.randint(low = 1, high = mat.size))
        inp_indices = indices if flat else list(map(list, np.array(list(itertools.chain(*((index // mat.shape[1], index % mat.shape[1]) for index in indices)))).reshape(-1, 2)))

        test_cmd = [*TESTS_BIN, f"""{"flat_" if flat else ""}getitem""", *map(str, mat.shape), str(indices.size)]
        proc = sp.Popen(test_cmd, stdin = sp.PIPE, stdout = sp.PIPE, stderr = sp.PIPE)
        result_out_text, result_err_text = map(decode_bytes, proc.communicate(np.array(inp_indices).astype(np.uintp).tobytes() + mat.tobytes()))
        retcode = proc.wait()
        if retcode != 0:
            sys.stderr.write(red(f"""{"Flat-access" if flat else "Access"} to a valid item in matrix with dimensions {mat.shape} caused your code to exit with code {retcode}.\n"""))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            if USE_VALGRIND:
                sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            TEST_FAILED(test_name)
            return True


        if result_err_text:
            sys.stderr.write(red(f"""{"Flat-access" if flat else "Access"} to a valid item in matrix with dimensions {mat.shape} caused your code to print to standard error.\n"""))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

        if USE_VALGRIND and os.path.isfile(VALGRIND_LOGFILE) and os.stat(VALGRIND_LOGFILE).st_size > 0:
            sys.stderr.write(red(f"Valgrind has detected a memory problem while running test \"{test_name}\":\n"))
            with open(VALGRIND_LOGFILE, 'r') as valgrind_logfile_rfd:
                valgrind_log_lines = valgrind_logfile_rfd.read().splitlines()
            sys.stderr.write('\n'.join('\t' + valgrind_log_line for valgrind_log_line in valgrind_log_lines))
            sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

        expected_arr = mat.flatten()[indices].astype(MatrixTests.MAT_DTYPE)
        actual_arr = MatrixTests.load_text_matrix(result_out_text).flatten()

        equal_arr = expected_arr == actual_arr
        for i, equal_elem in enumerate(equal_arr):
            if not equal_elem:
                sys.stderr.write(red(f"""{"Flat-access" if flat else "Access"} to valid item in matrix with dimensions {mat.shape} """ \
                                     f"yielded a highly deviant result at {(i // mat.shape[1], i % mat.shape[1])} (expected: {expected_arr[i]}; actual: {actual_arr[i]}).\n"))

                np.savetxt(INP_FILE, mat)
                sys.stderr.write(INP_FILE_INFO)
                TEST_FAILED(test_name)
                return True

    @staticmethod
    def valid_setitem(flat = False):
        test_name = MatrixTests.VALID_SETITEM_TEST_NAME.format("flat_" if flat else "")

        mat = MatrixTests.randmat(MatrixTests.SETITEM_DIM_BOUNDS, MatrixTests.SETITEM_ENTRY_BOUNDS)
        indices = MatrixTests.randint(low = 0, high = mat.size - 1, size = MatrixTests.randint(low = 1, high = mat.size))
        inp_indices = indices if flat else [(index // mat.shape[1], index % mat.shape[1]) for index in indices]
        new_values = np.random.uniform(*MatrixTests.SCALAR_BOUNDS, size = indices.size).astype(MatrixTests.MAT_DTYPE)

        test_cmd = [*TESTS_BIN, f"""{"flat_" if flat else ""}setitem""", *map(str, mat.shape), str(indices.size)]
        proc = sp.Popen(test_cmd, stdin = sp.PIPE, stdout = sp.PIPE, stderr = sp.PIPE)
        result_out_text, result_err_text = map(decode_bytes, proc.communicate(np.array(inp_indices).astype(np.uintp).tobytes() + new_values.tobytes() + mat.tobytes()))
        retcode = proc.wait()
        if retcode != 0:
            sys.stderr.write(red(f"""Mutating an item in a matrix with dimensions {mat.shape}{" via flat-access" if flat else ""} caused your code to exit with code {retcode}.\n"""))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            if USE_VALGRIND:
                sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            TEST_FAILED(test_name)
            return True

        if result_err_text:
            sys.stderr.write(red(f"""Mutating an item in a matrix with dimensions {mat.shape}{" via flat-access" if flat else ""} caused your code to print to standard error.\n"""))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

        if USE_VALGRIND and os.path.isfile(VALGRIND_LOGFILE) and os.stat(VALGRIND_LOGFILE).st_size > 0:
            sys.stderr.write(red(f"Valgrind has detected a memory problem while running test \"{test_name}\":\n"))
            with open(VALGRIND_LOGFILE, 'r') as valgrind_logfile_rfd:
                valgrind_log_lines = valgrind_logfile_rfd.read().splitlines()
            sys.stderr.write('\n'.join('\t' + valgrind_log_line for valgrind_log_line in valgrind_log_lines))
            sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

        for i, inp_index in enumerate(inp_indices):
            mat[(inp_index // mat.shape[1], inp_index % mat.shape[1]) if flat else inp_index] = new_values[i]

        expected_mat = mat.astype(MatrixTests.MAT_DTYPE)
        actual_mat = MatrixTests.load_text_matrix(result_out_text)

        equal_mat = expected_mat == actual_mat
        for coord, equal_elem in np.ndenumerate(equal_mat):
            if flat:
                coord = (inp_index // mat.shape[1], inp_index % mat.shape[1])
            if not equal_elem:
                sys.stderr.write(red(f"""Mutating an item in a matrix with dimensions {mat.shape}{" via flat-access" if flat else ""} yielded a highly deviant entry at {coord} in the matrix """ \
                                     f"(expected: {expected_mat[coord]}; actual: {actual_mat[coord]}).\n"))

                np.savetxt(INP_FILE, mat)
                sys.stderr.write(INP_FILE_SHORT_INFO)
                np.savetxt(EXPECTED_RESULTS_FILE, expected_mat)
                np.savetxt(ACTUAL_RESULTS_FILE, actual_mat)
                sys.stderr.write(DUMP_FILES_INFO)
                TEST_FAILED(test_name)
                return True

    @staticmethod
    def invalid_matctor2():
        test_name = MatrixTests.INVALID_MATCTOR_TEST_NAME.format(2)
        dims = tuple(MatrixTests.randint(*MatrixTests.INVALID_MATCTOR_DIM_BOUNDS, size = 2))
        test_cmd = [*TESTS_BIN, "matctor2", *map(str, dims)]
        proc = sp.Popen(test_cmd, stdout = sp.PIPE, stderr = sp.PIPE)
        result_out_text, result_err_text = map(decode_bytes, (proc.stdout.read(), proc.stderr.read()))
        retcode = proc.wait()

        if retcode != 1:
            sys.stderr.write(red(f"Construction of matrix with invalid dimensions {dims} didn't cause an exit with code 1 (but rather {retcode}).\n"))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            if USE_VALGRIND:
                sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            TEST_FAILED(test_name)
            return True

        if result_out_text:
            sys.stderr.write(red(f"In construction of matrix with invalid dimensions {dims}, your code printed to standard output.\n"))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

        if not (result_err_text.startswith("Error:") and result_err_text.endswith('\n')):
            sys.stderr.write(red(f"In construction of matrix with invalid dimensions {dims}, your code should print to standard error " \
                                  "a message starting with \"Error:\" and ending with a newline.\n"))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

        if USE_VALGRIND_EXTRA and os.path.isfile(VALGRIND_LOGFILE) and os.stat(VALGRIND_LOGFILE).st_size > 0:
            sys.stderr.write(red(f"Valgrind has detected a memory problem while running test \"{test_name}\":\n"))
            with open(VALGRIND_LOGFILE, 'r') as valgrind_logfile_rfd:
                valgrind_log_lines = valgrind_logfile_rfd.read().splitlines()
            sys.stderr.write('\n'.join('\t' + valgrind_log_line for valgrind_log_line in valgrind_log_lines))
            sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

    @staticmethod
    def invalid_matmul():
        test_name = MatrixTests.INVALID_MATMUL_TEST_NAME

        mat1 = MatrixTests.randmat(MatrixTests.MATMUL_DIM_BOUNDS, MatrixTests.MATMUL_ENTRY_BOUNDS)
        mat2 = MatrixTests.randmat(MatrixTests.MATMUL_DIM_BOUNDS, MatrixTests.MATMUL_ENTRY_BOUNDS)
        while mat1.shape[1] == mat2.shape[0]: # Guarantee invalid matrix multiplication
            mat2 = MatrixTests.randmat(MatrixTests.MATMUL_DIM_BOUNDS, MatrixTests.MATMUL_ENTRY_BOUNDS)

        test_cmd = [*TESTS_BIN, "matmul", *map(str, mat1.shape + mat2.shape)]
        proc = sp.Popen(test_cmd, stdin = sp.PIPE, stdout = sp.PIPE, stderr = sp.PIPE)
        result_out_text, result_err_text = map(decode_bytes, proc.communicate(mat1.tobytes() + mat2.tobytes()))
        retcode = proc.wait()
        if retcode != 1:
            sys.stderr.write(red(f"Multiplication of incompatible matrices with dimensions {mat1.shape} * {mat2.shape} didn't cause an exit with code 1 (but rather {retcode}).\n"))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            if USE_VALGRIND:
                sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            TEST_FAILED(test_name)
            return True

        if result_out_text:
            sys.stderr.write(red(f"In multiplication of incompatible matrices with dimensions {mat1.shape} * {mat2.shape}, your code printed to standard output.\n"))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

        if not (result_err_text.startswith("Error:") and result_err_text.endswith('\n')):
            sys.stderr.write(red(f"In multiplication of incompatible matrices with dimensions {mat1.shape} * {mat2.shape}, your code should print to standard error " \
                                  "a message starting with \"Error:\" and ending with a newline.\n"))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

        if USE_VALGRIND_EXTRA and os.path.isfile(VALGRIND_LOGFILE) and os.stat(VALGRIND_LOGFILE).st_size > 0:
            sys.stderr.write(red(f"Valgrind has detected a memory problem while running test \"{test_name}\":\n"))
            with open(VALGRIND_LOGFILE, 'r') as valgrind_logfile_rfd:
                valgrind_log_lines = valgrind_logfile_rfd.read().splitlines()
            sys.stderr.write('\n'.join('\t' + valgrind_log_line for valgrind_log_line in valgrind_log_lines))
            sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

    @staticmethod
    def invalid_matadd(inplace = False):
        test_name = MatrixTests.INVALID_MATADD_TEST_NAME.format("_inplace" if inplace else "")

        mat1 = MatrixTests.randmat(MatrixTests.MATADD_DIM_BOUNDS, MatrixTests.MATADD_ENTRY_BOUNDS)
        mat2 = MatrixTests.randmat(MatrixTests.MATADD_DIM_BOUNDS, MatrixTests.MATADD_ENTRY_BOUNDS)
        while mat1.shape == mat2.shape: # Guarantee invalid matrix addition
            mat2 = MatrixTests.randmat(MatrixTests.MATMUL_DIM_BOUNDS, MatrixTests.MATMUL_ENTRY_BOUNDS)

        test_cmd = [*TESTS_BIN, "matadd_inplace" if inplace else "matadd", *map(str, mat1.shape + mat2.shape)]
        proc = sp.Popen(test_cmd, stdin = sp.PIPE, stdout = sp.PIPE, stderr = sp.PIPE)
        result_out_text, result_err_text = map(decode_bytes, proc.communicate(mat1.tobytes() + mat2.tobytes()))
        retcode = proc.wait()
        if retcode != 1:
            sys.stderr.write(red(f"Addition of incompatible matrices with dimensions {mat1.shape} + {mat2.shape} didn't cause an exit with code 1 (but rather {retcode}).\n"))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            if USE_VALGRIND:
                sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            TEST_FAILED(test_name)
            return True

        if result_out_text:
            sys.stderr.write(red(f"In addition of incompatible matrices with dimensions {mat1.shape} + {mat2.shape}, your code printed to standard output.\n"))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

        if not (result_err_text.startswith("Error:") and result_err_text.endswith('\n')):
            sys.stderr.write(red(f"In addition of incompatible matrices with dimensions {mat1.shape} + {mat2.shape}, your code should print to standard error " \
                                  "a message starting with \"Error:\" and ending with a newline.\n"))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

        if USE_VALGRIND_EXTRA and os.path.isfile(VALGRIND_LOGFILE) and os.stat(VALGRIND_LOGFILE).st_size > 0:
            sys.stderr.write(red(f"Valgrind has detected a memory problem while running test \"{test_name}\":\n"))
            with open(VALGRIND_LOGFILE, 'r') as valgrind_logfile_rfd:
                valgrind_log_lines = valgrind_logfile_rfd.read().splitlines()
            sys.stderr.write('\n'.join('\t' + valgrind_log_line for valgrind_log_line in valgrind_log_lines))
            sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

    @staticmethod
    def invalid_getitem(flat = False):
        test_name = MatrixTests.INVALID_GETITEM_TEST_NAME.format("flat_" if flat else "")

        mat = MatrixTests.randmat(MatrixTests.GETITEM_DIM_BOUNDS, MatrixTests.GETITEM_ENTRY_BOUNDS)
        index = MatrixTests.randint(low = mat.size, high = 2 * mat.size)
        inp_index = index if flat else (index // mat.shape[1], index % mat.shape[1])

        test_cmd = [*TESTS_BIN, f"""{"flat_" if flat else ""}getitem""", *map(str, mat.shape), '1']
        proc = sp.Popen(test_cmd, stdin = sp.PIPE, stdout = sp.PIPE, stderr = sp.PIPE)
        result_out_text, result_err_text = map(decode_bytes, proc.communicate(np.array(inp_index).astype(np.uintp).tobytes() + mat.tobytes()))
        retcode = proc.wait()
        if retcode != 1:
            sys.stderr.write(red(f"""{"Flat-access" if flat else "Access"} to an out-of-bounds item{(" [" + str(index) + "] ==") if flat else ""} """
                                 f"""{(index // mat.shape[1], index % mat.shape[1])} in matrix with dimensions {mat.shape} caused your code to exit with code {retcode}.\n"""))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            if USE_VALGRIND:
                sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            TEST_FAILED(test_name)
            return True


        if not (result_err_text.startswith("Error:") and result_err_text.endswith('\n')):
            sys.stderr.write(red(f"""In {"flat-access" if flat else "access"} to an out-of-bounds item{(" [" + str(index) + "] ==") if flat else ""} """
                                 f"""{(index // mat.shape[1], index % mat.shape[1])} in matrix with dimensions {mat.shape}, your code should print to standard error """ \
                                  "a message starting with \"Error:\" and ending with a newline.\n"))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

        if USE_VALGRIND_EXTRA and os.path.isfile(VALGRIND_LOGFILE) and os.stat(VALGRIND_LOGFILE).st_size > 0:
            sys.stderr.write(red(f"Valgrind has detected a memory problem while running test \"{test_name}\":\n"))
            with open(VALGRIND_LOGFILE, 'r') as valgrind_logfile_rfd:
                valgrind_log_lines = valgrind_logfile_rfd.read().splitlines()
            sys.stderr.write('\n'.join('\t' + valgrind_log_line for valgrind_log_line in valgrind_log_lines))
            sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

    @staticmethod
    def invalid_setitem(flat = False):
        test_name = MatrixTests.INVALID_SETITEM_TEST_NAME.format("flat_" if flat else "")

        mat = MatrixTests.randmat(MatrixTests.SETITEM_DIM_BOUNDS, MatrixTests.SETITEM_ENTRY_BOUNDS)
        index = MatrixTests.randint(low = mat.size, high = 2 * mat.size)
        inp_index = index if flat else (index // mat.shape[1], index % mat.shape[1])
        new_value = np.random.uniform(*MatrixTests.SCALAR_BOUNDS)

        test_cmd = [*TESTS_BIN, f"""{"flat_" if flat else ""}setitem""", *map(str, mat.shape), '1']
        proc = sp.Popen(test_cmd, stdin = sp.PIPE, stdout = sp.PIPE, stderr = sp.PIPE)
        result_out_text, result_err_text = map(decode_bytes, proc.communicate(np.array(inp_index).astype(np.uintp).tobytes() + \
                                                                              np.array(new_value).astype(MatrixTests.MAT_DTYPE).tobytes() + mat.tobytes()))
        retcode = proc.wait()
        if retcode != 1:
            sys.stderr.write(red(f"""{"Flat-access" if flat else "Access"} mutation of an out-of-bounds item{(" [" + str(index) + "] ==") if flat else ""} """
                                 f"""{(index // mat.shape[1], index % mat.shape[1])} in matrix with dimensions {mat.shape} caused your code to exit with code {retcode}.\n"""))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            if USE_VALGRIND:
                sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            TEST_FAILED(test_name)
            return True


        if not (result_err_text.startswith("Error:") and result_err_text.endswith('\n')):
            sys.stderr.write(red(f"""In {"flat-access" if flat else "access"} mutation of an out-of-bounds item{(" [" + str(index) + "] ==") if flat else ""} """
                                 f"""{(index // mat.shape[1], index % mat.shape[1])} in matrix with dimensions {mat.shape}, your code should print to standard error """ \
                                  "a message starting with \"Error:\" and ending with a newline.\n"))
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

        if USE_VALGRIND_EXTRA and os.path.isfile(VALGRIND_LOGFILE) and os.stat(VALGRIND_LOGFILE).st_size > 0:
            sys.stderr.write(red(f"Valgrind has detected a memory problem while running test \"{test_name}\":\n"))
            with open(VALGRIND_LOGFILE, 'r') as valgrind_logfile_rfd:
                valgrind_log_lines = valgrind_logfile_rfd.read().splitlines()
            sys.stderr.write('\n'.join('\t' + valgrind_log_line for valgrind_log_line in valgrind_log_lines))
            sys.stderr.write('\n' + VALGRIND_LOGFILE_INFO)
            with open(STDERR_DUMP_FILE, 'w') as stderr_dump_wfd:
                stderr_dump_wfd.write(result_err_text)
            sys.stderr.write(STDERR_FILE_INFO)
            TEST_FAILED(test_name)
            return True

    def __init__(self, tests_type):
        MatrixTests.MAT_DTYPE = np.float32

        MatrixTests.VALID_MATCTOR_TEST_NAME = "valid_matctor{}"
        MatrixTests.INVALID_MATCTOR_TEST_NAME = "invalid_matctor{}"
        MatrixTests.MATCTOR_DIM_BOUNDS = [1, 200] if not USE_VALGRIND else [1, 20]
        MatrixTests.INVALID_MATCTOR_DIM_BOUNDS = [-5, 0]
        MatrixTests.MATCTOR_ENTRY_BOUNDS = [-100., 100.]
        MatrixTests.MATCTOR_REL_DEV = 0. # rtol for allclose between matrices
        MatrixTests.MATCTOR_ABS_DEV = 0. # atol for allclose between matrices
        MatrixTests.MATCTOR_ITERS = 100 if not USE_VALGRIND else 10

        MatrixTests.VALID_MATMUL_TEST_NAME = "valid_matmul"
        MatrixTests.INVALID_MATMUL_TEST_NAME = "invalid_matmul"
        MatrixTests.MATMUL_REL_DEV = 1e-3 # rtol for allclose between matrices
        MatrixTests.MATMUL_ABS_DEV = 1e-1 # atol for allclose between matrices
        MatrixTests.MATMUL_DIM_BOUNDS = [1, 200] if not USE_VALGRIND else [1, 20]
        MatrixTests.MATMUL_ENTRY_BOUNDS = [-100., 100.]
        MatrixTests.MATMUL_ITERS = 100 if not USE_VALGRIND else 10

        MatrixTests.VALID_MATADD_TEST_NAME = "valid_matadd{}"
        MatrixTests.INVALID_MATADD_TEST_NAME = "invalid_matadd{}"
        MatrixTests.MATADD_REL_DEV = 0. # rtol for allclose between matrices
        MatrixTests.MATADD_ABS_DEV = 0. # atol for allclose between matrices
        MatrixTests.MATADD_DIM_BOUNDS = [1, 200] if not USE_VALGRIND else [1, 20]
        MatrixTests.MATADD_ENTRY_BOUNDS = [-100., 100.]
        MatrixTests.MATADD_ITERS = 100 if not USE_VALGRIND else 10

        MatrixTests.MATIO_PREMATURE_EOF_TEST_NAME = "matio_premature_eof"
        MatrixTests.MATIO_MISSING_EOF_TEST_NAME = "matio_missing_eof"
        MatrixTests.MATIO_DIM_BOUNDS = [1, 200] if not USE_VALGRIND else [1, 20]
        MatrixTests.MATIO_ENTRY_BOUNDS = [-100., 100.]
        MatrixTests.MATIO_ITERS = 100 if not USE_VALGRIND else 10

        MatrixTests.MATASSIGN_TEST_NAME = "matassign"
        MatrixTests.MATASSIGN_REL_DEV = 0. # rtol for allclose between matrices
        MatrixTests.MATASSIGN_ABS_DEV = 0. # atol for allclose between matrices
        MatrixTests.MATASSIGN_DIM_BOUNDS = [1, 200] if not USE_VALGRIND else [1, 20]
        MatrixTests.MATASSIGN_ENTRY_BOUNDS = [-100., 100.]
        MatrixTests.MATASSIGN_ITERS = 100 if not USE_VALGRIND else 10

        MatrixTests.VALID_SCALAR_MAT_MUL_TEST_NAME = "valid_scalar_mat_{}mul"
        MatrixTests.INVALID_SCALAR_MAT_MUL_TEST_NAME = "invalid_scalar_mat_{}mul"
        MatrixTests.SCALAR_MAT_MUL_REL_DEV = 0. # rtol for allclose between matrices
        MatrixTests.SCALAR_MAT_MUL_ABS_DEV = 0. # atol for allclose between matrices
        MatrixTests.SCALAR_MAT_MUL_DIM_BOUNDS = [1, 200] if not USE_VALGRIND else [1, 20]
        MatrixTests.SCALAR_MAT_MUL_ENTRY_BOUNDS = [-100., 100.]
        MatrixTests.SCALAR_MAT_MUL_ITERS = 100 if not USE_VALGRIND else 10
        MatrixTests.SCALAR_BOUNDS = [-100., 100.]

        MatrixTests.VALID_GETITEM_TEST_NAME = "valid_{}getitem"
        MatrixTests.INVALID_GETITEM_TEST_NAME = "invalid_{}getitem"
        MatrixTests.GETITEM_DIM_BOUNDS = [1, 200] if not USE_VALGRIND else [1, 20]
        MatrixTests.GETITEM_ENTRY_BOUNDS = [-100., 100.]
        MatrixTests.GETITEM_ITERS = 500 if not USE_VALGRIND else 10

        MatrixTests.VALID_SETITEM_TEST_NAME = "valid_{}setitem"
        MatrixTests.INVALID_SETITEM_TEST_NAME = "invalid_{}setitem"
        MatrixTests.SETITEM_DIM_BOUNDS = [1, 200] if not USE_VALGRIND else [1, 20]
        MatrixTests.SETITEM_ENTRY_BOUNDS = [-100., 100.]
        MatrixTests.SETITEM_ITERS = 100 if not USE_VALGRIND else 10

        passed = True
        if tests_type == "valid_construction":
            sys.stdout.write(title("VALID MATRIX CONSTRUCTION TESTS"))

            sys.stderr.write("[Matrix default constructor: Matrix::Matrix()]\n")
            if not MatrixTests.matctor0():
                TEST_PASSED(MatrixTests.VALID_MATCTOR_TEST_NAME.format(0))
                sys.stderr.write('\n')

            sys.stderr.write("[Matrix copy-constructor: Matrix::Matrix(Matrix const&)]\n")
            with tqdm.tqdm(total = MatrixTests.MATCTOR_ITERS, file = sys.stderr, leave = False) as pbar:
                for _ in range(MatrixTests.MATCTOR_ITERS):
                    if MatrixTests.matctor1():
                        passed = False
                        break
                    pbar.update(1)
                pbar.leave = passed
            if passed:
                TEST_PASSED(MatrixTests.VALID_MATCTOR_TEST_NAME.format(1))
                sys.stderr.write('\n')
            else:
                passed = True

            sys.stderr.write("[Matrix dimension-wise constructor: Matrix::Matrix(integral, integral)]\n")
            with tqdm.tqdm(total = MatrixTests.MATCTOR_ITERS, file = sys.stderr, leave = False) as pbar:
                for _ in range(MatrixTests.MATCTOR_ITERS):
                    if MatrixTests.valid_matctor2():
                        passed = False
                        break
                    pbar.update(1)
                pbar.leave = passed
            if passed:
                TEST_PASSED(MatrixTests.VALID_MATCTOR_TEST_NAME.format(2))
            else:
                passed = True

        elif tests_type == "invalid_construction":
            sys.stdout.write(title("INVALID MATRIX CONSTRUCTION TESTS"))

            sys.stderr.write("[Dimension-wise constructor with invalid arguments: Matrix::Matrix(integral, integral)]\n")
            with tqdm.tqdm(total = MatrixTests.MATCTOR_ITERS, file = sys.stderr, leave = False) as pbar:
                for _ in range(MatrixTests.MATCTOR_ITERS):
                    if MatrixTests.invalid_matctor2():
                        passed = False
                        break
                    pbar.update(1)
                pbar.leave = passed
            if passed:
                TEST_PASSED(MatrixTests.INVALID_MATCTOR_TEST_NAME.format(2))
            else:
                passed = True

        elif tests_type == "invalid_io":
            sys.stdout.write(title("INVALID MATRIX IO TESTS"))

            sys.stderr.write("[Premature EOF when loading matrix: operator>> between istream and Matrix]\n")
            with tqdm.tqdm(total = MatrixTests.MATIO_ITERS, file = sys.stderr, leave = False) as pbar:
                for _ in range(MatrixTests.MATIO_ITERS):
                    if MatrixTests.premature_eof():
                        passed = False
                        break
                    pbar.update(1)
                pbar.leave = passed
            if passed:
                TEST_PASSED(MatrixTests.MATIO_PREMATURE_EOF_TEST_NAME)
                sys.stderr.write('\n')
            else:
                passed = True

            sys.stderr.write("[Missing EOF at end when loading matrix: operator>> between istream and Matrix]\n")
            with tqdm.tqdm(total = MatrixTests.MATIO_ITERS, file = sys.stderr, leave = False) as pbar:
                for _ in range(MatrixTests.MATIO_ITERS):
                    if MatrixTests.missing_eof():
                        passed = False
                        break
                    pbar.update(1)
                pbar.leave = passed
            if passed:
                TEST_PASSED(MatrixTests.MATIO_MISSING_EOF_TEST_NAME)
                sys.stderr.write('\n')
            else:
                passed = True

        elif tests_type == "valid_arithmetic":
            sys.stdout.write(title("VALID MATRIX ARITHMETIC TESTS"))

            sys.stderr.write("[Matrix assignment: operator= between matrices]\n")
            with tqdm.tqdm(total = MatrixTests.MATASSIGN_ITERS, file = sys.stderr, leave = False) as pbar:
                for _ in range(MatrixTests.MATASSIGN_ITERS):
                    if MatrixTests.matassign():
                        passed = False
                        break
                    pbar.update(1)
                pbar.leave = passed
            if passed:
                TEST_PASSED(MatrixTests.MATASSIGN_TEST_NAME)
                sys.stderr.write('\n')
            else:
                passed = True

            sys.stderr.write("[Matrix multiplication: operator* between matrices]\n")
            with tqdm.tqdm(total = MatrixTests.MATMUL_ITERS, file = sys.stderr, leave = False) as pbar:
                for _ in range(MatrixTests.MATMUL_ITERS):
                    if MatrixTests.valid_matmul():
                        passed = False
                        break
                    pbar.update(1)
                pbar.leave = passed
            if passed:
                TEST_PASSED(MatrixTests.VALID_MATMUL_TEST_NAME)
                sys.stderr.write('\n')
            else:
                passed = True

            sys.stderr.write("[Matrix-scalar multiplication: operator* between matrix and scalar]\n")
            with tqdm.tqdm(total = MatrixTests.SCALAR_MAT_MUL_ITERS, file = sys.stderr, leave = False) as pbar:
                for _ in range(MatrixTests.SCALAR_MAT_MUL_ITERS):
                    if MatrixTests.valid_scalar_mat_mul(left = False):
                        passed = False
                        break
                    pbar.update(1)
                pbar.leave = passed
            if passed:
                TEST_PASSED(MatrixTests.VALID_SCALAR_MAT_MUL_TEST_NAME.format('r'))
                sys.stderr.write('\n')
            else:
                passed = True

            sys.stderr.write("[Scalar-matrix multiplication: operator* between scalar and matrix]\n")
            with tqdm.tqdm(total = MatrixTests.SCALAR_MAT_MUL_ITERS, file = sys.stderr, leave = False) as pbar:
                for _ in range(MatrixTests.SCALAR_MAT_MUL_ITERS):
                    if MatrixTests.valid_scalar_mat_mul(left = True):
                        passed = False
                        break
                    pbar.update(1)
                pbar.leave = passed
            if passed:
                TEST_PASSED(MatrixTests.VALID_SCALAR_MAT_MUL_TEST_NAME.format('l'))
                sys.stderr.write('\n')
            else:
                passed = True

            sys.stderr.write("[Matrix addition: operator+ between matrices]\n")
            with tqdm.tqdm(total = MatrixTests.MATADD_ITERS, file = sys.stderr, leave = False) as pbar:
                for _ in range(MatrixTests.MATADD_ITERS):
                    if MatrixTests.valid_matadd():
                        passed = False
                        break
                    pbar.update(1)
                pbar.leave = passed
            if passed:
                TEST_PASSED(MatrixTests.VALID_MATADD_TEST_NAME.format(""))
                sys.stderr.write('\n')
            else:
                passed = True

            sys.stderr.write("[In-place matrix addition: operator+= between matrices]\n")
            with tqdm.tqdm(total = MatrixTests.MATADD_ITERS, file = sys.stderr, leave = False) as pbar:
                for _ in range(MatrixTests.MATADD_ITERS):
                    if MatrixTests.valid_matadd(inplace = True):
                        passed = False
                        break
                    pbar.update(1)
                pbar.leave = passed
            if passed:
                TEST_PASSED(MatrixTests.VALID_MATADD_TEST_NAME.format("_inplace"))
                sys.stderr.write('\n')
            else:
                passed = True

            sys.stderr.write("[Matrix flat-access: operator[] on matrix]\n")
            with tqdm.tqdm(total = MatrixTests.GETITEM_ITERS, file = sys.stderr, leave = False) as pbar:
                for _ in range(MatrixTests.GETITEM_ITERS):
                    if MatrixTests.valid_getitem(flat = True):
                        passed = False
                        break
                    pbar.update(1)
                pbar.leave = passed
            if passed:
                TEST_PASSED(MatrixTests.VALID_GETITEM_TEST_NAME.format("flat_"))
                sys.stderr.write('\n')
            else:
                passed = True

            sys.stderr.write("[Matrix access: operator() on matrix]\n")
            with tqdm.tqdm(total = MatrixTests.GETITEM_ITERS, file = sys.stderr, leave = False) as pbar:
                for _ in range(MatrixTests.GETITEM_ITERS):
                    if MatrixTests.valid_getitem(flat = False):
                        passed = False
                        break
                    pbar.update(1)
                pbar.leave = passed
            if passed:
                TEST_PASSED(MatrixTests.VALID_GETITEM_TEST_NAME.format(""))
                sys.stderr.write('\n')
            else:
                passed = True

            sys.stderr.write("[Matrix flat-access mutation: setting item via operator[] on matrix]\n")
            with tqdm.tqdm(total = MatrixTests.SETITEM_ITERS, file = sys.stderr, leave = False) as pbar:
                for _ in range(MatrixTests.SETITEM_ITERS):
                    if MatrixTests.valid_setitem(flat = True):
                        passed = False
                        break
                    pbar.update(1)
                pbar.leave = passed
            if passed:
                TEST_PASSED(MatrixTests.VALID_SETITEM_TEST_NAME.format("flat_"))
                sys.stderr.write('\n')
            else:
                passed = True

            sys.stderr.write("[Matrix mutation: setting item via operator() on matrix]\n")
            with tqdm.tqdm(total = MatrixTests.SETITEM_ITERS, file = sys.stderr, leave = False) as pbar:
                for _ in range(MatrixTests.SETITEM_ITERS):
                    if MatrixTests.valid_setitem(flat = False):
                        passed = False
                        break
                    pbar.update(1)
                pbar.leave = passed
            if passed:
                TEST_PASSED(MatrixTests.VALID_SETITEM_TEST_NAME.format(""))
                sys.stderr.write('\n')
            else:
                passed = True

            sys.stdout.write(green("Valid matrix arithmetic tests passed succesfully.\n"))

        elif tests_type == "invalid_arithmetic":
            sys.stdout.write(title("INVALID MATRIX ARITHMETIC TESTS"))

            sys.stderr.write("[Invalid matrix multiplication: operator* between incompatible matrices]\n")
            with tqdm.tqdm(total = MatrixTests.MATMUL_ITERS, file = sys.stderr, leave = False) as pbar:
                for _ in range(MatrixTests.MATMUL_ITERS):
                    if MatrixTests.invalid_matmul():
                        passed = False
                        break
                    pbar.update(1)
                pbar.leave = passed
            if passed:
                TEST_PASSED(MatrixTests.INVALID_MATMUL_TEST_NAME)
                sys.stderr.write('\n')
            else:
                passed = True

            sys.stderr.write("[Invalid matrix addition: operator+ between incompatible matrices]\n")
            with tqdm.tqdm(total = MatrixTests.MATADD_ITERS, file = sys.stderr, leave = False) as pbar:
                for _ in range(MatrixTests.MATADD_ITERS):
                    if MatrixTests.invalid_matadd():
                        passed = False
                        break
                    pbar.update(1)
                pbar.leave = passed
            if passed:
                TEST_PASSED(MatrixTests.INVALID_MATADD_TEST_NAME.format(""))
                sys.stderr.write('\n')
            else:
                passed = True

            sys.stderr.write("[Invalid in-place matrix addition: operator+= between incompatible matrices]\n")
            with tqdm.tqdm(total = MatrixTests.MATADD_ITERS, file = sys.stderr, leave = False) as pbar:
                for _ in range(MatrixTests.MATADD_ITERS):
                    if MatrixTests.invalid_matadd(inplace = True):
                        passed = False
                        break
                    pbar.update(1)
                pbar.leave = passed
            if passed:
                TEST_PASSED(MatrixTests.INVALID_MATADD_TEST_NAME.format("_inplace"))
                sys.stderr.write('\n')
            else:
                passed = True

            sys.stderr.write("[Invalid matrix flat-access: out-of-bounds operator[] on matrices]\n")
            with tqdm.tqdm(total = MatrixTests.GETITEM_ITERS, file = sys.stderr, leave = False) as pbar:
                for _ in range(MatrixTests.GETITEM_ITERS):
                    if MatrixTests.invalid_getitem(flat = True):
                        passed = False
                        break
                    pbar.update(1)
                pbar.leave = passed
            if passed:
                TEST_PASSED(MatrixTests.INVALID_GETITEM_TEST_NAME.format("flat_"))
                sys.stderr.write('\n')

            sys.stderr.write("[Invalid matrix access: out-of-bounds operator() on matrices]\n")
            with tqdm.tqdm(total = MatrixTests.GETITEM_ITERS, file = sys.stderr, leave = False) as pbar:
                for _ in range(MatrixTests.GETITEM_ITERS):
                    if MatrixTests.invalid_getitem(flat = False):
                        passed = False
                        break
                    pbar.update(1)
                pbar.leave = passed
            if passed:
                TEST_PASSED(MatrixTests.INVALID_GETITEM_TEST_NAME.format(""))
                sys.stderr.write('\n')
            else:
                passed = True

            sys.stderr.write("[Invalid matrix flat-access mutation: out-of-bounds operator[] on matrices]\n")
            with tqdm.tqdm(total = MatrixTests.SETITEM_ITERS, file = sys.stderr, leave = False) as pbar:
                for _ in range(MatrixTests.SETITEM_ITERS):
                    if MatrixTests.invalid_setitem(flat = True):
                        passed = False
                        break
                    pbar.update(1)
                pbar.leave = passed
            if passed:
                TEST_PASSED(MatrixTests.INVALID_SETITEM_TEST_NAME.format("flat_"))
                sys.stderr.write('\n')
            else:
                passed = True

            sys.stderr.write("[Invalid matrix mutation: out-of-bounds operator() on matrices]\n")
            with tqdm.tqdm(total = MatrixTests.SETITEM_ITERS, file = sys.stderr, leave = False) as pbar:
                for _ in range(MatrixTests.SETITEM_ITERS):
                    if MatrixTests.invalid_setitem(flat = False):
                        passed = False
                        break
                    pbar.update(1)
                pbar.leave = passed
            if passed:
                TEST_PASSED(MatrixTests.INVALID_SETITEM_TEST_NAME.format(""))
                sys.stderr.write('\n')
            else:
                passed = True

            sys.stdout.write(green("Invalid matrix arithmetic tests passed succesfully.\n"))

class DigitTests:
    def __init__(self):
        DigitTests.DIGIT_ITERS = None if not USE_VALGRIND else 10

        sys.stdout.write(title("DIGIT RECOGNITION TESTS"))
        filenames = list(os.walk("mnist_data"))[0][2][:DigitTests.DIGIT_ITERS]
        with tqdm.tqdm(total = len(filenames), file = sys.stderr, leave = False) as pbar:
            for filename in filenames:
                mnist_filename = os.path.join("mnist_data", filename)
                school_result_filename = os.path.join("mnist_school_results", filename)
                with open(school_result_filename, 'r') as school_result_rfd:
                    school_result = school_result_rfd.read()

                test_cmd = [*TESTS_BIN, "digit", mnist_filename]
                proc = sp.Popen(test_cmd, stdout = sp.PIPE)
                actual_result = proc.stdout.read().decode()
                proc.stdout.close()
                proc.wait()

                if actual_result != school_result:
                    sys.stderr.write(red(f"Digit recognition for image {mnist_filename} produced results different from the school solution.\n"))

                    if FAST:
                        sys.stderr.write(yellow("If you only find a small difference in the digit prediction probability, consider running the tests again without --fast.\n"))

                    sys.stderr.write("In addition to bad recognition, this can happen if you print images (operator<<) incorrectly " \
                                     "or due to floating-point arithmetic deviations.\n")
                    with open(EXPECTED_RESULTS_FILE, 'w') as expected_wfd, open(ACTUAL_RESULTS_FILE, 'w') as actual_wfd:
                        expected_wfd.write(school_result)
                        actual_wfd.write(actual_result)

                    sys.stderr.write(DIGIT_DUMP_FILES_INFO)
                    TEST_FAILED("digit_recognition")

                pbar.update(1)
            pbar.leave = True

        sys.stdout.write(green("Digit recognition tests passed succesfully.\n"))

if __name__ == "__main__":
    import argparse
    import time

    parser = argparse.ArgumentParser(description = "Tests for C++ exercise 4 in HUJI C/C++ course (67315), June 2020, by Ariel Terkeltoub.")
    parser.add_argument("-a", "--all", help = "Run all algorithmic tests.", action = "store_true")
    parser.add_argument("--fast", help = "Maximize compile-time optimizations (dangerous).", action = "store_true")
    parser.add_argument("--persist", help = "Keep testing even after a test has failed.", action = "store_true")

    valgrind_group = parser.add_mutually_exclusive_group()
    valgrind_group.add_argument("--valgrind", help = "Run the tests under Valgrind, as per the exercise instructions.", action = "store_true")
    valgrind_group.add_argument("--valgrind-extra", help = "Run the tests under Valgrind and report ANY memory errors (including ones that the exercise instructions permit).", action = "store_true")
    parser.add_argument("--valid-construction", help = "Run valid matrix construction tests.", action = "store_true")
    parser.add_argument("--invalid-io", help = "Run invalid matrix IO tests.", action = "store_true")
    parser.add_argument("--invalid-construction", help = "Run invalid matrix construction tests.", action = "store_true")
    parser.add_argument("--valid-arithmetic", help = "Run valid matrix arithmetic tests.", action = "store_true")
    parser.add_argument("--invalid-arithmetic", help = "Run invalid matrix arithmetic tests.", action = "store_true")
    parser.add_argument("--digit-recognition", help = "Run digit recognition tests.", action = "store_true")

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args() # Only for the help message and filtering of bad arguments

    if args.persist:
        PERSIST = True

    if args.valgrind or args.valgrind_extra:
        sys.stderr.write(yellow("WARNING: when using Valgrind, the testing scale is automatically reduced, but it will still take some time.\n"))
        if shutil.which(VALGRIND_BIN) is None:
            sys.stderr.write(red("Valgrind not found. Aborting tests.\n", bold = True))
            sys.exit(1)

        USE_VALGRIND = True
        USE_VALGRIND_EXTRA = args.valgrind_extra
        with open(VALGRIND_LOGFILE, 'w'): # Only touch the file (and empty it)
            pass
        TESTS_BIN = [VALGRIND_BIN, "-q", "--leak-check=full", "--show-leak-kinds=all", "--track-origins=yes", f"--log-file={VALGRIND_LOGFILE}", *TESTS_BIN]
        CXXFLAGS.extend(["-g", "-Og"])

    if args.fast:
        FAST = True
        CXXFLAGS.extend(["-Ofast", "-funroll-loops", "-finline-functions", "-flto", "-fopenmp", "-D_GLIBCXX_PARALLEL", "-ffast-math", "-march=native", "-ftree-vectorize", "-fopt-info-vec-optimized"])


    TestsIntegrity()
    sys.stderr.write("\n\n")
    Compile(HEADERS, SOURCES)
    sys.stderr.write("\n\n")


    stime = time.time()
    performed = []
    for i, arg in enumerate(sys.argv[1:]):
        if (arg == "--valid-construction" or args.all) and "--valid-construction" not in performed:
            # Test valid matrix construction
            MatrixTests(tests_type = "valid_construction")
            performed.append("--valid-construction")
            if i != len(sys.argv) - 2:
                sys.stderr.write("\n\n")
        if (arg == "--invalid-construction" or args.all) and "--invalid-construction" not in performed:
            # Test invalid matrix construction
            MatrixTests(tests_type = "invalid_construction")
            performed.append("--invalid-construction")
            if i != len(sys.argv) - 2:
                sys.stderr.write("\n\n")
        if (arg == "--invalid-io" or args.all) and "--invalid-io" not in performed:
            # Test invalid matrix IO
            MatrixTests(tests_type = "invalid_io")
            performed.append("--invalid-io")
            if i != len(sys.argv) - 2:
                sys.stderr.write("\n\n")
        if (arg == "--valid-arithmetic" or args.all) and "--valid-arithmetic" not in performed:
            # Test valid matrix arithmetic
            MatrixTests(tests_type = "valid_arithmetic")
            performed.append("--valid-arithmetic")
            if i != len(sys.argv) - 2:
                sys.stderr.write("\n\n")
        if (arg == "--invalid-arithmetic" or args.all) and "--invalid-arithmetic" not in performed:
            # Test invalid matrix arithmetic
            MatrixTests(tests_type = "invalid_arithmetic")
            performed.append("--invalid-arithmetic")
            if i != len(sys.argv) - 2:
                sys.stderr.write("\n\n")
        if (arg == "--digit-recognition" or args.all) and "--digit-recognition" not in performed:
            # Test digit recognition
            DigitTests()
            performed.append("--digit-recognition")
            if i != len(sys.argv) - 2:
                sys.stderr.write("\n\n")

    if PERSIST_USED:
        sys.stdout.write(red(PERSIST_USED, bold = True))
    else:
        sys.stdout.write(green(f"""All tests passed successfully!{" No memory problems have been found." if USE_VALGRIND else ""} Time elapsed: {time.time() - stime:.3f}s.""", bold = True))
        sys.stdout.flush()
        with open(CRUCIAL_DATA_FILENAME, 'r') as crucial_data_rfd:
            lines = crucial_data_rfd.readlines()
            crucial_line = np.random.choice(lines).strip()
            sys.stderr.write(green(f" Fun remark: {crucial_line}\n"))
