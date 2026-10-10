# Payload models are a lens, not a gate

The payload models type what GitHub sends; they never refuse it. An unmodelled event type is accepted into a fallback that keeps the raw payload, fields the models do not know are kept rather than dropped, and a payload that fails validation is logged with its error and still acknowledged with a 2xx. The reason is that a refused delivery is a lost delivery — GitHub does not redeliver a delivery that failed — so a model stricter than GitHub's own documentation rejects real traffic permanently and silently, and models that drop unknown fields cannot record changes GitHub makes to a payload.

## Considered Options

- **Strict gate** — unknown event types and unmodelled fields are rejected with a 4xx. Gives a clean promise that everything downstream sees is modelled, at the cost of losing deliveries whenever GitHub adds an event type or a field.
- **Gate on event type only** — refuse event types with no model, tolerate field drift within them. Prevents garbage from flowing downstream, still loses every delivery for a newly introduced event type.
- **Lens** (chosen) — type and record, never refuse.

## Consequences

- Validation failures are visible only in the logs; GitHub sees a successful delivery either way.
- The models may lag GitHub's payloads without breaking the endpoint, so "is this payload modelled?" has to be readable from the acknowledgement and the log rather than from an error.
- Anything downstream must tolerate a payload whose type it does not recognise.
