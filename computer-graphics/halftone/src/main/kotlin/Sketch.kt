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
    private var particles: Int = 50
        set(value) {
            field = max(1, min(img.width, value))
        }

    override fun settings() {
        size(500, 700, P3D)
    }

    override fun setup() {
        img.resize(width, height)
        cam.setMinimumDistance(100.0)
        cam.setMaximumDistance(1500.0)
    }

    override fun draw() {
        translate(width / -2f, height / -2f)
        background(0xffffff.rgb)
        fill(0x111111.rgb)
        noStroke()
        ortho()

        val particleSize = width.div(particles)

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
        event?.let {
            if (it.count > 0) { // rotated down
                --particles
            } else { // rotated up
                ++particles
            }
        }
    }

    private val Int.rgb: Int
        get() = this.or(-0x1000000) // -0x1000000 == f...ff000000
}

fun main() = Sketch.run()
