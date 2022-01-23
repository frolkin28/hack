import trafaret as t

BaseMessage = t.Dict(
    action=t.String,
    data=t.Any
)

# backend allows: START
JoinMessageData = t.Dict(
    room_id=t.String,
    client=t.Dict(
        peer_id=t.String,
        name=t.String,
        email=t.String,
    ),
)

LeaveMessageData = t.Dict(
    room_id=t.String,
)

RelaySDPMessageData = t.Dict(
    room_id=t.String,
    peer_id=t.Int,
    session_description=t.String,
)

RelayIceMessageData = t.Dict(
    room_id=t.String,
    peer_id=t.Int,
    ice_candidate=t.String,
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
    peer_id=t.Int,
)

SessionDescriptionMessageData = t.Dict(
    peer_id=t.Int,
    session_description=t.String,
)

IceCandidateMessageData = t.Dict(
    peer_id=t.Int,
    ice_candidate=t.String,
)
# backend respond: END
