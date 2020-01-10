#ifndef VEC3_HH
#define VEC3_HH

#include <cmath>

struct Vec3 {
    union {
        struct { float x, y, z; };
        float D[3];
    };

    Vec3() { }
    Vec3(float x, float y, float z)
        : x(x)
        , y(y)
        , z(z) { }

    float &operator[](unsigned int i) { return D[i]; }
    const float &operator[](unsigned int i) const { return D[i]; }

    float maxComponent() const { return std::max(x, std::max(y, z)); }
    float minComponent() const { return std::min(x, std::min(y, z)); }

    Vec3 cmul(const Vec3 &v) const { return Vec3(x * v.x, y * v.y, z * v.z); }
    Vec3 cdiv(const Vec3 &v) const { return Vec3(x / v.x, y / v.y, z / v.z); }

    Vec3 operator+(const Vec3 &v) const { return Vec3(x + v.x, y + v.y, z + v.z); }
    Vec3 operator-(const Vec3 &v) const { return Vec3(x - v.x, y - v.y, z - v.z); }
    Vec3 operator*(float r) const { return Vec3(x * r, y * r, z * r); }
    Vec3 operator/(float r) const { return Vec3(x / r, y / r, z / r); }

    Vec3 &operator+=(const Vec3 &v) { x += v.x; y += v.y; z += v.z; return *this; }
    Vec3 &operator-=(const Vec3 &v) { x -= v.x; y -= v.y; z -= v.z; return *this; }
    Vec3 &operator*=(float r) { x *= r; y *= r; z *= r; return *this; }
    Vec3 &operator/=(float r) { x /= r; y /= r; z /= r; return *this; }

    float norm() const { return sqrtf(x * x + y * y + z * z); }
    float normSquared() const { return x * x + y * y + z * z; }

    Vec3 normalized() const {
        return *this / norm();
    }

    // Inner/dot product
    float operator*(const Vec3 &v) const {
        return x * v.x + y * v.y + z * v.z;
    }

    // Cross product
    Vec3 operator^(const Vec3 &v) const {
        return Vec3(y * v.z - z * v.y,
                    z * v.x - x * v.z,
                    x * v.y - y * v.x);
    }
};

inline Vec3 operator*(float r, const Vec3 &v) {
    return Vec3(v.x * r, v.y * r, v.z * r);
}

#endif