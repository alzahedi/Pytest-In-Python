import sys
import pytest
import os


def run_tests():
    result_path = "results"
    logging_name = "test_one"
    suite_name = "test_one"
    log_file_path = os.path.join(result_path, f"{logging_name}.txt")
    
    # Create the file if it doesn't exist
    os.makedirs(result_path, exist_ok=True)
    
    # Open the file in write mode to create it
    with open(log_file_path, 'w') as f:
        pass  # No content needed, just creating the file
    
    pytest_args = [
        f'-rpP',                             # Report progress in the output
        '-v',                               # Verbose output
        f'--log-file={os.path.join(result_path, f"{logging_name}.log")}',  # Log file
        f'--junitxml={os.path.join(result_path, f"{logging_name}.xml")}',  # JUnit XML output
        '-o',
        f'junit_suite_name={suite_name}',  # Suite name in JUnit report
        '-o',
        f'junit_family=xunit1',            # JUnit family
        f'--capture=no',                 # Capture output and write it to sys.stdout and log file
    ]
    
    # You can pass arguments to pytest.main like you would on the command line
    #result = pytest.main(pytest_args)
    with open(log_file_path, 'w') as f:
        sys.stdout = f
        sys.stderr = f
        
        # Run pytest, now output will go to the file
        result = pytest.main(pytest_args)
    
    # Checking the return code to determine the result of the test run
    if result == 0:
        print("Tests passed")
    else:
        print("Tests failed")

# Run the tests
run_tests()
