# Download a maven package with dependencies to local maven repository '~/.m2/repository'
# Supported maven repositories are defined in 'pom.xml'

ARTIFACT=$1
PACKAGING=${2:jar}
EXTRA=$3

mvn dependency:get -Dartifact=$ARTIFACT:$PACKAGING $EXTRA #-Dtransitive=false

if [[ "$PACKAGING" -ne "pom" ]]; then
    mvn dependency:get -Dartifact=$ARTIFACT:jar:sources
fi
