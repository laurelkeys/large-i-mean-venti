import processing.core.PApplet
import extensions.random

class Sketch : PApplet() {

    companion object {
        fun run() = Sketch().runSketch()
    }

    override fun settings() {
        size(400, 400)
    }

    override fun setup() {
        background(0f)
        strokeWeight(4f)
        stroke(255)
        repeat(times = 1000) {
            point(random(width), random(height))
        }
    }


    override fun draw() {

    }
}

fun main() = Sketch.run()