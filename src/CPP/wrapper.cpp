
#include <CGAL/number_utils.h>
#include <CGAL/Exact_predicates_exact_constructions_kernel.h>
#include <CGAL/Surface_mesh.h>
#include <CGAL/convex_hull_3.h>
#include <vector>
#include <array>
#include <unordered_map>
#include <CGAL/Polygon_mesh_processing/connected_components.h>
#include <boost/graph/graph_traits.hpp>
#include <CGAL/Polygon_mesh_processing/corefinement.h>
#include <chrono>
#include <iostream>
#include <string>
#include <CGAL/IO/polygon_mesh_io.h>
#include <CGAL/Surface_mesh.h>
#include <CGAL/AABB_tree.h>
#include <CGAL/AABB_face_graph_triangle_primitive.h>
#include <CGAL/Side_of_triangle_mesh.h>


// typedef CGAL::Surface_mesh<Point> Mesh;
namespace PMP = CGAL::Polygon_mesh_processing;
typedef CGAL::Exact_predicates_exact_constructions_kernel Kernel;
typedef Kernel::Point_3 Point;
using Mesh = CGAL::Surface_mesh<Point>;
using MESHES = std::vector<Mesh>;
typedef CGAL::Side_of_triangle_mesh<Mesh, Kernel> PMC;

typedef CGAL::AABB_face_graph_triangle_primitive<Mesh>      Primitive;
typedef CGAL::AABB_traits_3<Kernel, Primitive> Traits;
typedef CGAL::AABB_tree<Traits> Tree;

// Checks
#include <CGAL/version.h>
std::string get_cgal_version(){return std::string(CGAL_VERSION_STR);}
void print_cgal_version(){std::cout<<std::string(CGAL_VERSION_STR)<<std::endl;}
void print_mesh(std::string name, const Mesh& mesh){
    std::cout<<"\n\n Print mesh : "<<name<<"\n"<<" : num vertices : "<<mesh.number_of_vertices()<<"\n";
    std::cout<<" : num faces : "<<mesh.number_of_faces()<<"\n\n";
}
void get_intersection_difference(Mesh& A, Mesh& B, Mesh& C, Mesh& D);

void convex_hull(Mesh& input,Mesh& hull);
void get_components(Mesh& mesh, MESHES& components);
void split_into_disjoint_meshes(Mesh& mesh, MESHES& components);
void self_difference(Mesh& original,Mesh& result);
void self_difference_and_split(Mesh& original,MESHES& components);
void self_difference_split_intersection_difference(Mesh& original,MESHES& components,MESHES& intersections,MESHES& differences);


bool is_point_on_mesh(const Tree& tree, const Point& p)
{
    double eps = 1e-12;
    // std::cout<<"p = "<<p<<" , d = "<<tree.squared_distance(p)<<"\n";
    return tree.squared_distance(p) < eps;
}

void writeSTL(Mesh& result, std::string name) {
    print_mesh(name, result);
    if (CGAL::IO::write_polygon_mesh(name,result,CGAL::parameters::stream_precision(17)))
        std::cout << "Success wrting "  + name + "\n";
    else
        std::cerr << "Failed to write  "  + name + "\n";
}
void convex_hull(Mesh& input, Mesh& hull)
{

    CGAL::convex_hull_3(input.points().begin(),
                        input.points().end(),
                        hull);
}


void self_difference(Mesh& original,Mesh& result)
{

    std::cout << "\n\nCGAL_VERSION = "<<CGAL_VERSION_STR << "\n\n";
    Mesh hull;

    auto start = std::chrono::high_resolution_clock::now();
    convex_hull(original,hull);

    // writeSTL(original,"original.stl");
    // writeSTL(hull,"hull.stl");

    bool ok = PMP::corefine_and_compute_difference(hull,original,result);

    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    std::cout << "self_difference(Hull + Boolean Diff) Execution time: " << duration.count() << " µs\n\n";

    // ... build mesh or compute boolean result ...
    if(!ok) 
        std::cerr << "corefine_and_compute_difference is not OK\n" ;
    else 
        std::cout<<"corefine_and_compute_difference is OK\n";

}

void get_components(Mesh& mesh, MESHES& components)
{
        std::vector<std::size_t> component_ids(mesh.number_of_faces());
        std::size_t num_comp = PMP::connected_components(
            mesh,
            boost::make_iterator_property_map(
                component_ids.begin(),
                get(
                    boost::face_index, 
                    mesh
                )
            )
        );

        components.resize(num_comp);
        PMP::split_connected_components(mesh, components);
}

void split_into_disjoint_meshes(Mesh& mesh, MESHES& components)
{
    components.clear();
    PMP::split_connected_components(mesh, components);
}

