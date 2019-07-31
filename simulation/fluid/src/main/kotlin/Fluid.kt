import kotlin.math.pow

// ref.: https://mikeash.com/pyblog/fluid-simulation-for-dummies.html
//       https://pdfs.semanticscholar.org/847f/819a4ea14bd789aca8bc88e85e906cfc657c.pdf

typealias Real = Float // Double

const val ZERO: Real = 0f // 0.0

infix fun Int.`**`(exponent: Int): Int = this.toDouble().pow(exponent).toInt()

class Fluid(
    private val dimensions: Int,
    val size: Int, val dt: Real, val diffusion: Real, val viscosity: Real
) {

    private val sources: Array<Real>
    private val density: Array<Real>
    private val velocity: Array<Real>
    private val velocity0: Array<Real>

    init {
        val dim = size `**` dimensions
        sources = Array(dim) { ZERO }
        density = Array(dim) { ZERO }
        velocity = Array(dim) { ZERO }
        velocity0 = Array(dim) { ZERO }
    }

    fun addDensity(amount: Real, position: Array<Real>) {
        assert(position.size == dimensions)
    }
}