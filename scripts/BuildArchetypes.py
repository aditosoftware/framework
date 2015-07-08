#coding=UTF-8

#
# Windows users: 
# You need to setup your environment so that you have mvn on your PATH.
# Maven needs that JAVA_HOME environment is set and points to a JDK
# Python3 is required as this script uses some Python3 specific features.
# Might work with Python2, haven't tested.
#
# python BuildArchetypes.py version fw-repo-id archetype-repo-id plugin-repo-id
#

import subprocess, sys
from BuildHelpers import mavenValidate, copyWarFiles, getLogFile, mavenCmd, updateRepositories, getArgs, removeDir, parser, resultPath
from DeployHelpers import deployWar

## DEFAULT VARIABLES ##

# ArchetypeGroupId
archetypeGroup = "com.vaadin"

# List of built archetypes
archetypes = [
	"vaadin-archetype-widget", 
	"vaadin-archetype-application", 
	"vaadin-archetype-application-example",
	"vaadin-archetype-application-multimodule"
]

# Maven GroupID
group = "testpkg"

log = None
args = None

## BUILDING METHODS ##

# Generates and modifies a maven pom file
def generateArchetype(archetype, artifactId):
	# Generate the required command line for archetype generation
	cmd = [mavenCmd, "archetype:generate"]
	cmd.append("-DarchetypeGroupId=%s" % (archetypeGroup))
	cmd.append("-DarchetypeArtifactId=%s" % (archetype))
	cmd.append("-DarchetypeVersion=%s" % (args.version))
	if hasattr(args, "archetype") and args.archetype != None:
		cmd.append("-DarchetypeRepository=%s" % (repo % (args.archetype)))
	cmd.append("-DgroupId=%s" % (group))
	cmd.append("-DartifactId=%s" % (artifactId))
	cmd.append("-Dversion=1.0-SNAPSHOT")
	cmd.append("-DinteractiveMode=false")
	if hasattr(args, "maven") and args.maven is not None:
		cmd.extend(args.maven.strip('"').split(" "))
	
	# Generate pom.xml
	print("Generating pom.xml for archetype %s" % (archetype))
	subprocess.check_call(cmd, cwd=resultPath, stdout=log)
	
## DO THIS IF RUN AS A SCRIPT (not import) ##
if __name__ == "__main__":
	# Add command line arguments for staging repos
	parser.add_argument("framework", type=int, help="Framework repo id (comvaadin-XXXX)", nargs='?')
	parser.add_argument("archetype", type=int, help="Archetype repo id (comvaadin-XXXX)", nargs='?')
	parser.add_argument("plugin", type=int, help="Maven Plugin repo id (comvaadin-XXXX)", nargs='?')
	parser.add_argument("--repo", type=str, help="Staging repository template", required=True)

	archetypesFailed = False

	# Parse the arguments
	args = getArgs()

	if hasattr(args, "artifactPath") and args.artifactPath is not None:
		raise Exception("Archetype validation build does not support artifactPath")

	for archetype in archetypes:
		artifactId = "test-%s-%s" % (archetype, args.version.replace(".", "-"))
		try:
			log = getLogFile(archetype)
			generateArchetype(archetype, artifactId)
			updateRepositories(artifactId)
			mavenValidate(artifactId, logFile=log)	
			warFiles = copyWarFiles(artifactId, name=archetype)
			for war in warFiles:
				try:
					deployWar(war, "%s-%s.war" % (archetype.split("-", 2)[2], args.version))
				except Exception as e:
					print("War %s failed to deploy: %s" % (war, e))
					archetypesFailed = True
		except Exception as e:
			print("Archetype %s build failed" % (archetype, e))
			archetypesFailed = True
		removeDir(artifactId)
		print("")
	if archetypesFailed:
		sys.exit(1)
