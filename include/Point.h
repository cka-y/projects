#include <istream>
#include <iostream>

using namespace std;
class Point
{
public:
    int x;
    int y;
    Point(int _x=0, int _y=0);
    Point(const Point &p){
        this->x = p.x;
        this->y = p.y;
    }
    // Needed to sort array of points according to X coordinate
    static int compareX(const void* a, const void* b)
    {
        Point *p1 = (Point *)a,  *p2 = (Point *)b;
        return (p1->x - p2->x);
    }
    // Needed to sort array of points according to Y coordinate
    static int compareY(const void* a, const void* b)
    {
        Point *p1 = (Point *)a,   *p2 = (Point *)b;
        return (p1->y - p2->y);
    }
    friend istream& operator>>(istream& is, Point& p){
        is >> p.x >> p.y;
        return is;
    }
    friend ostream& operator<<(ostream& os, Point& p){
        os << "(x = " << p.x << ", y = " << p.y << ")\n";
    }
};

Point::Point(int _x, int _y)
{
    x = _x;
    y = _y;
}
