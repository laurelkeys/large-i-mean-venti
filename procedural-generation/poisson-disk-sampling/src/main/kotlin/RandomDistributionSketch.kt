import extensions.stackMatrix
import processing.core.PApplet
import processing.core.PConstants
import processing.core.PVector

class RandomDistributionSketch(
    private val radius: Float,
    private val samplesPerFrame: Int = 4
) : PApplet() {

    companion object {
        fun run(radius: Float = 200f) = RandomDistributionSketch(radius).runSketch()
    }

    override fun settings() {
        size(800, 600)
    }

    override fun setup() {
        background(0f)
        stroke(255)
        colorMode(PConstants.HSB)
        ellipseMode(PConstants.CENTER)
        stackMatrix(width / 2f, height / 2f) {
            noFill()
            ellipse(0f, 0f, 2f * radius, 2f * radius)
        }
    }

    override fun draw() {
        strokeWeight(4f)
        stackMatrix(width / 2f, height / 2f) {
            repeat(times = samplesPerFrame) {
                val sample = PVector
                    .random2D()
                    .setMag(random(0f, radius))
                stroke(
                    map(sample.mag(), 0f, radius, 0f, 255f),
                    255f, 255f
                )
                point(sample.x, sample.y)
            }
        }
    }
}

fun main() = RandomDistributionSketch.run()