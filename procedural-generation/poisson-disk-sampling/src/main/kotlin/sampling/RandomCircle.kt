package sampling

import extensions.circle
import extensions.stackMatrix
import processing.core.PApplet
import processing.core.PConstants
import processing.core.PVector

private class RandomCircle(
    private val radius: Float,
    private val samplesPerFrame: Int
) : PApplet() {
    private val offset by lazy { (2 * radius + width) / 6f }

    companion object {
        fun run(radius: Float = 200f, samplesPerFrame: Int = 4) =
            RandomCircle(radius, samplesPerFrame).runSketch()
    }

    override fun settings() {
        size(800, 600)
    }

    override fun setup() {
        background(0f)
        stroke(255)
        strokeWeight(2f)
        ellipseMode(PConstants.CENTER)
        stackMatrix(width / 2f, height / 2f) {
            noFill()
            // left
            circle(-offset, 0f, radius)
            // right
            circle(offset, 0f, radius)
        }
    }

    override fun draw() {
        strokeWeight(4f)
        stackMatrix(width / 2f, height / 2f) {
            repeat(times = samplesPerFrame) {
                // left
                val leftSample = PVector
                    .random2D()
                    .setMag(random(0f, radius))
                stroke(255f, map(leftSample.mag(), 0f, radius, 0f, 255f), 255f)
                point(leftSample.x - offset, leftSample.y)

                // right
                val rightSample = PVector
                    .random2D()
                    .setMag(sqrt(random(0f, radius * radius)))
                stroke(255f, map(rightSample.mag(), 0f, radius, 0f, 255f), 255f)
                point(rightSample.x + offset, rightSample.y)
            }
        }
    }
}

fun main() = RandomCircle.run(175f)