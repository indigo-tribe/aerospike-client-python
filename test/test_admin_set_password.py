# -*- coding: utf-8 -*-

import pytest
import sys
import time

try:
    import aerospike
except:
    print "Please install aerospike python client."
    sys.exit(1)

class TestSetPassword(object):

    def setup_method(self, method):

        """
        Setup method
        """
        config = {
                "hosts": [("127.0.0.1", 3000)]
                }
        self.client = aerospike.client(config).connect( "admin", "admin" )

        self.client.admin_create_user( {}, "testreaduser", "aerospike", ["read"], 1)

        self.delete_users = []

    def teardown_method(self, method):

        """
        Teardown method
        """

        self.client.admin_drop_user( {}, "testreaduser" )

        self.client.close()

    def test_set_password_without_any_parameters(self):

        with pytest.raises(TypeError) as typeError:
            status = self.client.admin_set_password()

        assert "Required argument 'policy' (pos 1) not found" in typeError.value

    def test_set_password_with_proper_parameters(self):

        policy = { 'timeout' : 0 }
        user = "testreaduser"
        password = "newpassword"

        status = self.client.admin_set_password( policy, user, password )

        assert status == 0

    def test_set_password_with_invalid_timeout_policy_value(self):

        policy = { 'timeout' : 0.1 }
        user = "testreaduser"
        password = "newpassword"

        with pytest.raises(Exception) as exception:
            status = self.client.admin_set_password( policy, user, password )

        assert exception.value[0] == -2
        assert exception.value[1] == "Invalid value(type) for policy key"

    def test_set_password_with_proper_timeout_policy_value(self):

        policy = {'timeout' : 4}
        user = "testreaduser"
        password = "newpassword"

        status = self.client.admin_set_password( policy, user, password )

        assert status == 0

    def test_set_password_with_none_username(self):

        policy = {}
        user = None
        password = "newpassword"

        with pytest.raises(Exception) as exception :
            status = self.client.admin_set_password( policy, user, password )

        assert exception.value[0] == -2
        assert exception.value[1] == "Username should be a string"

    def test_set_password_with_none_password(self):

        policy = {}
        user = "testreaduser"
        password = None

        with pytest.raises(Exception) as exception:
            status = self.client.admin_set_password( policy, user, password )

        assert exception.value[0] == -2
        assert exception.value[1] == "Password should be a string"

    def test_set_password_with_non_existent_user(self):

        policy = {}
        user = "new_user"
        password = "newpassword"

        with pytest.raises(Exception) as exception:
            status = self.client.admin_set_password( policy, user, password )

        assert exception.value[0] == 60
        assert exception.value[1] == "aerospike set password failed"

    def test_set_password_with_too_long_password(self):

        policy = {}
        user = "testreaduser"
        password = "newpassword$"*1000

        status = self.client.admin_set_password( policy, user, password )

        assert status == 0
