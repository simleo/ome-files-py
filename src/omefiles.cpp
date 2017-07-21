#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <string>
#include <ome/files/in/OMETIFFReader.h>

namespace py = pybind11;
using ome::files::in::OMETIFFReader;

PYBIND11_PLUGIN(ome_files) {
  py::module m("ome_files");
  py::class_<OMETIFFReader>(m, "OMETIFFReader")
    .def(py::init<>())
    .def("set_id", [](OMETIFFReader &r, std::string id) {
	r.setId(id);
      }, "Set the current file name.")
    .def("set_series", [](OMETIFFReader &r, size_t series) {
        r.setSeries(series);
      }, "Set the active series.")
    .def("get_series", [](OMETIFFReader &r) {
        return r.getSeries();
      }, "Get the active series.")
    .def("get_image_count", [](OMETIFFReader &r) {
	return r.getImageCount();
      }, "Get the number of image planes in the current series.")
    .def("get_series_count", [](OMETIFFReader &r) {
        return r.getSeriesCount();
      }, "Get the number of image series.")
    .def("get_size_x", [](OMETIFFReader &r) {
	return r.getSizeX();
      }, "Get the size of the X dimension.")
    .def("get_size_y", [](OMETIFFReader &r) {
        return r.getSizeY();
      }, "Get the size of the Y dimension.")
    .def("get_size_z", [](OMETIFFReader &r) {
        return r.getSizeZ();
      }, "Get the size of the Z dimension.")
    .def("get_size_t", [](OMETIFFReader &r) {
        return r.getSizeT();
      }, "Get the size of the T dimension.")
    .def("get_size_c", [](OMETIFFReader &r) {
        return r.getSizeC();
      }, "Get the size of the C dimension.")
    .def("get_dimension_order", [](OMETIFFReader &r) {
        return r.getDimensionOrder();
      }, "Get a five-character string representing the order in which "
      "planes will be returned.")
    .def("get_index", [](OMETIFFReader &r, size_t z, size_t c, size_t t) {
	return r.getIndex(z, c, t);
      }, "Get the plane index corresponding to the given ZCT coordinates.")
    .def("get_zct_coords", [](OMETIFFReader &r, size_t index) {
	return r.getZCTCoords(index);
      }, "Get the ZCT coordinates for the given plane index.")
    .def("get_rgb_channel_count", [](OMETIFFReader &r, size_t channel) {
	return r.getRGBChannelCount(channel);
      }, "Get the number of sub-channels for the given channel.")
    .def("close", &OMETIFFReader::close, "Close the currently open file. "
	 "If file_only is False, also reset all internal state",
	 py::arg("file_only") = false);
  return m.ptr();
}
