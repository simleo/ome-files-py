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
      }, "Set the current file name.")
    .def("get_image_count", [](ome::files::in::OMETIFFReader &r) {
	return r.getImageCount();
      }, "Get the number of image planes in the current series.")
    .def("close", &ome::files::in::OMETIFFReader::close,
	 "Close the currently open file. "
	 "If file_only is False, also reset all internal state",
	 py::arg("file_only") = false);
  return m.ptr();
}
