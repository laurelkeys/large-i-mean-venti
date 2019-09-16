package sampling

import extensions.circle
import extensions.stackMatrix
import processing.core.PApplet
import processing.core.PConstants
import processing.core.PVector

private class RandomAnnulus(
    private val radius: Float,
    private val samplesPerFrame: Int
) : PApplet() {
    private val offset by lazy { (2 * radius + width) / 6f }
    private val innerFactor = 0.2f

    companion object {
        fun run(radius: Float = 200f, samplesPerFrame: Int = 4) =
            RandomAnnulus(radius, samplesPerFrame).runSketch()
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
            circle(-offset, 0f, innerFactor * radius)
            // right
            circle(offset, 0f, radius)
            circle(offset, 0f, innerFactor * radius)
        }
    }

    override fun draw() {
        stroke(255)
        strokeWeight(2f)
        stackMatrix(width / 2f, height / 2f) {
            strokeWeight(4f)
            repeat(times = samplesPerFrame) {
                // left
                val leftSample = PVector
                    .random2D()
                    .setMag(random(innerFactor * radius, radius))
                stroke(255f, map(leftSample.mag(), innerFactor * radius, radius, 0f, 255f), 255f)
                point(leftSample.x - offset, leftSample.y)

                // right
                val rightSample = PVector
                    .random2D()
                    .setMag(sqrt(random(innerFactor * radius * innerFactor * radius, radius * radius)))
                stroke(255f, map(rightSample.mag(), innerFactor * radius, radius, 0f, 255f), 255f)
                point(rightSample.x + offset, rightSample.y)
            }
        }
    }
}

fun main() = RandomAnnulus.run(175f)