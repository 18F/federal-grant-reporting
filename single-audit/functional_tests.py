from selenium import webdriver
import unittest


class NewGranteeVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_single_audit_package_and_submit_it(self):
        # Nina handles financial grant reporting at a grant
        # recipient that has to submit single audits. She goes to
        # submit a new single audit package for a grant that's
        # just closed out.
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention the SF-SAC.
        self.assertIn('SF-SAC', self.browser.title)
        self.fail('@todo: Finish this test.')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
