import subprocess
import sys

def run_tests():
    print("Running tests...")
    result = subprocess.run([sys.executable, "-m", "pytest", "tests/"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode == 0:
        print("All tests passed successfully.")
    else:
        print("Some tests failed. Please check the details above.")
    with open("tests/test_report.txt", "w") as f:
        f.write(result.stdout)

if __name__ == "__main__":
    run_tests()
