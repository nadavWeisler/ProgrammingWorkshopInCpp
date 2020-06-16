#########################################
############ TEST CPP - EX1 #############
#########################################
# If you found a bug in the test you can always send an email to me:
# amit.david@mail.huji.ac.il
#
# HOW TO RUN
# 1) Place all of the project '.c' files in './in' folder
# 2) Run in terminal using 'python3 cpp_ex1.py'
# 3) Results will be shown in terminal
#########################################
import difflib
import subprocess

PYTHON_VER = f"If you see this error message, you are using python 2.x instead of 3.7"

ARGS = " param/w1 param/w2 param/w3 param/w4 param/b1 param/b2 param/b3 param/b4"

# File types
IN = "in"
OUT = "out"
CMP = "cmp"
VAL = "val"


#########################################
def convert_file_name(name, loc):
    return f"{loc}/{name}.{loc}"


def cmp_files(cmp_file, out_file):
    with open(cmp_file, 'r') as fCmp:
        with open(out_file, 'r') as fOut:
            diff = difflib.ndiff(fOut.readlines(), fCmp.readlines())

            for i, line in enumerate(diff):
                if line.startswith("- ") or line.startswith("+ ") or line.startswith("? "):
                    print("\tOutput test - FAIL")
                    print("\tDifference found in '" + out_file + "' at line " + str(i))
                    return

            print("\tOutput test - PASS")


def check_valgrind_file(val_file):
    check_lines = -1

    with open(val_file, 'r') as fVal:
        for line in fVal.readlines():
            if "LEAK SUMMARY:" in line:
                check_lines = 0

            if 0 <= check_lines < 5:
                check_lines += 1
                if ": 0 bytes in 0 blocks" not in line:
                    print("\tValgrind test - FAIL")
                    print("\tMemory leak found, more info in '" + val_file + "'")
                    return

            if "ERROR SUMMARY:" in line and "ERROR SUMMARY: 0 errors from" not in line:
                print("\tValgrind test - FAIL")
                print("\tError found, more info in '" + val_file + "'")
                return

    print("\tValgrind test - PASS")


def t_file(file_name, extra_file=False):
    in_file = f"in/{file_name}"
    input_file = convert_file_name(file_name, IN)
    out_file = convert_file_name(file_name, OUT)
    cmp_file = convert_file_name(file_name, CMP)
    val_file = convert_file_name(file_name, VAL)

    with open(out_file, 'w') as fOut:
        try:
            program = "valgrind --leak-check=full --log-file=" + val_file + " " + in_file + ARGS

            if extra_file:
                with open(input_file, 'r') as fIn:
                    subprocess.run(program, stdin=fIn, stdout=fOut, stderr=subprocess.STDOUT, shell=True, timeout=6)
            else:
                subprocess.run(program, stdout=fOut, stderr=subprocess.STDOUT, shell=True, timeout=10)

        except subprocess.TimeoutExpired:
            print("\tTest - FAIL")
            print("\tTIMEOUT Reached")
            return

    cmp_files(cmp_file, out_file)
    check_valgrind_file(val_file)


def t_no_valg(file_name):
    in_file = f"in/{file_name}"
    out_file = convert_file_name(file_name, OUT)
    cmp_file = convert_file_name(file_name, CMP)

    with open(out_file, 'w') as fOut:
        try:
            program = in_file + ARGS
            subprocess.run(program, stdout=fOut, stderr=subprocess.DEVNULL, shell=True, timeout=6)

        except subprocess.TimeoutExpired:
            print("\tTest - FAIL")
            print("\tTIMEOUT Reached")
            return

    cmp_files(cmp_file, out_file)


#########################################
if __name__ == "__main__":
    print("\n------- COMPILATION START -------")

    print("Compile your files and place binaries at './in' folder...")

    if subprocess.run("(cd in; make all)", text=True, shell=True).returncode != 0:
        print("\nProgram failed compiling")
        exit(1)

    print("------- COMPILATION END - The section above should have no warnings nor errors -------")
    print("\nProgram compiled successfully")

    print("\n------- TEST START -------")

    print("Test for school solution for given images")
    t_file('mlpnetwork', True)
    print()

    print("Test for large data set (No valgrind)")
    t_no_valg('simple_main')
    print()

    print("Test valid matrix")
    t_file('matrix_valid')
    print()

    print("Test invalid matrix (No valgrind)")
    t_no_valg('matrix_invalid')
    print()

    print("------- TEST END -------")
