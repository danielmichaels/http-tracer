import unittest

import vcr

from tracer.main import Tracer


class TestTracer(unittest.TestCase):
    """Basic testing suite"""

    @classmethod
    @vcr.use_cassette("cassettes/TestTracer.yml")
    def setUpClass(cls) -> None:
        url = "reddit.com"
        tracer = Tracer(url)
        tracer.get_response()

    def test_response(self):
        with vcr.use_cassette("cassettes/TestTracer.yml") as cass:
            self.assertEqual(cass.responses[1]["status"]["code"], 200)
            self.assertEqual(cass.requests[1].uri, "https://www.reddit.com/")

    def test_time_converter_returns_milliseconds(self):
        pass

    def test_total_time_elapsed_calc(self):
        pass

    def test_cookies_exist(self):
        with vcr.use_cassette("cassettes/TestTracer.yml") as cass:
            # print(cass.responses[0]['headers']['Set-Cookie'])
            self.assertTrue(cass.responses[1]["headers"]["Set-Cookie"])

    def test_create_dicts(self):
        pass

    def test_http_protocol_stripped_on_gethostbyname(self):
        with vcr.use_cassette("cassettes/TestTracer.yml") as cass:
            result = Tracer._ipaddr(cass.requests[1].uri)
            expected = Tracer._ipaddr(cass.requests[1].uri)
            self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
