"""Launch NextDom GUI tests
"""
import sys
from tests.libs.tests_funcs import *

NEXTDOM_URL = 'http://127.0.0.1:8765'
NEXTDOM_LOGIN = 'admin'
NEXTDOM_PASSWORD = 'nextdom-test'

def first_use_tests():
    """Starts gui tests related to the first use page
    """
    container_name = 'firstuse'
    print_subtitle('First use page')
    start_test_container(container_name)
    run_test('tests/first_use_page.py', [NEXTDOM_URL])
    remove_test_container(container_name)

def migration_tests():
    """Starts gui tests related to the migration page
    """
    container_name = 'migration'
    print_subtitle('Migration')
    start_test_container(container_name, NEXTDOM_PASSWORD)
    # Copy minimal Jeedom backup in the container
    copy_file_in_container(container_name, 'data/backup-Jeedom-3.2.11-2018-11-17-23h26.tar.gz', '/var/www/html/backup/') #pylint: disable=line-too-long
    # Execute the migration
    exec_command_in_container(container_name, 'php /var/www/html/install/restore.php backup=/var/www/html/backup/backup-Jeedom-3.2.11-2018-11-17-23h26.tar.gz > /dev/null 2>&1') #pylint: disable=line-too-long
    # Reset admin password
    exec_command_in_container(container_name, '/usr/bin/mysql -u root nextdomdev -e "UPDATE user SET password = SHA2(\'nextdom-test\', 512)"') #pylint: disable=line-too-long
    run_test('tests/migration_page.py', [NEXTDOM_URL, NEXTDOM_LOGIN, NEXTDOM_PASSWORD])
    remove_test_container(container_name)

def custom_js_css_tests():
    """Starts gui tests related to the Custom JS and CSS page
    """
    container_name = 'custom-js-css'
    print_subtitle('Custom JS/CSS')
    start_test_container(container_name, NEXTDOM_PASSWORD)
    run_test('tests/custom_js_css_page.py', [NEXTDOM_URL, NEXTDOM_LOGIN, NEXTDOM_PASSWORD])
    remove_test_container(container_name)

def plugins_tests():
    """Starts gui tests related to the plugin page
    """
    container_name = 'plugins'
    print_subtitle('Plugins')
    start_test_container(container_name, NEXTDOM_PASSWORD)
    exec_command_in_container(
        container_name,
        '/bin/cp -fr /var/www/html/tests/data/plugin4tests /var/www/html/plugins')
    exec_command_in_container(
        container_name,
        '/bin/chown www-data:www-data -R /var/www/html/plugins')
    exec_command_in_container(
        container_name,
        '/usr/bin/mysql -u root nextdomdev < data/plugin_test.sql')
    run_test('tests/plugins_page.py', [NEXTDOM_URL, NEXTDOM_LOGIN, NEXTDOM_PASSWORD])
    remove_test_container(container_name)

def others_tests():
    """Starts others gui tests
    """
    container_name = 'others'
    print_subtitle('Others tests')
    start_test_container(container_name, NEXTDOM_PASSWORD)
    print_subtitle('Connection page')
    run_test('tests/connection_page.py', [NEXTDOM_URL, NEXTDOM_LOGIN, NEXTDOM_PASSWORD])
    print_subtitle('Administrations pages')
    run_test('tests/administrations_page.py', [NEXTDOM_URL, NEXTDOM_LOGIN, NEXTDOM_PASSWORD])
    print_subtitle('Rescue pages')
    run_test('tests/rescue_page.py', [NEXTDOM_URL, NEXTDOM_LOGIN, NEXTDOM_PASSWORD])
    remove_test_container(container_name)

if __name__ == "__main__":
    TESTS_LIST = {
        'first_use': first_use_tests,
        'migration': migration_tests,
        'custom_js_css': custom_js_css_tests,
        'plugins': plugins_tests,
        'others': others_tests
    }
    init_docker()
    if len(sys.argv) == 1:
        start_all_tests('GUI Tests', TESTS_LIST)
    else:
        start_specific_test(sys.argv[1], TESTS_LIST)
