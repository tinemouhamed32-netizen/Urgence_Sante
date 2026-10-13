from __future__ import annotations

from app.models.protocol import EmergencyProtocol


class ProtocolRepository:
    def __init__(self, protocols: list[EmergencyProtocol] | None = None) -> None:
        self.protocols = protocols or []

    def list_valid(self) -> list[EmergencyProtocol]:
        return [protocol for protocol in self.protocols if protocol.is_active]

    def get_by_id(self, protocol_id: str) -> EmergencyProtocol | None:
        for protocol in self.protocols:
            if protocol.protocol_id == protocol_id:
                return protocol
        return None
