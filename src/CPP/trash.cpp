// module.cpp

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <CGAL/Simple_cartesian.h>
#include <CGAL/convex_hull_2.h>

#include <vector>

namespace py = pybind11;

// Define CGAL kernel
typedef CGAL::Simple_cartesian<double> Kernel;
typedef Kernel::Point_2 Point_2;

std::vector<std::pair<double, double>>
convex_hull(const std::vector<std::pair<double, double>>& input_points)
{
    std::vector<Point_2> points;
    for (const auto& p : input_points) {
        points.emplace_back(p.first, p.second);
    }

    std::vector<Point_2> result;
    CGAL::convex_hull_2(points.begin(), points.end(), std::back_inserter(result));

    std::vector<std::pair<double, double>> output;
    for (const auto& p : result) {
        output.emplace_back(p.x(), p.y());
    }

    return output;
}

PYBIND11_MODULE(cgal_module, m) {
    m.def("self_difference", &convex_hull);
}