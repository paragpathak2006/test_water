using VERTS = std::vector<std::array<double,3>>;
using FACES = std::vector<std::array<int,3>>;
using SIZES = std::vector<int>;

using VMESHES = std::vector<Mesh>;

using PYVERTS = py::array_t<double>;
using PYFACES = py::array_t<int>;
using PYINTS = py::array_t<int>;

void reserve_space(Mesh& mesh, VERTS& vertices, FACES& faces);
void extract_mesh(const Mesh& mesh,VERTS& vertices,FACES& faces);
void reserve_space(Mesh& mesh, VERTS& vertices, FACES& faces);
void get_vertices_and_faces(Mesh& mesh, VERTS& vertices, FACES& faces, SIZES& num_of_vertices, SIZES& num_of_faces);
void numpy_to_mesh(PYVERTS &V, PYFACES &F, Mesh& mesh);

py::tuple mesh_to_numpy(Mesh& mesh);
py::tuple mesh_to_numpy(const VERTS& verts,const FACES& faces,const SIZES& num_of_vertices,const SIZES& num_of_faces);
py::tuple mesh_to_numpy(VMESHES& components);
py::tuple mesh_to_numpy(VMESHES& components,VMESHES& intersections,VMESHES& differences);
    
py::array_t<int> vector_to_numpy(const std::vector<int>& vec)
{
    return py::array_t<int>(vec.size(), vec.data());
}

void reserve_space(Mesh& mesh, VERTS& vertices, FACES& faces)
{
    vertices.reserve(mesh.number_of_vertices());
    faces.reserve(mesh.number_of_faces());
}

void extract_mesh(
    const Mesh& mesh,
    VERTS& vertices,
    FACES& faces)
{
    // -------------------------
    // 1. Extract Vertices
    // -------------------------
    std::unordered_map<Mesh::Vertex_index, int> index_map;
    index_map.reserve(mesh.number_of_vertices());

    int idx = 0;
    std::array<double,3> point;
    for (auto v : mesh.vertices())
    {
        auto& p = mesh.point(v);

        point[0] = CGAL::to_double(p.x()); 
        point[1] = CGAL::to_double(p.y());  
        point[2] = CGAL::to_double(p.z());

        vertices.push_back(point);
        index_map[v] = idx++;
    }

    // -------------------------
    // 2. Extract Faces
    // -------------------------
    for (auto f : mesh.faces())
    {
        std::array<int,3> face_indices;
        int j = 0;

        for (auto v : CGAL::vertices_around_face(mesh.halfedge(f), mesh))
            face_indices[j++] = index_map[v];

        if (j == 3)  // triangle mesh
            faces.push_back(face_indices);
    }
}


void get_vertices_and_faces(Mesh& mesh,
    VERTS& vertices, FACES& faces, 
    SIZES& num_of_vertices, SIZES& num_of_faces)
{
    reserve_space(mesh, vertices, faces);
    extract_mesh(mesh, vertices, faces);
    num_of_vertices.push_back(mesh.number_of_vertices());
    num_of_faces.push_back(mesh.number_of_faces());
}

void get_vertices_and_faces(VMESHES& components, 
    VERTS& vertices, FACES& faces, 
    SIZES& num_of_vertices, SIZES& num_of_faces)
{
        for (auto& comp : components) {
            extract_mesh(comp, vertices, faces);
            num_of_vertices.push_back(comp.number_of_vertices());
            num_of_faces.push_back(comp.number_of_faces());
        }
}


void numpy_to_mesh(PYVERTS &V,
                   PYFACES &F,
                   Mesh& mesh)
{
    auto v = V.unchecked<2>();
    auto f = F.unchecked<2>();

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

}

py::tuple mesh_to_numpy(
    const VERTS& verts,
    const FACES& faces,
    const SIZES& num_of_vertices,
    const SIZES& num_of_faces)
{
    PYVERTS V(
        std::vector<py::ssize_t>{
            static_cast<py::ssize_t>(verts.size()),
            3
        }
    );

    PYFACES F(
        std::vector<py::ssize_t>{
            static_cast<py::ssize_t>(faces.size()),
            3
        }
    );

    PYINTS num_vertices = vector_to_numpy(num_of_vertices);
    PYINTS num_faces = vector_to_numpy(num_of_vertices);

    auto Vbuf = V.mutable_unchecked<2>();
    auto Fbuf = F.mutable_unchecked<2>();
    auto num_vertices_buf = num_vertices.mutable_unchecked<1>();
    auto num_faces_buf = num_faces.mutable_unchecked<1>();

    for (size_t i = 0; i < num_of_vertices.size(); ++i)
    {
        num_vertices_buf(i) = num_of_vertices[i];
        num_faces_buf(i) = num_of_faces[i];
    }

    for (size_t i = 0; i < verts.size(); ++i)
    {
        Vbuf(i,0) = verts[i][0];
        Vbuf(i,1) = verts[i][1];
        Vbuf(i,2) = verts[i][2];
    }

    for (size_t i = 0; i < faces.size(); ++i)
    {
        Fbuf(i,0) = faces[i][0];
        Fbuf(i,1) = faces[i][1];
        Fbuf(i,2) = faces[i][2];
    }

    return py::make_tuple(V, F, num_vertices, num_faces);
}


py::tuple mesh_to_numpy(Mesh& mesh)
{
    VERTS vertices;
    FACES faces;
    SIZES num_of_vertices;
    SIZES num_of_faces;
    get_vertices_and_faces(mesh, vertices, faces, num_of_vertices, num_of_faces);
    return mesh_to_numpy(vertices, faces, num_of_vertices, num_of_faces);
}


py::tuple mesh_to_numpy(VMESHES& components)
{
    VERTS vertices;
    FACES faces;
    SIZES num_of_vertices;
    SIZES num_of_faces;

    get_vertices_and_faces(components, vertices, faces, num_of_vertices, num_of_faces);

    return mesh_to_numpy(vertices, faces, num_of_vertices, num_of_faces);
}


py::tuple mesh_to_numpy(
    VMESHES& components,
    VMESHES& intersections,
    VMESHES& differences)
{
    VERTS vertices;
    FACES faces;
    SIZES num_of_vertices;
    SIZES num_of_faces;

    get_vertices_and_faces(components, vertices, faces, num_of_vertices, num_of_faces);
    get_vertices_and_faces(intersections, vertices, faces, num_of_vertices, num_of_faces);
    get_vertices_and_faces(differences, vertices, faces, num_of_vertices, num_of_faces);

    return mesh_to_numpy(vertices, faces, num_of_vertices, num_of_faces);
}
