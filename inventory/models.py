from dataclasses import dataclass

@dataclass
class AssetRecord:

    
    ship_sys: str
    system: str
    equipment: str
    manufacturer: str
    model: str
    uniq_id: str
    os: str
    firmware: str
    app: str
    sec_zone: str
    function: str
    suc: str
    untrusted_network: str
    phy_interfaces: str
    comm_protocols: str
    is_neg_risk: bool
    has_ta_cert: bool
    source_sheet: str