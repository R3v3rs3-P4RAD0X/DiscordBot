import unittest
import os

if __name__ == "__main__":
    # Get the directory of the test files
    test_dir = "tests"

    # Get all the test files in the directory
    test_files = [f[:-3] for f in os.listdir(test_dir) if f.endswith(".py")]

    # Load the tests from each file and add them to the test suite
    test_suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    for test_file in test_files:
        # Print the test file name
        print(f"Testing {test_file}...")
        module = __import__(f"{test_dir}.{test_file}", fromlist=[""])
        test_suite.addTest(loader.loadTestsFromModule(module))

    # Run the tests
    runner = unittest.TextTestRunner()
    result = runner.run(test_suite)
