# py-scopes

The 'py-scopes' package is a re-implementation of a similar module in Go,
called 'go-scopes'. It processes application data focussing on changes
instead of objects or state.

The first sub-package (scopes.storage) deals with storing application data 
(as records or tracks, messages, or more specific kinds of entities)
in a SQL database, using some header columns for indexing and direct access and 
a jsonb column for the real data (payload).

Status: implementation started

Project website: https://www.cyberconcepts.org

License: MIT, see LICENSE file

