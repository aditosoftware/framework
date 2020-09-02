# Versioning

For the internal distribution we use a custom versioning scheme to identify the actual framework version and internal changes.

E.g. if the branch is based on Vaadin version *8.11.2* with the default patches, the following custom version shall be used:

**8.11.2.adito.0** (For snapshots, just add *-SNAPSHOT*)

The first part identifies the actual Vaadin version, followed by the keyword *"adito"* and an additional incremental integer.

When adding internal changes we just increment the last integer (based on the previous example, the new version shall be **8.11.2.adito.1**).

