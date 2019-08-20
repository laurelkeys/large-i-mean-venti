// ref.: https://www.cs.ubc.ca/~rbridson/docs/bridson-siggraph07-poissondisk.pdf

import extensions.random
import processing.core.PApplet
import processing.core.PVector

class Sketch(
    private val radius: Float,
    private val maxSampleAttempts: Int,
    private val samplesPerFrame: Int = 4
) : PApplet() {

    private val cellScale = radius / sqrt(N.toFloat())
    private val rows by lazy { floor(height / cellScale) }
    private val columns by lazy { floor(width / cellScale) }
    private val grid by lazy { arrayOfNulls<PVector>(rows * columns) }
    private val active = mutableListOf<PVector>()

    companion object {
        private const val N = 2 // number of dimensions
        fun run(r: Float, k: Int = 30) = Sketch(r, k).runSketch()
    }

    // grid (rows x columns):
    //   ___    _
    //  |_|_|..|_|      grid cell:
    //  |_|_|..|_|          _
    //  :   :  : :  ==>    |_| (cellScale x cellScale)
    //  |_|_|..|_|
    private fun inGrid(u: Int, v: Int) = u in 0 until columns && v in 0 until rows

    override fun settings() {
        size(800, 600)
    }

    override fun setup() {
        background(0f)
        stroke(255)

        val initialSample = PVector(random(width), random(height))
        val u = floor(initialSample.x / cellScale)
        val v = floor(initialSample.y / cellScale)
        grid[u + v * columns] = initialSample
        active.add(initialSample)
    }

    override fun draw() {
        background(0f)
        strokeWeight(4f)

        repeat(times = samplesPerFrame) {
            if (active.isNotEmpty()) {
                val randomIndex = floor(random(active.size))
                val activeSample = active[randomIndex]

                var foundValidSample = false
                for (attempt in 0 until maxSampleAttempts) {
                    // TODO verify if the generated points are uniformly distributed in the annulus
                    val sample = PVector
                        .random2D()
                        .setMag(random(radius, 2 * radius))
                        .add(activeSample)

                    // sample's location in the grid
                    val u = floor(sample.x / cellScale)
                    val v = floor(sample.y / cellScale)

                    // check if the generated sample is new and adequately far from existing samples
                    if (inGrid(u, v) && grid[u + v * columns] == null) {
                        var farEnough = true
                        (-1..1).forEach { i ->
                            (-1..1).forEach { j ->
                                val neighbor = grid.getOrNull((u + i) + (v + j) * columns)
                                if (neighbor != null) {
                                    val squaredDistance = PVector.sub(sample, neighbor).magSq()
                                    farEnough = squaredDistance >= radius * radius
                                }
                            }
                        }
                        if (farEnough) {
                            foundValidSample = true
                            grid[u + v * columns] = sample
                            active.add(sample)
                            break
                        }
                    }
                }

                if (!foundValidSample) active.removeAt(randomIndex)

            } else noLoop()
        }

        stroke(255f)
        strokeWeight(4f)
        for (sample in grid) {
            if (sample != null) point(sample.x, sample.y)
        }

        stroke(255f, 0f, 255f)
        strokeWeight(6f)
        for (sample in active) {
            point(sample.x, sample.y)
        }
    }
}

fun main() = Sketch.run(r = 24f)