void extract_faces_as_mesh(const Mesh& mesh, const std::vector<Mesh::Face_index>& selected_face, Mesh& result)
{
    std::unordered_map<Mesh::Vertex_index, Mesh::Vertex_index> vmap;
    vmap.reserve(selected_face.size()*3);
    std::vector<Mesh::Vertex_index> new_face_vertices;
    for (auto f : selected_face)
    {
        new_face_vertices.clear();
        for (auto v : CGAL::vertices_around_face(mesh.halfedge(f), mesh))
        {
                // Copy vertex into new mesh
            if (vmap.find(v) == vmap.end())
                vmap[v] = result.add_vertex(mesh.point(v));
            new_face_vertices.push_back(vmap[v]);
        }
        result.add_face(new_face_vertices);
    }
}
void get_intersection_difference(Mesh& A, Mesh& B, Mesh& intersection, Mesh& difference)
{
    auto start = std::chrono::high_resolution_clock::now();

    std::vector<Mesh::Face_index> intersection_index;
    std::vector<Mesh::Face_index> difference_index;
    Mesh difference_mesh;

    Tree treeB(faces(B).first, faces(B).second, B);
    treeB.accelerate_distance_queries();

    std::cout<<"A\n";
    std::cout << "A mesh num faces = "<<A.number_of_faces() << std::endl;
    std::cout << "A mesh num verts = "<<A.number_of_vertices() << std::endl;

    std::cout<<"B\n";
    std::cout << "B mesh num faces = "<<B.number_of_faces() << std::endl;
    std::cout << "B mesh num verts = "<<B.number_of_vertices() << std::endl;

    std::cout << "\n d = " << treeB.squared_distance(Point(1.1, 2.0, 2.3))<< std::endl;

    bool is_face_on_mesh;
    double eps = 1e-8;
    // PMC inside(B);

    std::array<double,3> p;
    for(Mesh::Face_index f : A.faces()){
        is_face_on_mesh = true;
        p[0] = 0;p[1] = 0;p[2] = 0;
        for(auto v : CGAL::vertices_around_face(A.halfedge(f), A)) {
            // Point p = treeB.closest_point_and_primitive(A.point(v)).first;
            // double d = CGAL::to_double(CGAL::squared_distance(p, A.point(v)));
            p[0] += CGAL::to_double(A.point(v).x());
            p[1] += CGAL::to_double(A.point(v).y());
            p[2] += CGAL::to_double(A.point(v).z());
            // if(!inside(A.point(v)) == CGAL::ON_BOUNDARY)
        }

        if(treeB.squared_distance(Point(p[0]/3, p[1]/3, p[2]/3)) > eps)
        {
            // std::cout<<"differemce f = "<<f<<std::endl;
            is_face_on_mesh = false;
        }

        if(is_face_on_mesh)
            intersection_index.push_back(f);
        else
            difference_index.push_back(f);

    }

    // std::cout<<"intersection_index = \n\n";

    // for(auto i : intersection_index)
    //     std::cout << i <<" , ";

    std::cout<<"\n\n-----------------------------\n\n";
    // std::cout<<"difference_index = \n\n";
    // for(auto i : difference_index)
    //     std::cout << i <<" , ";


    extract_faces_as_mesh(A,intersection_index, intersection);
    extract_faces_as_mesh(A,difference_index, difference);

    // bool valid = PMP::corefine_and_compute_intersection(
    //                 A, B,
    //                 intersection_mesh);

    // if (!valid) 
    //     std::cerr << "Intersection failed\n";
    // else
    //     writeSTL(intersection_mesh,"intersection_mesh.stl");

    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    std::cout << "\nget_intersection_difference Execution time: " << duration.count() << " µs\n\n";
}

// Mesh get_difference( Mesh& A, Mesh& B)
// {
//     Mesh difference_mesh;
//     bool valid = PMP::corefine_and_compute_difference(
//                     A, B,
//                     difference_mesh);

//     if (!valid) 
//         std::cerr << "Difference failed\n";
//     else
//         writeSTL(difference_mesh,"difference_mesh.stl");

//     return difference_mesh;
// }


void self_difference_and_split(Mesh& original,MESHES& components)
{
    auto start = std::chrono::high_resolution_clock::now();
        Mesh mesh ;
        self_difference(original, mesh);
        // writeSTL(mesh,"self_difference.stl");
        split_into_disjoint_meshes(mesh, components);

    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    std::cout << "self_difference_and_split Execution time: " << duration.count() << " µs\n\n";
}


void self_difference_split_intersection_difference(
    Mesh& original,
    MESHES& components,
    MESHES& intersections,
    MESHES& differences){

    Mesh mesh ;
    auto start_total = std::chrono::high_resolution_clock::now();

    self_difference(original, mesh);
    // writeSTL(mesh,"self_difference.stl");
    auto start = std::chrono::high_resolution_clock::now();
        split_into_disjoint_meshes(mesh, components);
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    std::cout << "split_into_disjoint_meshes Execution time: " << duration.count() << " µs\n\n";

    Mesh intersection;
    Mesh difference;
    MESHES differences_split;    
    std::cout<<"num# of components = "<<components.size();

    for (auto& comp : components)
    {
        if(comp.number_of_vertices() == 0)
            continue;
        get_intersection_difference(comp,original,intersection,difference);
        intersections.push_back(intersection);
        differences.push_back(difference);
        get_components(difference, differences_split);
        std::cout<<"num# of differences_split = "<<differences_split.size();
        int i = 0, count = 0;

        for (auto& IO : differences_split)
            if(IO.number_of_vertices() > 0)
                count++;

        if(count >= 2)
            for (auto& IO : differences_split)
                if(IO.number_of_vertices() > 0)
                    differences.push_back(IO);
                // writeSTL(IO,"IO-" + std::to_string(i++) + ".stl");

        intersection.clear();
        difference.clear();
    }
    auto end_total = std::chrono::high_resolution_clock::now();
    auto duration_total = std::chrono::duration_cast<std::chrono::microseconds>(end_total - start_total);
    std::cout << "\ntotal Execution time: " << duration.count() << " µs\n\n";

        writeSTL(intersection,"intersection_mesh.stl");
        writeSTL(difference,"difference_mesh.stl");
}










