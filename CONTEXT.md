# GitHub Webhooks

The receiving surface for GitHub's webhook deliveries: every delivery arrives here, is typed, and is recorded. Nothing is decided here yet — this context exists so that the shape GitHub sends is pinned down before anything acts on it.

## Language

**Delivery**:
One HTTP POST from GitHub carrying one payload, identified by the delivery ID GitHub gives it.
_Avoid_: Event, notification, message, request

**Event Type**:
The kind of activity a delivery reports, declared by GitHub in the delivery's event header. An event type names what happened in general terms (`issues`, `push`), never a specific occurrence.
_Avoid_: Event, event name, type, topic

**Payload**:
The JSON document carried by a delivery, describing the occurrence the delivery reports.
_Avoid_: Event, message, body, data

**Action**:
The sub-kind of activity within an event type (`opened`, `closed`, `synchronize`). Only event types that have sub-kinds carry one; a payload without an action is complete as it stands.
_Avoid_: Subtype, verb, operation, event action

**Envelope**:
The fields every payload carries regardless of event type: the sender, and the references to the subject the delivery concerns (repository, organization, installation).
_Avoid_: Header, metadata, common fields

**Unmodelled Event**:
A payload whose event type has no dedicated model. It is accepted and retained like any other delivery; the absence of a model never makes it a refusal.
_Avoid_: Unknown event, unsupported event, unrecognized event

**Acknowledgement**:
The JSON document returned to GitHub for an accepted delivery, naming the delivery and what it carried.
_Avoid_: Response, reply, ack, receipt
