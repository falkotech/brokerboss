from app import create_app
import logging
import pytest
import time

# Run tests before startup with these options: 
# -s(Show print statements) -v(Verbose) /tests(All tests in the /tests folder)
return_code = pytest.main(['-s', '-v', '/tests'])

# If all tests passed, start the app
if return_code == 0:
    logging.info('')
    logging.info('=================  ALL TESTS PASSED. Starting app.  ==================')
    
    app = create_app(config_object='app.config.DevelopmentConfig')

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000, debug=False)

# If tests failed, exit
else:
    time.sleep(2) # Give time for the pytest output to be printed
    logging.error('=============================================================')
    logging.error('=================  TESTS FAILED. Exiting.  ==================')
    logging.error('=============================================================')