# eval/

The evaluation harness for the agent itself — maps directly onto the
module's design → test → evaluate → refine cycle (Week 3), and onto the
Week 11 report's requirement to "systematically evaluate the agent using
appropriate test scenarios, criteria and metrics."

A simple approach: a set of sample lost/found descriptions with the
attributes you'd expect extracted, and known lost-to-found pairs you'd
expect the agent to match. Re-run this set after every prompt change and
track accuracy over time — this is also your evidence trail for the
evaluation section of the report.
