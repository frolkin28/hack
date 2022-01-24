const ACTION = {
  JOIN: 'join',
  LEAVE: 'leave',
  ADD_PEER: 'add-peer',
  REMOVE_PEER: 'remove-peer',
  RELAY_SDP: 'relay-sdp',
  RELAY_ICE: 'relay-ice',
  ICE_CANDIDATE: 'ice-candidate',
  SESSION_DESCRIPTION: 'session-description',
  DELETE_CLIENT: 'delete-client',
  CLIENT_DELETED: 'client-deleted',
  RECONNECT: 'reconnect',
};

export default ACTION;
