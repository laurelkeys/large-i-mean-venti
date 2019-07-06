import org.jetbrains.kotlin.gradle.tasks.KotlinCompile

plugins {
    kotlin("jvm") version "1.3.21"
}

group = "laurelkeys"
version = "1.0"

repositories {
    mavenCentral()
}

dependencies {
    implementation(kotlin("stdlib-jdk8"))
    compile(group="org.processing", name="core", version="3.3.7")
}

tasks.withType<KotlinCompile> {
    kotlinOptions.jvmTarget = "1.8"
}