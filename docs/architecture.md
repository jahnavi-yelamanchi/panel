# Architecture

Panel is a rights-aware visual-search platform. The first implementation has
three boundaries:

1. The API owns catalog metadata, rights, ingestion state, and audit records.
2. Object storage holds original and derived partner assets; it is never public.
3. Future processing workers consume only accepted ingestion records and create
   versioned derivatives.

Every asset is scoped to a title, partner, territory, allowed surfaces, and an
expiry. Search and model indexing must use the same entitlement decision before
they return or process an asset.

