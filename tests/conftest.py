import os
import signal

import pytest

def pytest_runtest_makereport(item, call):
    # Create the report from the test item and call
    report = pytest.TestReport.from_item_and_call(item, call)
    
    # Check for the 'setup' phase
    if call.when == "setup" and call.excinfo is not None and os.environ.get('TEST_TIMEOUT') == "True":
        # Customize the failure message for setup failures
        custom_message = f"Test ran for abnormally long time, please check attached logs for details"
        report.longrepr = custom_message  # Override the long failure message
        
    # Check for test call failures and custom timeout logic
    elif call.when == "call" and report.failed and os.environ.get('TEST_TIMEOUT') == "True":
        # Customize the failure message for test call failures with a timeout
        custom_message = f"Test ran for abnormally long time, please check attached logs for details"
        report.longrepr = custom_message  # Override the long failure message
    
    return report




def handle_signal(signum, frame):
    """
    Handle termination signals like SIGTERM and SIGINT.
    """
    print(f"Received termination signal: {signum}")
    # Perform cleanup or other necessary actions here
    print("Cleaning up resources...")
    os.environ["XML_TAG_ROOT_CAUSE"] = "Test ran for abnormally long time"
    os.environ["TEST_TIMEOUT"] = "True"
    # Exit gracefully
    exit(0)

@pytest.fixture(scope='function', autouse=True)
def term_handler(record_xml_attribute):
    print("Setting up signal handler")
    orig = signal.signal(signal.SIGINT, signal.getsignal(signal.SIGINT))
    signal.signal(signal.SIGINT, handle_signal)
    yield
    print("Restoring signal handler")
    signal.signal(signal.SIGTERM, orig)
    for env_var in os.environ:
        if env_var.startswith("XML_TAG_"):
            record_xml_attribute(env_var, os.environ.get(env_var, "-"))