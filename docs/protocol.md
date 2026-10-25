# Protocol: berth

## Connecting to OpenPak

There is no Berth-specific login and no replacement guest API. The intent is
for the guest's own account and Xbox Live calls to reach OpenPak's Xbox services
through DNS and routing at the network boundary. That integration is not yet
implemented or validated, so Berth cannot sign in to OpenPak today.

## Known limitations

- No OpenPak service compatibility yet. The Xbox services run as separate
  containers on the OpenPak server and are still being built.
- The original Xbox sends its Xbox Live gateway traffic to fixed UDP port 3074,
  which another OpenPak service family also uses; how to route both is unresolved.
