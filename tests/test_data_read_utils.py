import numpy as np
import os
import re
import requests
from mond_test import data_read_utils


test_api_key = os.getenv("ILL_KEY")
test_base_url = "http://www.illustris-project.org/api/"


def test_get_fail():
    """Test fail cases for :function:`mond_test.data_read_utils.get`. This tests
    the cases when a bad URL or bad API key is given
    """
    # Set up a bad URL and a bad API key
    test_fail_url = list(test_base_url)
    test_fail_url[-2] = "s"
    test_fail_url = "".join(test_fail_url)
    test_fail_key = "".join([test_api_key[i:i+2][::-1] for i in range(0,
        len(test_api_key), 2)])
    
    # Try running with bad URL: should get an HTTPError
    with np.testing.assert_raises_regex(requests.exceptions.HTTPError, 
            "404 Client Error: NOT FOUND for url: " + test_fail_url):
        data_read_utils.get(test_fail_url, test_api_key)

    # Try running with bad API key: should get an HTTPError
    with np.testing.assert_raises_regex(requests.exceptions.HTTPError,
            "403 Client Error: FORBIDDEN for url: " + test_base_url):
        data_read_utils.get(test_base_url, test_fail_key)


def test_get_json():
    """Test getting json page with :function:`mond_test.data_read_utils.get`. In
    this case, we should successfully get a return dict
    """
    r = data_read_utils.get(test_base_url, test_api_key)

    # Check that the results are as expected
    ## Only key should be 'simulations'
    np.testing.assert_array_equal(r.keys(), ["simulations"], 
            "Keys returned from base URL are not as expected")
    ## Check first simulation meta-data
    sim0_exp = {"name": "Illustris-1",
            "num_snapshots": 134,
            "url": "http://www.illustris-project.org/api/Illustris-1/"}
    sim0_get = r["simulations"][0]
    print(sim0_get)
    for key in sim0_exp.iterkeys():
        assert key in sim0_get, "Missing key %s in results" %(key)
    for key, val in sim0_get.iteritems():
        assert key in sim0_exp, "Extra key %s in results" %(key)
        print(val, sim0_exp[key])
        np.testing.assert_string_equal(val, sim0_exp[key])
