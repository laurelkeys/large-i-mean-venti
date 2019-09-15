package extensions

import processing.core.PApplet

fun PApplet.stackMatrix(x: Number = 0f, y: Number = 0f, angle: Number = 0f, transformation: () -> Unit) {
    stackMatrix(x.toFloat(), y.toFloat(), angle.toFloat(), transformation)
}

fun PApplet.stackMatrix(x: Float = 0f, y: Float = 0f, angle: Float = 0f, transformation: () -> Unit) {
    pushMatrix() // saves the current coordinate system to the stack
    if (x != 0f || y != 0f) translate(x, y)
    if (angle != 0f) rotate(angle)

    transformation()

    popMatrix() // restores the prior coordinate system
}

fun PApplet.transformPixels(transformation: () -> Unit) {
    loadPixels()
    transformation()
    updatePixels()
}

fun PApplet.circle(x: Number, y: Number, radius: Number) {
    this.ellipse(x.toFloat(), y.toFloat(), 2f * radius.toFloat(), 2f * radius.toFloat())
}

fun PApplet.random(low: Number, high: Number): Float = this.random(low.toFloat(), high.toFloat())

fun PApplet.random(high: Number): Float = this.random(high.toFloat())