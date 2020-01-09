#ifndef VEC3_HH
#define VEC3_HH

#include <algorithm>
#include <cmath>

typedef unsigned int uint;

struct Vec3;
Vec3 operator*(float r, const Vec3 &v);

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

    float &operator[](uint i) { return D[i]; }
    const float &operator[](uint i) const { return D[i]; }

    float maxComponent() const { return std::max(x, std::max(y, z)); }
    float minComponent() const { return std::min(x, std::min(y, z)); }

    Vec3 operator+(const Vec3 &r) const { return Vec3(x + r.x, y + r.y, z + r.z); }
    Vec3 operator-(const Vec3 &r) const { return Vec3(x - r.x, y - r.y, z - r.z); }

    Vec3 cmul(const Vec3 &r) const { return Vec3(x * r.x, y * r.y, z * r.z); }
    Vec3 cdiv(const Vec3 &r) const { return Vec3(x / r.x, y / r.y, z / r.z); }

    Vec3 operator*(float r) const { return Vec3(x * r, y * r, z * r); }
    Vec3 operator/(float r) const { return Vec3(x / r, y / r, z / r); }

    Vec3 &operator+=(const Vec3 &r) {
        x += r.x;
        y += r.y;
        z += r.z;
        return *this;
    }

    Vec3 &operator-=(const Vec3 &r) {
        x -= r.x;
        y -= r.y;
        z -= r.z;
        return *this;
    }

    Vec3 &operator*=(float r) {
        x *= r;
        y *= r;
        z *= r;
        return *this;
    }

    float norm() const { return sqrtf(x * x + y * y + z * z); }
    float normSquared() const { return x * x + y * y + z * z; }

    Vec3 normalized() const {
        return *this / norm();
    }

    // Inner/dot product
    float operator*(const Vec3 &r) const {
        return x * r.x + y * r.y + z * r.z;
    }

    // Cross product
    Vec3 operator^(const Vec3 &r) const {
        return Vec3(y * r.z - z * r.y,
                    z * r.x - x * r.z,
                    x * r.y - y * r.x);
    }
};

inline Vec3 operator*(float r, const Vec3 &v) {
    return Vec3(v.x * r, v.y * r, v.z * r);
}

#endif