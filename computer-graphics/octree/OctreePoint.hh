#ifndef OCTREE_POINT_HH
#define OCTREE_POINT_HH

#include "Vec3.hh"

// Simple point data type to insert into the tree.
// Have something with more interesting behavior inherit 
// from this in order to store other attributes in the tree.
class OctreePoint {
    private:
        Vec3 position;

    public:
        OctreePoint() { }
        OctreePoint(const Vec3 &position)
            : position(position) { }
        
        inline const Vec3 &getPosition() const {
            return position;
        }
        
        inline void setPosition(const Vec3 &p) {
            position = p;
        }
};

#endif