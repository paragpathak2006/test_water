#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
namespace py = pybind11;

#include "wrapper.cpp"
#include "helpers.cpp"

// Pybind Test
void bind_test(py::module_& m) {
    m.def("test", []() {
        return "✅✅Pybind Success✅✅";
    });
}

// CAGL Test
void bind_get_cgal_version(py::module_& m){m.def("get_cgal_version", []() {return get_cgal_version();});}
void bind_print_cgal_version(py::module_& m){m.def("print_cgal_version", []() { print_cgal_version();});}

// Forward declarations
void bind_convex_hull(py::module_& m);
void bind_self_difference(py::module_& m);
void bind_self_difference_and_split(py::module_& m);
void bind_self_difference_split_intersection_difference(py::module_& m);

PYBIND11_MODULE(cgal_module, m) {
    bind_test(m);

    bind_get_cgal_version(m);
    bind_print_cgal_version(m);

    bind_convex_hull(m);
    bind_self_difference(m);
    bind_self_difference_and_split(m);
    bind_self_difference_split_intersection_difference(m);
}

void bind_convex_hull(py::module_& m){
    m.def("convex_hull", [](py::array_t<double> V,
                                py::array_t<int> F) {

        Mesh original,hull;
        numpy_to_mesh(V, F, original);
        convex_hull(original, hull);
        return mesh_to_numpy(hull);
    });
}


void bind_self_difference(py::module_& m){
    m.def("self_difference", [](py::array_t<double> V,
                                py::array_t<int> F) {

        Mesh original,self_difference_mesh;
        numpy_to_mesh(V, F, original);
        self_difference(original, self_difference_mesh);
        return mesh_to_numpy(self_difference_mesh);
    });
}

void bind_self_difference_and_split(py::module_& m){

m.def("self_difference_and_split", [](py::array_t<double> V,
                                py::array_t<int> F) {
        Mesh original;
        MESHES components;

        numpy_to_mesh(V, F, original);
        self_difference_and_split(original, components);
        return mesh_to_numpy(components);
    });
}

void bind_self_difference_split_intersection_difference(py::module_& m){
    m.def("self_difference_split_intersection_difference", [](
        py::array_t<double> V,
        py::array_t<int> F)
    {

        Mesh original;
        std::vector<Mesh> components;
        std::vector<Mesh> intersections;
        std::vector<Mesh> differences;
        
        numpy_to_mesh(V, F, original);
        
        self_difference_split_intersection_difference(original, components, intersections, differences);
        return mesh_to_numpy(components, intersections, differences);
    });
}

    // std::string name = "C_difference";     
    // auto start = std::chrono::steady_clock::now();
    // auto end = std::chrono::steady_clock::now(); 
    // std::chrono::duration<double> elapsed_seconds = end - start ; 
    // performance[name] = elapsed_seconds.count();
