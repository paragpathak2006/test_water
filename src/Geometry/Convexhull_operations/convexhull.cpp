#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

#include <CGAL/Exact_predicates_exact_constructions_kernel.h>
#include <CGAL/Surface_mesh.h>
#include <CGAL/convex_hull_3.h>
#include <CGAL/Polygon_mesh_processing/corefinement.h>

namespace py = pybind11;
namespace PMP = CGAL::Polygon_mesh_processing;

typedef CGAL::Exact_predicates_exact_constructions_kernel Kernel;
typedef Kernel::Point_3 Point;
typedef CGAL::Surface_mesh<Point> Mesh;
Mesh compute_hull(const Mesh& input)
{
    Mesh hull;
    CGAL::convex_hull_3(input.points().begin(),
                        input.points().end(),
                        hull);
    return hull;
}

Mesh self_difference(py::array_t<double> V,
                     py::array_t<int> F)
{
    Mesh original = numpy_to_mesh(V, F);
    Mesh hull = compute_hull(original);
    Mesh result;

    PMP::corefine_and_compute_difference(
        hull,
        original,
        result
    );

    return result;
}
Mesh numpy_to_mesh(py::array_t<double> V,
                   py::array_t<int> F)
{
    auto v = V.unchecked<2>();
    auto f = F.unchecked<2>();

    Mesh mesh;
    std::vector<Mesh::Vertex_index> verts;

    for (ssize_t i = 0; i < v.shape(0); ++i) {
        verts.push_back(mesh.add_vertex(
            Point(v(i,0), v(i,1), v(i,2))));
    }

    for (ssize_t i = 0; i < f.shape(0); ++i) {
        mesh.add_face(
            verts[f(i,0)],
            verts[f(i,1)],
            verts[f(i,2)]);
    }

    return mesh;
}

py::tuple mesh_to_numpy(const Mesh& mesh)
{
    std::vector<Point> verts;
    std::vector<std::array<int,3>> faces;

    std::map<Mesh::Vertex_index, int> index_map;
    int idx = 0;

    for (auto v : mesh.vertices()) {
        index_map[v] = idx++;
        verts.push_back(mesh.point(v));
    }

    for (auto f : mesh.faces()) {
        std::array<int,3> tri;
        int i = 0;
        for (auto v : vertices_around_face(
                 mesh.halfedge(f), mesh))
        {
            tri[i++] = index_map[v];
        }
        faces.push_back(tri);
    }

    py::array_t<double> V({(ssize_t)verts.size(),3});
    py::array_t<int> F({(ssize_t)faces.size(),3});

    auto v_out = V.mutable_unchecked<2>();
    auto f_out = F.mutable_unchecked<2>();

    for (size_t i=0;i<verts.size();++i) {
        v_out(i,0)=CGAL::to_double(verts[i].x());
        v_out(i,1)=CGAL::to_double(verts[i].y());
        v_out(i,2)=CGAL::to_double(verts[i].z());
    }

    for (size_t i=0;i<faces.size();++i) {
        f_out(i,0)=faces[i][0];
        f_out(i,1)=faces[i][1];
        f_out(i,2)=faces[i][2];
    }

    return py::make_tuple(V,F);
}

PYBIND11_MODULE(cgal_module, m) {
    m.def("self_difference", [](py::array_t<double> V,
                                py::array_t<int> F) {
        Mesh result = self_difference(V,F);
        return mesh_to_numpy(result);
    });
}

#include <CGAL/Polygon_mesh_processing/connected_components.h>
#include <CGAL/Polygon_mesh_processing/connected_components.h>
#include <boost/graph/graph_traits.hpp>

namespace PMP = CGAL::Polygon_mesh_processing;

std::vector<std::size_t> component_ids(
    num_faces(result_mesh));

std::size_t num = PMP::connected_components(
    result_mesh,
    boost::make_iterator_property_map(
        component_ids.begin(),
        get(boost::face_index, result_mesh)
    )
);

#include <CGAL/Polygon_mesh_processing/connected_components.h>

std::vector<Mesh> components;
components.resize(num);

PMP::split_connected_components(result_mesh, components);

