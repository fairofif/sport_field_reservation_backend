from static import *
from app import app

def test_join_to_public_reservation_normal():
    ## ============ admin prerequirement ============= #

    admin_device = newVirtualDeviceID()
    admin_token = newUserToken()

    sport_kind_id = insert_admin_unittest_sport_kind()
    sport_venue_id = newSportFieldUUID()

    insert_unittest_device(admin_device)
    insert_admin_unittest_user()
    insert_admin_unittest_token(admin_token, admin_device)
    insert_admin_unittest_sport_venue(sport_venue_id, sport_kind_id)

    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, sport_venue_id, 1)

    ## ============ player prerequirement ============= #

    player_device = newVirtualDeviceID()
    player_token = newUserToken()
    insert_unittest_device(player_device)
    insert_player_unittest_user()
    insert_player_unittest_token(player_token, player_device)

    ## ============== condition requirement =============== #

    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2024-05-01", "09:00:00", "11:59:59")
    change_reservation_status(booking_id, 'approved')
    change_open_member_status(booking_id, 1)

    username_join = "wakacipuyyy"
    insert_player_unittest_user_custom(username_join)
    token_join = newUserToken()
    device_join = newVirtualDeviceID()
    insert_unittest_device(device_join)
    insert_player_unittest_token_custom(token_join, device_join, username_join)

    ## TEST

    url = f"/player/reservation/join/{booking_id}"

    header = {
        'token': token_join
    }

    client = app.test_client()

    response = client.post(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(device_join)
    delete_player_unittest_user_custom(username_join)

    # =========== VALIDATION =========== #

    assert response.status_code == 200
    assert response.get_json()['join_status'] == True
    assert response.get_json()['message'] == f"{username_join} now is member of reservation {booking_id}"
    assert response.get_json()['data'] != None

def test_join_to_public_reservation_not_open_member():
    ## ============ admin prerequirement ============= #

    admin_device = newVirtualDeviceID()
    admin_token = newUserToken()

    sport_kind_id = insert_admin_unittest_sport_kind()
    sport_venue_id = newSportFieldUUID()

    insert_unittest_device(admin_device)
    insert_admin_unittest_user()
    insert_admin_unittest_token(admin_token, admin_device)
    insert_admin_unittest_sport_venue(sport_venue_id, sport_kind_id)

    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, sport_venue_id, 1)

    ## ============ player prerequirement ============= #

    player_device = newVirtualDeviceID()
    player_token = newUserToken()
    insert_unittest_device(player_device)
    insert_player_unittest_user()
    insert_player_unittest_token(player_token, player_device)

    ## ============== condition requirement =============== #

    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2024-05-01", "09:00:00", "11:59:59")
    change_reservation_status(booking_id, 'approved')
    change_open_member_status(booking_id, 0)

    username_join = "wakacipuyyy"
    insert_player_unittest_user_custom(username_join)
    token_join = newUserToken()
    device_join = newVirtualDeviceID()
    insert_unittest_device(device_join)
    insert_player_unittest_token_custom(token_join, device_join, username_join)

    ## TEST

    url = f"/player/reservation/join/{booking_id}"

    header = {
        'token': token_join
    }

    client = app.test_client()

    response = client.post(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(device_join)
    delete_player_unittest_user_custom(username_join)

    # =========== VALIDATION =========== #

    assert response.status_code == 403
    assert response.get_json()['join_status'] == False
    assert response.get_json()['message'] == f"Reservation {booking_id} is not open member"
    assert response.get_json()['data'] == None

def test_join_to_public_reservation_if_a_host():
    ## ============ admin prerequirement ============= #

    admin_device = newVirtualDeviceID()
    admin_token = newUserToken()

    sport_kind_id = insert_admin_unittest_sport_kind()
    sport_venue_id = newSportFieldUUID()

    insert_unittest_device(admin_device)
    insert_admin_unittest_user()
    insert_admin_unittest_token(admin_token, admin_device)
    insert_admin_unittest_sport_venue(sport_venue_id, sport_kind_id)

    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, sport_venue_id, 1)

    ## ============ player prerequirement ============= #

    player_device = newVirtualDeviceID()
    player_token = newUserToken()
    insert_unittest_device(player_device)
    insert_player_unittest_user()
    insert_player_unittest_token(player_token, player_device)

    ## ============== condition requirement =============== #

    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2024-05-01", "09:00:00", "11:59:59")
    change_reservation_status(booking_id, 'approved')
    change_open_member_status(booking_id, 1)

    ## TEST

    url = f"/player/reservation/join/{booking_id}"

    header = {
        'token': player_token
    }

    client = app.test_client()

    response = client.post(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 403
    assert response.get_json()['join_status'] == False
    assert response.get_json()['message'] == f"You are already a host of this reservation {booking_id}"
    assert response.get_json()['data'] == None

def test_join_to_public_reservation_if_already_joined():
    ## ============ admin prerequirement ============= #

    admin_device = newVirtualDeviceID()
    admin_token = newUserToken()

    sport_kind_id = insert_admin_unittest_sport_kind()
    sport_venue_id = newSportFieldUUID()

    insert_unittest_device(admin_device)
    insert_admin_unittest_user()
    insert_admin_unittest_token(admin_token, admin_device)
    insert_admin_unittest_sport_venue(sport_venue_id, sport_kind_id)

    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, sport_venue_id, 1)

    ## ============ player prerequirement ============= #

    player_device = newVirtualDeviceID()
    player_token = newUserToken()
    insert_unittest_device(player_device)
    insert_player_unittest_user()
    insert_player_unittest_token(player_token, player_device)

    ## ============== condition requirement =============== #

    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2024-05-01", "09:00:00", "11:59:59")
    change_reservation_status(booking_id, 'approved')
    change_open_member_status(booking_id, 1)

    username_join = "wakacipuyyy"
    insert_player_unittest_user_custom(username_join)
    token_join = newUserToken()
    device_join = newVirtualDeviceID()
    insert_unittest_device(device_join)
    insert_player_unittest_token_custom(token_join, device_join, username_join)
    insert_member_reservation(booking_id, username_join)

    ## TEST

    url = f"/player/reservation/join/{booking_id}"

    header = {
        'token': token_join
    }

    client = app.test_client()

    response = client.post(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(device_join)
    delete_player_unittest_user_custom(username_join)

    # =========== VALIDATION =========== #

    assert response.status_code == 409
    assert response.get_json()['join_status'] == False
    assert response.get_json()['message'] == f"This user is already a member of this reservation {booking_id}"
    assert response.get_json()['data'] == None

def test_invite_player_by_host():
    ## ============ admin prerequirement ============= #

    admin_device = newVirtualDeviceID()
    admin_token = newUserToken()

    sport_kind_id = insert_admin_unittest_sport_kind()
    sport_venue_id = newSportFieldUUID()

    insert_unittest_device(admin_device)
    insert_admin_unittest_user()
    insert_admin_unittest_token(admin_token, admin_device)
    insert_admin_unittest_sport_venue(sport_venue_id, sport_kind_id)

    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, sport_venue_id, 1)

    ## ============ player prerequirement ============= #

    player_device = newVirtualDeviceID()
    player_token = newUserToken()
    insert_unittest_device(player_device)
    insert_player_unittest_user()
    insert_player_unittest_token(player_token, player_device)

    ## ============== condition requirement =============== #

    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2024-05-01", "09:00:00", "11:59:59")
    change_reservation_status(booking_id, 'approved')
    change_open_member_status(booking_id, 1)

    username_join = "wakacipuyyy"
    insert_player_unittest_user_custom(username_join)
    token_join = newUserToken()
    device_join = newVirtualDeviceID()
    insert_unittest_device(device_join)
    insert_player_unittest_token_custom(token_join, device_join, username_join)

    ## TEST

    url = f"/player/reservation/invite/{booking_id}/{username_join}"

    header = {
        'token': player_token
    }

    client = app.test_client()

    response = client.post(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(device_join)
    delete_player_unittest_user_custom(username_join)

    # =========== VALIDATION =========== #

    assert response.status_code == 200
    assert response.get_json()['invite_status'] == True
    assert response.get_json()['message'] == f"{username_join} now is member of reservation {booking_id}"
    assert response.get_json()['data'] != None

def test_invite_player_by_not_host():
    ## ============ admin prerequirement ============= #

    admin_device = newVirtualDeviceID()
    admin_token = newUserToken()

    sport_kind_id = insert_admin_unittest_sport_kind()
    sport_venue_id = newSportFieldUUID()

    insert_unittest_device(admin_device)
    insert_admin_unittest_user()
    insert_admin_unittest_token(admin_token, admin_device)
    insert_admin_unittest_sport_venue(sport_venue_id, sport_kind_id)

    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, sport_venue_id, 1)

    ## ============ player prerequirement ============= #

    player_device = newVirtualDeviceID()
    player_token = newUserToken()
    insert_unittest_device(player_device)
    insert_player_unittest_user()
    insert_player_unittest_token(player_token, player_device)

    ## ============== condition requirement =============== #

    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2024-05-01", "09:00:00", "11:59:59")
    change_reservation_status(booking_id, 'approved')
    change_open_member_status(booking_id, 1)

    username_join = "wakacipuyyy"
    insert_player_unittest_user_custom(username_join)
    token_join = newUserToken()
    device_join = newVirtualDeviceID()
    insert_unittest_device(device_join)
    insert_player_unittest_token_custom(token_join, device_join, username_join)
    insert_member_reservation(booking_id, username_join)

    username_join_2 = "wadadada"
    insert_player_unittest_user_custom(username_join_2)

    ## TEST

    url = f"/player/reservation/invite/{booking_id}/{username_join_2}"

    header = {
        'token': token_join
    }

    client = app.test_client()

    response = client.post(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(device_join)
    delete_player_unittest_user_custom(username_join)
    delete_player_unittest_user_custom(username_join_2)

    # =========== VALIDATION =========== #

    assert response.status_code == 403
    assert response.get_json()['invite_status'] == False
    assert response.get_json()['message'] == f"{username_join_2} failed to be invited, {username_join} not a host of reservation {booking_id}"
    assert response.get_json()['data'] == None

def test_invite_player_by_host_player_is_already_in():
    ## ============ admin prerequirement ============= #

    admin_device = newVirtualDeviceID()
    admin_token = newUserToken()

    sport_kind_id = insert_admin_unittest_sport_kind()
    sport_venue_id = newSportFieldUUID()

    insert_unittest_device(admin_device)
    insert_admin_unittest_user()
    insert_admin_unittest_token(admin_token, admin_device)
    insert_admin_unittest_sport_venue(sport_venue_id, sport_kind_id)

    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, sport_venue_id, 1)

    ## ============ player prerequirement ============= #

    player_device = newVirtualDeviceID()
    player_token = newUserToken()
    insert_unittest_device(player_device)
    insert_player_unittest_user()
    insert_player_unittest_token(player_token, player_device)

    ## ============== condition requirement =============== #

    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2024-05-01", "09:00:00", "11:59:59")
    change_reservation_status(booking_id, 'approved')
    change_open_member_status(booking_id, 1)

    username_join = "wakacipuyyy"
    insert_player_unittest_user_custom(username_join)
    token_join = newUserToken()
    device_join = newVirtualDeviceID()
    insert_unittest_device(device_join)
    insert_player_unittest_token_custom(token_join, device_join, username_join)

    insert_member_reservation(booking_id, username_join)

    ## TEST

    url = f"/player/reservation/invite/{booking_id}/{username_join}"

    header = {
        'token': player_token
    }

    client = app.test_client()

    response = client.post(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(device_join)
    delete_player_unittest_user_custom(username_join)

    # =========== VALIDATION =========== #

    assert response.status_code == 409
    assert response.get_json()['invite_status'] == False
    assert response.get_json()['message'] == f"{username_join} is already in reservation {booking_id} before"
    assert response.get_json()['data'] == None

def test_invite_player_by_host_himself():
    ## ============ admin prerequirement ============= #

    admin_device = newVirtualDeviceID()
    admin_token = newUserToken()

    sport_kind_id = insert_admin_unittest_sport_kind()
    sport_venue_id = newSportFieldUUID()

    insert_unittest_device(admin_device)
    insert_admin_unittest_user()
    insert_admin_unittest_token(admin_token, admin_device)
    insert_admin_unittest_sport_venue(sport_venue_id, sport_kind_id)

    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, sport_venue_id, 1)

    ## ============ player prerequirement ============= #

    player_device = newVirtualDeviceID()
    player_token = newUserToken()
    insert_unittest_device(player_device)
    insert_player_unittest_user()
    insert_player_unittest_token(player_token, player_device)

    ## ============== condition requirement =============== #

    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2024-05-01", "09:00:00", "11:59:59")
    change_reservation_status(booking_id, 'approved')
    change_open_member_status(booking_id, 1)

    ## TEST

    url = f"/player/reservation/invite/{booking_id}/unittest"

    header = {
        'token': player_token
    }

    client = app.test_client()

    response = client.post(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)
    # =========== VALIDATION =========== #

    assert response.status_code == 403
    assert response.get_json()['invite_status'] == False
    assert response.get_json()['message'] == f"This user is already a host of reservation {booking_id}"
    assert response.get_json()['data'] == None

