from trafaret import Dict, String, Int, Bool

config_trafaret = Dict(
    host=String(max_length=64),
    port=Int(gt=0),
    is_debug=Bool,
    static_root=String(max_length=256)
)
