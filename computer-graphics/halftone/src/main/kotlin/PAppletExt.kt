import processing.core.PApplet

fun PApplet.pushPop(x: Float = 0f, y: Float = 0f, angle: Float = 0f, transformation: () -> Unit) {
    pushMatrix() // saves the current coordinate system to the stack
    translate(x, y)
    rotate(angle)

    transformation()

    popMatrix() // restores the prior coordinate system
}