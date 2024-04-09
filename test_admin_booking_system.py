from static import *





def test_get_all_reservation_from_player():
    # Player prerequirements
    insert_player_unittest_user()
    p_device_id = newVirtualDeviceID()
    p_token = newUserToken()
    insert_unittest_device(p_device_id)
    insert_player_unittest_token(p_token, p_device_id)

    # Admin prerequirements
    insert_admin_unittest_user()
    a_device_id = newVirtualDeviceID()
    insert_unittest_device(a_device_id)
    a_token = newUserToken()
    insert_admin_unittest_token(a_token, a_device_id)
    venue_id = newSportFieldUUID()
    sport_kind_id = insert_admin_unittest_sport_kind()
    insert_admin_unittest_sport_venue(venue_id, sport_kind_id)
    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, venue_id, 1)

    # Conditiion prerequirements
    insert_booking_unittest(newBookingUUID(), field_id, "2025-03-26", "13:00:00", "14:59:59")
    insert_booking_unittest(newBookingUUID(), field_id, "2025-03-27", "13:00:00", "14:59:59")
    insert_booking_unittest(newBookingUUID(), field_id, "2025-03-28", "13:00:00", "14:59:59")

    # test
    header = {
        'token': a_token
    }

    url = '/admin/reservation/payment'

    client = app.test_client()

    response = client.get(url, headers=header)

    # clean
    delete_admin_unittest_user()
    delete_player_unittest_user()
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(a_device_id)
    delete_unittest_device(p_device_id)

    # validation
    assert response.status_code == 200
    assert response.get_json()['get_status'] == True