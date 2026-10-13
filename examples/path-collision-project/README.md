# Path collision CI fixture

The CI workflow builds a synthetic ZIP containing `Common/Events.txt` and `common/events.TXT`, then verifies that ModRelease Studio blocks the cross-filesystem case collision. Generating the archive during CI keeps the repository itself cleanly cloneable on case-insensitive filesystems such as Windows.
