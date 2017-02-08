#include <boost/python.hpp>
#include <ome/files/in/OMETIFFReader.h>

using namespace boost::python;

BOOST_PYTHON_MODULE(omefiles) {
  // TODO: expose constructor
  class_<ome::files::in::OMETIFFReader>("OMETIFFReader")
    .def("set_id", &ome::files::in::OMETIFFReader::setId)
    .def("get_image_count", &ome::files::in::OMETIFFReader::getImageCount);
}
