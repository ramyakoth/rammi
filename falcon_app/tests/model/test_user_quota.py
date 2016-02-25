import pytest

@pytest.mark.django_db
def test_user_quota(test_user):
    ''' test for check user quaota'''
    user = test_user
    assert user.quota == 1024

@pytest.mark.django_db
def test_hquota_MB(test_user):
    ''' test for check hquota'''
    user = test_user
    user.quota = 1048576
    assert user.hquota('MB') == 1.0

@pytest.mark.django_db
def test_hquota_GB(test_user):
    ''' test for check hquota'''
    user = test_user
    user.quota = 1073741824
    assert user.hquota('GB') == 1.0

    
@pytest.mark.django_db
def test_used_quota(test_user,test_doc):
    assert test_user.used_quota == test_doc.file_size

@pytest.mark.django_db
def test_balance_quota(test_user,test_doc):
    assert test_user.balance_quota == test_user.quota - test_doc.file_size