def test_invite_player_by_host_player_not_exists():
    ## ============ admin prerequirement ============= #

    admin_device = newVirtualDeviceID()
    admin_token = newUserToken()

    sport_kind_id = insert_admin_unittest_sport_kind()
    sport_venue_id = newSportFieldUUID()

    insert_unittest_device(admin_device)
    insert_admin_unittest_user()
    insert_admin_unittest_token(admin_token, admin_device)
    insert_admin_unittest_sport_venue(sport_venue_id, sport_kind_id)

    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, sport_venue_id, 1)

    ## ============ player prerequirement ============= #

    player_device = newVirtualDeviceID()
    player_token = newUserToken()
    insert_unittest_device(player_device)
    insert_player_unittest_user()
    insert_player_unittest_token(player_token, player_device)

    ## ============== condition requirement =============== #

    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2024-05-01", "09:00:00", "11:59:59")
    change_reservation_status(booking_id, 'approved')
    change_open_member_status(booking_id, 1)
    ## TEST

    username_invite = 'usernamenotexist'

    url = f"/player/reservation/invite/{booking_id}/{username_invite}"

    header = {
        'token': player_token
    }

    client = app.test_client()

    response = client.post(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 404
    assert response.get_json()['invite_status'] == False
    assert response.get_json()['message'] == f"{username_invite} not found as a player in database"
    assert response.get_json()['data'] == None

def test_get_list_player_of_reservation():
    ## ============ admin prerequirement ============= #

    admin_device = newVirtualDeviceID()
    admin_token = newUserToken()

    sport_kind_id = insert_admin_unittest_sport_kind()
    sport_venue_id = newSportFieldUUID()

    insert_unittest_device(admin_device)
    insert_admin_unittest_user()
    insert_admin_unittest_token(admin_token, admin_device)
    insert_admin_unittest_sport_venue(sport_venue_id, sport_kind_id)

    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, sport_venue_id, 1)

    ## ============ player prerequirement ============= #

    player_device = newVirtualDeviceID()
    player_token = newUserToken()
    insert_unittest_device(player_device)
    insert_player_unittest_user()
    insert_player_unittest_token(player_token, player_device)

    ## ============== condition requirement =============== #

    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2024-05-01", "09:00:00", "11:59:59")
    change_reservation_status(booking_id, 'approved')
    change_open_member_status(booking_id, 1)

    username_join = "wakacipuyyy"
    insert_player_unittest_user_custom(username_join)
    token_join = newUserToken()
    device_join = newVirtualDeviceID()
    insert_unittest_device(device_join)
    insert_player_unittest_token_custom(token_join, device_join, username_join)
    insert_member_reservation(booking_id, username_join)

    ## TEST

    url = f"/player/reservation/members/{booking_id}"

    header = {
        'token': player_token
    }

    client = app.test_client()

    response = client.get(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(device_join)
    delete_player_unittest_user_custom(username_join)

    # =========== VALIDATION =========== #

    assert response.status_code == 200
    assert response.get_json()['get_status'] == True
    assert response.get_json()['message'] == f"List member of reservation {booking_id} successfully retrieved"
    assert response.get_json()['data'] != None

def test_kick_player_from_a_reservation():
    ## ============ admin prerequirement ============= #

    admin_device = newVirtualDeviceID()
    admin_token = newUserToken()

    sport_kind_id = insert_admin_unittest_sport_kind()
    sport_venue_id = newSportFieldUUID()

    insert_unittest_device(admin_device)
    insert_admin_unittest_user()
    insert_admin_unittest_token(admin_token, admin_device)
    insert_admin_unittest_sport_venue(sport_venue_id, sport_kind_id)

    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, sport_venue_id, 1)

    ## ============ player prerequirement ============= #

    player_device = newVirtualDeviceID()
    player_token = newUserToken()
    insert_unittest_device(player_device)
    insert_player_unittest_user()
    insert_player_unittest_token(player_token, player_device)

    ## ============== condition requirement =============== #

    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2024-05-01", "09:00:00", "11:59:59")
    change_reservation_status(booking_id, 'approved')
    change_open_member_status(booking_id, 1)

    username_join = "wakacipuyyy"
    insert_player_unittest_user_custom(username_join)
    token_join = newUserToken()
    device_join = newVirtualDeviceID()
    insert_unittest_device(device_join)
    insert_player_unittest_token_custom(token_join, device_join, username_join)
    insert_member_reservation(booking_id, username_join)

    ## TEST

    url = f"/player/reservation/kick/{booking_id}/{username_join}"

    header = {
        'token': player_token
    }

    client = app.test_client()

    response = client.delete(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(device_join)
    delete_player_unittest_user_custom(username_join)

    # =========== VALIDATION =========== #

    assert response.status_code == 200
    assert response.get_json()['kick_status'] == True
    assert response.get_json()['message'] == f"{username_join} has been removed from reservation {booking_id}"
    assert response.get_json()['data'] != None

def test_kick_player_from_a_reservation_booking_id_not_valid():
    ## ============ admin prerequirement ============= #

    admin_device = newVirtualDeviceID()
    admin_token = newUserToken()

    sport_kind_id = insert_admin_unittest_sport_kind()
    sport_venue_id = newSportFieldUUID()

    insert_unittest_device(admin_device)
    insert_admin_unittest_user()
    insert_admin_unittest_token(admin_token, admin_device)
    insert_admin_unittest_sport_venue(sport_venue_id, sport_kind_id)

    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, sport_venue_id, 1)

    ## ============ player prerequirement ============= #

    player_device = newVirtualDeviceID()
    player_token = newUserToken()
    insert_unittest_device(player_device)
    insert_player_unittest_user()
    insert_player_unittest_token(player_token, player_device)

    ## ============== condition requirement =============== #

    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2024-05-01", "09:00:00", "11:59:59")
    change_reservation_status(booking_id, 'approved')
    change_open_member_status(booking_id, 1)

    username_join = "wakacipuyyy"
    insert_player_unittest_user_custom(username_join)
    token_join = newUserToken()
    device_join = newVirtualDeviceID()
    insert_unittest_device(device_join)
    insert_player_unittest_token_custom(token_join, device_join, username_join)
    insert_member_reservation(booking_id, username_join)

    new_book_id = newBookingUUID()
    ## TEST

    url = f"/player/reservation/kick/{new_book_id}/{username_join}"

    header = {
        'token': player_token
    }

    client = app.test_client()

    response = client.delete(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(device_join)
    delete_player_unittest_user_custom(username_join)

    # =========== VALIDATION =========== #

    assert response.status_code == 404
    assert response.get_json()['kick_status'] == False
    assert response.get_json()['message'] == f"Reservation {new_book_id} is not exists"
    assert response.get_json()['data'] == None

def test_kick_player_from_a_reservation_player_not_found():
    ## ============ admin prerequirement ============= #

    admin_device = newVirtualDeviceID()
    admin_token = newUserToken()

    sport_kind_id = insert_admin_unittest_sport_kind()
    sport_venue_id = newSportFieldUUID()

    insert_unittest_device(admin_device)
    insert_admin_unittest_user()
    insert_admin_unittest_token(admin_token, admin_device)
    insert_admin_unittest_sport_venue(sport_venue_id, sport_kind_id)

    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, sport_venue_id, 1)

    ## ============ player prerequirement ============= #

    player_device = newVirtualDeviceID()
    player_token = newUserToken()
    insert_unittest_device(player_device)
    insert_player_unittest_user()
    insert_player_unittest_token(player_token, player_device)

    ## ============== condition requirement =============== #

    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2024-05-01", "09:00:00", "11:59:59")
    change_reservation_status(booking_id, 'approved')
    change_open_member_status(booking_id, 1)

    username_join = "wakacipuyyy"
    insert_player_unittest_user_custom(username_join)
    token_join = newUserToken()
    device_join = newVirtualDeviceID()
    insert_unittest_device(device_join)
    insert_player_unittest_token_custom(token_join, device_join, username_join)
    insert_member_reservation(booking_id, username_join)

    ## TEST

    url = f"/player/reservation/kick/{booking_id}/unittest123"

    header = {
        'token': player_token
    }

    client = app.test_client()

    response = client.delete(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(device_join)
    delete_player_unittest_user_custom(username_join)

    # =========== VALIDATION =========== #

    assert response.status_code == 404
    assert response.get_json()['kick_status'] == False
    assert response.get_json()['message'] == f"unittest123 is not a member of reservation {booking_id}"
    assert response.get_json()['data'] == None

def test_kick_player_from_a_reservation_not_a_host():
    ## ============ admin prerequirement ============= #

    admin_device = newVirtualDeviceID()
    admin_token = newUserToken()

    sport_kind_id = insert_admin_unittest_sport_kind()
    sport_venue_id = newSportFieldUUID()

    insert_unittest_device(admin_device)
    insert_admin_unittest_user()
    insert_admin_unittest_token(admin_token, admin_device)
    insert_admin_unittest_sport_venue(sport_venue_id, sport_kind_id)

    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, sport_venue_id, 1)

    ## ============ player prerequirement ============= #

    player_device = newVirtualDeviceID()
    player_token = newUserToken()
    insert_unittest_device(player_device)
    insert_player_unittest_user()
    insert_player_unittest_token(player_token, player_device)

    ## ============== condition requirement =============== #

    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2024-05-01", "09:00:00", "11:59:59")
    change_reservation_status(booking_id, 'approved')
    change_open_member_status(booking_id, 1)

    username_join = "wakacipuyyy"
    insert_player_unittest_user_custom(username_join)
    token_join = newUserToken()
    device_join = newVirtualDeviceID()
    insert_unittest_device(device_join)
    insert_player_unittest_token_custom(token_join, device_join, username_join)
    insert_member_reservation(booking_id, username_join)

    new_book_id = newBookingUUID()
    ## TEST

    url = f"/player/reservation/kick/{booking_id}/unittest"

    header = {
        'token': token_join
    }

    client = app.test_client()

    response = client.delete(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(device_join)
    delete_player_unittest_user_custom(username_join)

    # =========== VALIDATION =========== #

    assert response.status_code == 403
    assert response.get_json()['kick_status'] == False
    assert response.get_json()['message'] == f"Only host could kick a member, {username_join} is not a host of reservation {booking_id}"
    assert response.get_json()['data'] == None

def test_kick_player_from_a_reservation_kick_himself():
    ## ============ admin prerequirement ============= #

    admin_device = newVirtualDeviceID()
    admin_token = newUserToken()

    sport_kind_id = insert_admin_unittest_sport_kind()
    sport_venue_id = newSportFieldUUID()

    insert_unittest_device(admin_device)
    insert_admin_unittest_user()
    insert_admin_unittest_token(admin_token, admin_device)
    insert_admin_unittest_sport_venue(sport_venue_id, sport_kind_id)

    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, sport_venue_id, 1)

    ## ============ player prerequirement ============= #

    player_device = newVirtualDeviceID()
    player_token = newUserToken()
    insert_unittest_device(player_device)
    insert_player_unittest_user()
    insert_player_unittest_token(player_token, player_device)

    ## ============== condition requirement =============== #

    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2024-05-01", "09:00:00", "11:59:59")
    change_reservation_status(booking_id, 'approved')
    change_open_member_status(booking_id, 1)

    username_join = "wakacipuyyy"
    insert_player_unittest_user_custom(username_join)
    token_join = newUserToken()
    device_join = newVirtualDeviceID()
    insert_unittest_device(device_join)
    insert_player_unittest_token_custom(token_join, device_join, username_join)
    insert_member_reservation(booking_id, username_join)

    new_book_id = newBookingUUID()
    ## TEST

    url = f"/player/reservation/kick/{booking_id}/unittest"

    header = {
        'token': player_token
    }

    client = app.test_client()

    response = client.delete(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(device_join)
    delete_player_unittest_user_custom(username_join)

    # =========== VALIDATION =========== #

    assert response.status_code == 403
    assert response.get_json()['kick_status'] == False
    assert response.get_json()['message'] == f"Can't kick a host"
    assert response.get_json()['data'] == None

def test_leave_player_from_a_reservation():
    ## ============ admin prerequirement ============= #

    admin_device = newVirtualDeviceID()
    admin_token = newUserToken()

    sport_kind_id = insert_admin_unittest_sport_kind()
    sport_venue_id = newSportFieldUUID()

    insert_unittest_device(admin_device)
    insert_admin_unittest_user()
    insert_admin_unittest_token(admin_token, admin_device)
    insert_admin_unittest_sport_venue(sport_venue_id, sport_kind_id)

    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, sport_venue_id, 1)

    ## ============ player prerequirement ============= #

    player_device = newVirtualDeviceID()
    player_token = newUserToken()
    insert_unittest_device(player_device)
    insert_player_unittest_user()
    insert_player_unittest_token(player_token, player_device)

    ## ============== condition requirement =============== #

    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2024-05-01", "09:00:00", "11:59:59")
    change_reservation_status(booking_id, 'approved')
    change_open_member_status(booking_id, 1)

    username_join = "wakacipuyyy"
    insert_player_unittest_user_custom(username_join)
    token_join = newUserToken()
    device_join = newVirtualDeviceID()
    insert_unittest_device(device_join)
    insert_player_unittest_token_custom(token_join, device_join, username_join)
    insert_member_reservation(booking_id, username_join)

    ## TEST

    url = f"/player/reservation/leave/{booking_id}"

    header = {
        'token': token_join
    }

    client = app.test_client()

    response = client.delete(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(device_join)
    delete_player_unittest_user_custom(username_join)

    # =========== VALIDATION =========== #

    assert response.status_code == 200
    assert response.get_json()['leave_status'] == True
    assert response.get_json()['message'] == f"{username_join} has been leaved from reservation {booking_id}"
    assert response.get_json()['data'] != None

def test_leave_player_from_a_reservation_host_self():
    ## ============ admin prerequirement ============= #

    admin_device = newVirtualDeviceID()
    admin_token = newUserToken()

    sport_kind_id = insert_admin_unittest_sport_kind()
    sport_venue_id = newSportFieldUUID()

    insert_unittest_device(admin_device)
    insert_admin_unittest_user()
    insert_admin_unittest_token(admin_token, admin_device)
    insert_admin_unittest_sport_venue(sport_venue_id, sport_kind_id)

    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, sport_venue_id, 1)

    ## ============ player prerequirement ============= #

    player_device = newVirtualDeviceID()
    player_token = newUserToken()
    insert_unittest_device(player_device)
    insert_player_unittest_user()
    insert_player_unittest_token(player_token, player_device)

    ## ============== condition requirement =============== #

    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2024-05-01", "09:00:00", "11:59:59")
    change_reservation_status(booking_id, 'approved')
    change_open_member_status(booking_id, 1)

    username_join = "wakacipuyyy"
    insert_player_unittest_user_custom(username_join)
    token_join = newUserToken()
    device_join = newVirtualDeviceID()
    insert_unittest_device(device_join)
    insert_player_unittest_token_custom(token_join, device_join, username_join)
    insert_member_reservation(booking_id, username_join)

    ## TEST

    url = f"/player/reservation/leave/{booking_id}"

    header = {
        'token': player_token
    }

    client = app.test_client()

    response = client.delete(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(device_join)
    delete_player_unittest_user_custom(username_join)

    # =========== VALIDATION =========== #

    assert response.status_code == 403
    assert response.get_json()['leave_status'] == False
    assert response.get_json()['message'] == f"Host can't leave his/her reservation"
    assert response.get_json()['data'] == None

def test_leave_player_from_a_reservation_not_a_member():
    ## ============ admin prerequirement ============= #

    admin_device = newVirtualDeviceID()
    admin_token = newUserToken()

    sport_kind_id = insert_admin_unittest_sport_kind()
    sport_venue_id = newSportFieldUUID()

    insert_unittest_device(admin_device)
    insert_admin_unittest_user()
    insert_admin_unittest_token(admin_token, admin_device)
    insert_admin_unittest_sport_venue(sport_venue_id, sport_kind_id)

    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, sport_venue_id, 1)

    ## ============ player prerequirement ============= #

    player_device = newVirtualDeviceID()
    player_token = newUserToken()
    insert_unittest_device(player_device)
    insert_player_unittest_user()
    insert_player_unittest_token(player_token, player_device)

    ## ============== condition requirement =============== #

    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2024-05-01", "09:00:00", "11:59:59")
    change_reservation_status(booking_id, 'approved')
    change_open_member_status(booking_id, 1)

    username_join = "wakacipuyyy"
    insert_player_unittest_user_custom(username_join)
    token_join = newUserToken()
    device_join = newVirtualDeviceID()
    insert_unittest_device(device_join)
    insert_player_unittest_token_custom(token_join, device_join, username_join)

    ## TEST

    url = f"/player/reservation/leave/{booking_id}"

    header = {
        'token': token_join
    }

    client = app.test_client()

    response = client.delete(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(device_join)
    delete_player_unittest_user_custom(username_join)

    # =========== VALIDATION =========== #

    assert response.status_code == 404
    assert response.get_json()['leave_status'] == False
    assert response.get_json()['message'] == f"{username_join} not a member of reservation {booking_id}"
    assert response.get_json()['data'] == None
