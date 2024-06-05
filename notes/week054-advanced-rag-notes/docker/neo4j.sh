docker run \
    --name neo4j \
    -p 7474:7474 -p 7687:7687 \
    -d \
    -e NEO4J_AUTH=neo4j/password \
    -e 'NEO4J_PLUGINS=["apoc"]'  \
    -e 'NEO4JLABS_PLUGINS=["apoc"]' \
    neo4j:latest
