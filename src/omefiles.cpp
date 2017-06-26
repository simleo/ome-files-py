#include <pybind11/pybind11.h>
#include <string>
#include <ome/files/in/OMETIFFReader.h>

namespace py = pybind11;

PYBIND11_PLUGIN(ome_files) {
  py::module m("ome_files");
  py::class_<ome::files::in::OMETIFFReader>(m, "OMETIFFReader")
    .def(py::init<>())
    .def("set_id", [](ome::files::in::OMETIFFReader &r, std::string id) {
	r.setId(id);
      })
    .def("get_image_count", [](ome::files::in::OMETIFFReader &r) {
	return r.getImageCount();
      })
    .def("close", &ome::files::in::OMETIFFReader::close);
  return m.ptr();
}
