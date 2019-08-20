// ref.: https://www.cs.ubc.ca/~rbridson/docs/bridson-siggraph07-poissondisk.pdf

import extensions.random
import processing.core.PApplet
import processing.core.PVector

class Sketch(
    private val radius: Float,
    private val maxSampleAttempts: Int,
    private val samplesPerFrame: Int = 1
) : PApplet() {

    private val cellSize = radius / sqrt(N.toFloat())
    private val rows by lazy { floor(height / cellSize) }
    private val columns by lazy { floor(width / cellSize) }
    private val grid by lazy { Array<PVector?>(rows * columns) { null } }
    private val active = mutableListOf<PVector>()

    companion object {
        private const val N = 2 // number of dimensions
        fun run(r: Float, k: Int = 30) = Sketch(r, k).runSketch()
    }

    override fun settings() {
        size(400, 400)
    }

    override fun setup() {
        background(0f)
        strokeWeight(4f)
        stroke(255)

        val initialSample = PVector(random(width), random(height))
        grid[gridIndex(initialSample)] = initialSample
        active.add(initialSample)
    }

    override fun draw() {
        background(0f)

        repeat(times = samplesPerFrame) {
            if (active.isNotEmpty()) {
                val randomIndex = floor(random(active.size))
                val activeSample = active[randomIndex]

                var foundValidSample = false
                repeat(times = maxSampleAttempts) {
                    // TODO verify if the generated points are uniformly distributed in the annulus
                    val sample = PVector
                        .random2D()
                        .setMag(random(radius, 2 * radius))
                        .add(activeSample)

                    val col = floor(sample.x / cellSize)
                    val row = floor(sample.y / cellSize)
                    if (row in 0 until rows &&
                        col in 0 until columns &&
                        grid[col + row * columns] != null // gridIndex(sample)
                    ) { // check if the generated sample is adequately far from existing samples
                        var farEnough = true
                        (-1..1).forEach { i ->
                            (-1..1).forEach { j ->
                                val neighbor = grid[(col + i) + (row + j) * columns]
                                if (neighbor != null) {
                                    val squaredDistance = PVector.sub(sample, neighbor).magSq()
                                    farEnough = squaredDistance < radius * radius
                                }
                            }
                        }
                        if (farEnough) {
                            foundValidSample = true
                            grid[col + row * columns] = sample // gridIndex(sample)
                            active.add(sample)
                            // break
                        }
                    }
                }

                if (!foundValidSample) active.removeAt(randomIndex)
            } //else noLoop()
        }

        stroke(255f)
        strokeWeight(4f)
        for (sample in grid) {
            if (sample != null) {
                point(sample.x, sample.y)
            }
        }

        stroke(255f, 0f, 255f)
        for (sample in active) {
            point(sample.x, sample.y)
        }
    }

    private fun gridIndex(sample: PVector): Int {
        val x = floor(sample.x / cellSize)
        val y = floor(sample.y / cellSize)
        return x + y * columns
    }
}

fun main() = Sketch.run(r = 10f)