# ADR 0001: rights are a first-class boundary

## Decision

Store partner rights in the transactional catalog and require an active right
before an asset can move from quarantine to processing, indexing, or delivery.

## Consequences

Each derivative retains its source asset ID. Rights expiry or revocation drives
one deletion workflow across object storage, processing queues, and future
search indexes.
