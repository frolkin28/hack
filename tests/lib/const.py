from tests.const import TEST_ROOM_ID

JOIN_DATA = {
    'room_id': TEST_ROOM_ID,
    'client': {
        'peer_id': 'peer_id',
        'name': 'name',
        'email': 'email',
        'is_organizer': False,
    }
}

LEAVE_DATA = {
    'room_id': TEST_ROOM_ID,
}

DELETE_CLIENT_DATA = {
    'room_id': TEST_ROOM_ID,
    'peer_id': 'peer_id',
}

RELAY_SDP_DATA = {
    'room_id': TEST_ROOM_ID,
    'peer_id': 'peer_id',
    'session_description': {'aaa': 'bbb'}
}

RELAY_ICE_DATA = {
    'room_id': TEST_ROOM_ID,
    'peer_id': 'peer_id',
    'ice_candidate': {'aaa': 'bbb'}
}

ADD_PEER_DATA = {
    'client': {
        'peer_id': 'peer_id',
        'name': 'name',
        'email': 'email',
        'is_organizer': False,
    },
    'create_offer': False
}

REMOVE_PEER_DATA = {
    'peer_id': 'peer_id'
}

SESSION_DESCRIPTION_DATA = {
    'peer_id': 'peer_id',
    'session_description': {'bbbb': 'aaaa'},
}

ICE_CANDIDATE_DATA = {
    'peer_id': 'peer_id',
    'ice_candidate': {'bbbb': 'aaaa'},
}
