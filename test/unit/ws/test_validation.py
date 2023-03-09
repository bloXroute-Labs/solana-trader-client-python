import unittest

from bxserum.proto import GetAccountBalanceResponse, GetOpenOrdersResponse, GetServerTimeResponse, \
    TokenBalance
from bxsolana_trader_proto import GetUserResponse

from bxsolana.provider.ws import _validated_response


class TestWSValidation(unittest.TestCase):
    def test_response_not_dictionary(self):
        response = "abcdef-123"

        try:
            _validated_response(response, GetAccountBalanceResponse)
            self.fail("_validated_response should have thrown exception")
        except Exception as e:
            self.assertEqual(str(e), f"response {response} was not a dictionary")

    def test_response_none(self):
        response = None

        try:
            _validated_response(response, GetAccountBalanceResponse)
            self.fail("_validated_response should have thrown exception")
        except Exception as e:
            self.assertEqual(str(e), f"response {response} was not a dictionary")

    def test_error_message(self):
        response = {"code":5, "message":"Not Found", "details":[]}

        try:
            _validated_response(response, GetAccountBalanceResponse)
            self.fail("_validated_response should have thrown exception")
        except Exception as e:
            self.assertEqual(str(e), "Not Found")

    def test_incorrect_type(self):
        response = GetServerTimeResponse(timestamp="123")
        response_dict = response.to_dict()

        try:
            _validated_response(response_dict, GetAccountBalanceResponse)
            self.fail("_validated_response should have thrown exception")
        except Exception as e:
            self.assertEqual(str(e), "response {'timestamp': '123'} was not of type <class 'bxserum.proto.api.GetAccountBalanceResponse'>")

    def test_valid_response_1(self):
        response = GetOpenOrdersResponse(orders=[])
        response_dict = response.to_dict(include_default_values=True)

        try:
            actual_response = _validated_response(response_dict, GetOpenOrdersResponse)
            self.assertEqual(actual_response, response)
        except Exception:
            self.fail("should not have thrown exception")

    def test_valid_response_2(self):
        response = GetAccountBalanceResponse(tokens=[TokenBalance(symbol="SOL")])
        response_dict = response.to_dict(include_default_values=True)

        try:
            actual_response = _validated_response(response_dict, GetAccountBalanceResponse)
            self.assertEqual(actual_response, response)
        except Exception:
            self.fail("should not have thrown exception")

    def test_valid_response_3(self):
        response = GetUserResponse(status="good", account_number=0)
        response_dict = response.to_dict(include_default_values=True)

        try:
            actual_response = _validated_response(response_dict, GetUserResponse)
            self.assertEqual(actual_response, response)
        except Exception:
            self.fail("should not have thrown exception")
