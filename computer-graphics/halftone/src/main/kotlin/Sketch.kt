import peasy.PeasyCam
import processing.core.PApplet
import processing.core.PImage
import processing.event.MouseEvent

// ref.: https://timrodenbroeker.de/how-to-rasterize-an-image-with-processing/

class Sketch : PApplet() {

    companion object {
        fun run() = Sketch().runSketch()
    }

    private val img: PImage by lazy { loadImage("woman.jpg") }
    private val cam: PeasyCam by lazy { PeasyCam(this, width / 1.0) }
    private var particleSizes = listOf(
        //1, 2, 3,
        4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
        15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
        26, 27, 28, 30, 32, 34, 36, 39, 42, 46,
        51, 56, 63, 72, 84, 103, 128, 168
    ) // FIXME generate procedurally
    private var particleSizeIndex = 4
        set(value) {
            field = max(0, min(particleSizes.size - 1, value))
        }

    override fun settings() {
        size(500, 700, P3D)
    }

    override fun setup() {
        img.resize(width, height)
        cam.setMinimumDistance(100.0)
        cam.setMaximumDistance(1500.0)
        print(particleSizes)
    }

    override fun draw() {
        translate(width / -2f, height / -2f)
        background(0xffffff.rgb)
        fill(0x111111.rgb)
        noStroke()
        ortho()

        val particleSize = particleSizes[particleSizeIndex]
        img.loadPixels()
        for (y in 0 until img.height step particleSize) {
            for (x in 0 until img.width step particleSize) {
                val color = img.pixels[x + y * img.width]
                val darkness = map(brightness(color), 0f, 255f, 1f, 0f)
                stackMatrix(x, y, darkness * 100) {
                    box(particleSize * darkness)
                }
            }
        }
    }

    override fun mouseWheel(event: MouseEvent?) {
        event?.also {
            if (it.count > 0) { // rotated down
                --particleSizeIndex
            } else { // rotated up
                ++particleSizeIndex
            }
        }
    }

    private val Int.rgb: Int
        get() = this.or(-0x1000000) // -0x1000000 == f...ff000000
}

fun main() = Sketch.run()
