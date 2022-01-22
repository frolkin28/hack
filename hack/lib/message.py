import trafaret as t

BaseMessage = t.Dict(
    action=t.String,
    data=t.Any
)

JoinMessage = t.Dict(
    peer_id=t.Int,
)

AddPeerMessage = t.Dict(
    peer_id=t.Int,
    create_offer=t.Bool,
)

RemovePeerMessage = t.Dict(
    peer_id=t.Int,
)

SessionDescriptionMessage = t.Dict(
    peer_id=t.Int,
    session_description=t.String,
)

IceCandidateMessage = t.Dict(
    peer_id=t.Int,
    ice_candidate=t.String,
)
