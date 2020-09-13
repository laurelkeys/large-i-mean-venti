// Reference: "Fluid Engine Development", Doyub Kim

#include <array>
#include <chrono>
#include <cmath>
#include <cstdio>
#include <iostream>
#include <thread>

constexpr std::size_t buffer_size = 80;

constexpr char const* grayscale_table = " .:-=+*#%@";
constexpr std::size_t grayscale_table_size = std::char_traits<char>::length(grayscale_table);

constexpr double pi() {
    return std::atan(1.0) * 4.0;
}

struct Wave {
    /// Defines the state of a 1D wave
    struct State {
        double pos;
        double speed;
    } state;

    /// Specifies the shape of a wave (used for visualization)
    struct Shape {
        double length;
        double height;
    } shape;
};

/// Updates the `wave`'s state given the input `time_interval`
void update_wave(double const time_interval, Wave::State* wave) {
    double const displacement = time_interval * wave->speed;
    wave->pos += displacement;

    // Boundary reflection
    if (wave->pos > 1.0) {
        wave->speed *= -1.0;
        wave->pos = 1.0 + displacement;
    } else if (wave->pos < 0.0) {
        wave->speed *= -1.0;
        wave->pos = displacement;
    }
}

/// Maps the `wave` points to the `height_field` for visualization
void accumulate_wave_to_height_field(Wave const& wave, double (*height_field)[buffer_size]) {
    auto const& old_pos = wave.state.pos;
    auto const& [max_height, length] = wave.shape;
    double const quarter_wave_length = 0.25 * length;

    int const start = static_cast<int>((old_pos - quarter_wave_length) * buffer_size);
    int const end = static_cast<int>((old_pos + quarter_wave_length) * buffer_size);

    // Assuming waves have a cosine shape centered at `pos`,
    // add the clamped cosine function to the input `height_field`
    for (int i = start; i < end; ++i) {
        int const new_i = [i](int const max_i) {
            if (i < 0) return -(i + 1);
            if (i >= max_i) return 2 * max_i - (i + 1);
            return i;
        }(static_cast<int>(buffer_size));

        double const distance = std::fabs((i + 0.5) / buffer_size - old_pos);

        (*height_field)[new_i] +=
            0.5 * max_height * (1.0 + std::cos(std::min(distance * pi() / quarter_wave_length, pi())));
    }
}

void draw(double const (&height_field)[buffer_size]) {
    std::string buffer(buffer_size, ' ');

    // Convert height field to ASCII grayscale
    for (std::size_t i = 0; i < buffer_size; ++i) {
        auto const height = height_field[i];
        auto const table_index = static_cast<std::size_t>(std::floor(grayscale_table_size * height));

        buffer[i] = grayscale_table[std::min(table_index, grayscale_table_size - 1)];
    }

    // Clear old prints
    for (std::size_t i = 0; i < buffer_size; ++i) printf("\b");

    // Draw new buffer
    printf("%s", buffer.c_str());
    fflush(stdout);
}

int main() {
    Wave x { { 0.0, 1.0 }, { 0.8, 0.5 } };
    Wave y { { 1.0, -0.5 }, { 1.2, 0.4 } };

    int const fps = 100;
    double const time_interval = 1.0 / fps;

    // @Note: each 0, 1, ..., N − 1 element of the array stores the
    // height of the waves at location 0.5/N, 1.5/N, ..., N − 0.5/N
    double height_field[buffer_size];

    for (int i = 0; i < 1000; ++i) {
        // March through time
        update_wave(time_interval, &x.state);
        update_wave(time_interval, &y.state);

        // Clear height field
        for (double& height : height_field) height = 0.0;

        // Accumulate waves for each center point
        accumulate_wave_to_height_field(x, &height_field);
        accumulate_wave_to_height_field(y, &height_field);

        // Draw height field
        draw(height_field);

        std::this_thread::sleep_for(std::chrono::milliseconds(1000 / fps));
    }

    printf("\n");
    fflush(stdout);

    return 0;
}
