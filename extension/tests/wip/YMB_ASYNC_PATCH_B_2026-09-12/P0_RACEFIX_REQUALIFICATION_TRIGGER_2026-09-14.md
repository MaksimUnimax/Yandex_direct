# P0 race-fix requalification trigger

This QA-only checkpoint triggers exact-source requalification after production commit `9979c31d547099856a34dea5afc430279145cb6c`.

Production scope is unchanged by this file. Required gates: exact Node differential, repeated real-Chrome resource owner race, deterministic fresh-extracted package, controlled-network package contour. Real provider calls remain forbidden in automated qualification.
