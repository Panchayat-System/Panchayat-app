from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .models import Ticket, WhatsAppMessage


@dataclass
class InMemoryStore:
    messages: List[WhatsAppMessage] = field(default_factory=list)
    tickets: List[Ticket] = field(default_factory=list)

    def add_message(self, message: WhatsAppMessage) -> None:
        self.messages.append(message)

    def add_ticket(self, ticket: Ticket) -> None:
        self.tickets.append(ticket)


store = InMemoryStore()
