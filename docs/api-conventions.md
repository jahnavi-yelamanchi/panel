# API conventions

- Prefix public endpoints with `/v1` once a route is released.
- Use JSON request and response bodies with UTC ISO-8601 timestamps.
- Return RFC 7807-compatible error objects with a stable machine-readable
  `code` field.
- Destructive state changes are idempotent when an `Idempotency-Key` header is
  supplied.
- Asset bytes are never returned by the API. Clients receive short-lived signed
  object-storage URLs only after entitlement checks.

