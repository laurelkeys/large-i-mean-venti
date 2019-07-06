import processing.core.PApplet
import processing.core.PImage

// ref.: https://timrodenbroeker.de/how-to-rasterize-an-image-with-processing/

class Sketch : PApplet() {

    companion object {
        fun run() = Sketch().runSketch()
    }

    private val img: PImage by lazy { loadImage("woman.jpg") }

    override fun settings() {
        size(500, 700)
    }

    override fun setup() {
        img.resize(width, height)
    }

    override fun draw() {
        background(0xffffff.rgb)
        fill(0x111111.rgb)
        noStroke()

        val particles = map(mouseX / 1f, 0f, width / 1f, 0f, img.width / 2f)
        val particleSize = width.div(particles).toInt()
        img.loadPixels()
        for (y in 0 until img.height step particleSize) {
            for (x in 0 until img.width step particleSize) {
                val color = img.pixels[x + y * img.width]
                val darkness = map(brightness(color), 0f, 255f, 1f, 0f)
                pushPop(x / 1f, y / 1f) {
                    rect(0f, 0f, particleSize * darkness, particleSize * darkness)
                }
            }
        }
    }

    private val Int.rgb: Int
        get() = this.or(-0x1000000) // -0x1000000 == f...ff000000
}

fun main() = Sketch.run()
