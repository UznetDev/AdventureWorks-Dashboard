name := "mssql-mleap-app"

version := "1.0"

scalaVersion := "2.11.12"

libraryDependencies ++= Seq(
  "ml.combust.mleap" %% "mleap-runtime" % "0.13.0" % "provided",
  "org.apache.commons" % "commons-csv" % "1.5",
  "commons-cli" % "commons-cli" % "1.4",
  "org.scalatest" %% "scalatest" % "3.2.0-SNAP10" % Test,
  "org.scalacheck" %% "scalacheck" % "1.14.0" % Test,
  "com.novocode" % "junit-interface" % "0.11" % Test
)

// Exclude scala-library from this fat jar. The scala library is already there in spark package.
assemblyOption in assembly := (assemblyOption in assembly).value.copy(includeScala = false)

// exclude specific jars
assemblyExcludedJars in assembly := {
  val cp = (fullClasspath in assembly).value
  cp filter {_.data.getName == "mssql_java_lang_extension.jar"}
}
