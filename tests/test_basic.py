import unittest

import vcr

from tracer.main import Tracer


class TestTracer(unittest.TestCase):
    """Basic testing suite"""

    @classmethod
    @vcr.use_cassette("cassettes/TestTracer.yml")
    def setUpClass(cls) -> None:
        url = "http://wikipedia.org/wiki/Domain_Name_System"
        tracer = Tracer(url)
        tracer.get_response()

    def test_response(self):
        with vcr.use_cassette("cassettes/TestTracer.yml") as cass:
            self.assertEqual(cass.responses[7]["status"]["code"], 200)
            self.assertEqual(
                cass.requests[7].uri, "https://en.wikipedia.org/wiki/Domain_Name_System"
            )

    def test_time_converter_returns_milliseconds(self):
        pass

    def test_total_time_elapsed_calc(self):
        pass

    def test_cookies_exist(self):
        with vcr.use_cassette("cassettes/TestTracer.yml") as cass:
            # print(cass.responses[0]['headers']['Set-Cookie'])
            self.assertTrue(cass.responses[0]["headers"]["Set-Cookie"])

    def test_create_dicts(self):
        pass

    def test_http_protocol_stripped_on_gethostbyname(self):
        with vcr.use_cassette("cassettes/TestTracer.yml") as cass:
            result = Tracer._ipaddr(cass.requests[7].uri)
            expected = "103.102.166.224"  # may change
            self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
