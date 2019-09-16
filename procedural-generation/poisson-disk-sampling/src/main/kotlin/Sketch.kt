// ref.: https://www.cs.ubc.ca/~rbridson/docs/bridson-siggraph07-poissondisk.pdf

import extensions.circle
import extensions.random
import processing.core.PApplet
import processing.core.PVector

class Sketch(
    private val radius: Float,
    private val maxSampleAttempts: Int,
    private val samplesPerFrame: Int
) : PApplet() {

    private val cellScale = radius / sqrt(N.toFloat())

    private val rows by lazy { ceil(height / cellScale) }
    private val columns by lazy { ceil(width / cellScale) }
    private val grid by lazy { IntArray(rows * columns) { NO_POINT } }

    private val points = mutableListOf<PVector>()
    private val activePoints = mutableListOf<PVector>()

    companion object {
        private const val NO_POINT = -1
        private const val N = 2 // number of dimensions
        fun run(r: Float, k: Int = 30, spf: Int = 4) = Sketch(r, k, spf).runSketch()
    }

    // grid (rows x columns):
    //   ___    _
    //  |_|_|..|_|      grid cell:
    //  |_|_|..|_|          _
    //  :   :  : :  ==>    |_| (1 x 1)
    //  |_|_|..|_|
    private fun inGrid(u: Int, v: Int) = u in 0 until columns && v in 0 until rows

    override fun settings() {
        size(800, 600)
    }

    override fun setup() {
        background(0f)
        stroke(255)

        val initialSample = PVector(width / 2f, height / 2f) // PVector(random(width), random(height))
        val u = floor(initialSample.x / cellScale)
        val v = floor(initialSample.y / cellScale)
        grid[u + v * columns] = 0 // first sample's index

        points.add(initialSample)
        activePoints.add(initialSample)
    }

    override fun draw() {
        background(0f)
        strokeWeight(3f)

        repeat(times = samplesPerFrame) {
            if (activePoints.isNotEmpty()) {
                val randomIndex = floor(random(activePoints.size))
                val activeSample = activePoints[randomIndex]

                var candidateAccepted = false
                for (attempt in 0 until maxSampleAttempts) {
                    val candidate = PVector
                        .random2D()
                        .setMag(sqrt(random(radius * radius, 4f * radius * radius)))
                        .add(activeSample)

                    // candidate's location in the grid
                    val u = floor(candidate.x / cellScale)
                    val v = floor(candidate.y / cellScale)
                    if (isValid(candidate, u, v)) {
                        points.add(candidate)
                        activePoints.add(candidate)
                        grid[u + v * columns] = points.size - 1 // 0 based index of the accepted candidate
                        candidateAccepted = true
                    }
                }

                if (!candidateAccepted) activePoints.removeAt(randomIndex)

            } else {
                // TODO save the points list here if you want to
                noLoop() // we are finished
            }
        }

        stroke(255f)
        strokeWeight(3f)
        grid.filter { it != NO_POINT }.forEach {
            val sample = points[it]
            point(sample.x, sample.y)
        }

        stroke(255f, 0f, 255f)
        strokeWeight(5f)
        activePoints.forEach { sample ->
            point(sample.x, sample.y)
        }
    }

    private fun isValid(candidate: PVector, u: Int, v: Int): Boolean {
        if (inGrid(u, v)) {
            val delta = 1 // searches for neighbors in a (2*delta+1) x (2*delta+1) region around (u, v)
            for (t in -delta..delta) {
                for (s in -delta..delta) {
                    val neighbor = grid.getOrNull((u + s) + (v + t) * columns) ?: continue
                    if (neighbor != NO_POINT) {
                        val squaredDistance = PVector.sub(candidate, points[neighbor]).magSq()
                        if (squaredDistance < radius * radius) return false
                    }
                }
            }
            return true
        }
        return false
    }
}

fun main() = Sketch.run(r = 12f, spf = 6)