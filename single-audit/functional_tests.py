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

        # She notices the page header mentions the SF-SAC.
        header_text = self.browser.find_elements_by_tag_name('h1')[1].text
        self.assertIn('SF-SAC', header_text)

        self.fail('@todo: Finish this test.')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
