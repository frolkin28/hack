import trafaret as t

BaseMessage = t.Dict(
    action=t.String,
    data=t.Any
)

# backend allows: START
JoinMessageData = t.Dict(
    room_id=t.String,
    client=t.Dict({
        'peer_id': t.String,
        'name': t.String,
        'email': t.String,
        t.Key('is_organizer', optional=True): t.Bool,
    })
)

LeaveMessageData = t.Dict(
    room_id=t.String,
)

ReconnectMessageData = t.Dict(
    room_id=t.String,
    peer_id=t.String,
)

DeleteClientMessageData = t.Dict(
    room_id=t.String,
    peer_id=t.String,
)

RelaySDPMessageData = t.Dict(
    room_id=t.String,
    peer_id=t.String,
    session_description=t.Any,
)

RelayIceMessageData = t.Dict(
    room_id=t.String,
    peer_id=t.String,
    ice_candidate=t.Any,
)
# backend allows: END

# backend respond: START
AddPeerMessageData = t.Dict(
    client=t.Dict(
        peer_id=t.String,
        name=t.String,
        email=t.String,
        is_organizer=t.Bool,
    ),
    create_offer=t.Bool,
)

RemovePeerMessageData = t.Dict(
    peer_id=t.String,
)

SessionDescriptionMessageData = t.Dict(
    peer_id=t.String,
    session_description=t.Any,
)

IceCandidateMessageData = t.Dict(
    peer_id=t.String,
    ice_candidate=t.Any,
)

ClientDeletedMessageData = t.Dict(
    room_id=t.String,
    peer_id=t.String,
)
# backend respond: END
