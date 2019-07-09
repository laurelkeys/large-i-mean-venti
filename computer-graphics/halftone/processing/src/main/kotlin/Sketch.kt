import peasy.PeasyCam
import peasy.PeasyWheelHandler
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
    private var particleSize = 10
        set(value) {
            field = max(1, min(250, value))
        }

    override fun settings() {
        size(500, 700, P3D)
    }

    override fun setup() {
        img.resize(width, height)
        cam.setMinimumDistance(700.0)
        cam.setMaximumDistance(700.0)
        cam.wheelHandler = PeasyWheelHandler { }
    }

    override fun draw() {
        background(0xffffff.rgb)
        fill(0x111111.rgb)
        noStroke()
        ortho()

        img.loadPixels()
        for (y in img.height / -2 until img.height / 2 step particleSize) {
            for (x in img.width / -2 until img.width / 2 step particleSize) {
                val offset = (x + img.width / 2) + (y + img.height / 2) * img.width
                val color = img.pixels[offset]
                val darkness = map(brightness(color), 0f, 255f, 1f, 0f)
                stackMatrix(x, y, darkness * 150) {
                    box(particleSize * darkness)
                }
            }
        }
    }

    override fun mouseWheel(event: MouseEvent?) {
        event?.also {
            if (it.count > 0) { // rotated down
                --particleSize
            } else { // rotated up
                ++particleSize
            }
        }
    }

    private val Int.rgb: Int
        get() = this.or(-0x1000000) // -0x1000000 == f...ff000000
}

fun main() = Sketch.run()
