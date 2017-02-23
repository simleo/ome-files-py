#include <boost/python.hpp>
#include <ome/files/in/OMETIFFReader.h>

using namespace boost::python;

struct OMETIFFReaderWrapper : ome::files::in::OMETIFFReader {
  void setIdStr(std::string filename) {
    setId(filename);
  }
};

BOOST_PYTHON_MODULE(ome_files) {
  class_<OMETIFFReaderWrapper, boost::noncopyable>("OMETIFFReader")
    .def("set_id", &OMETIFFReaderWrapper::setIdStr)
    .def("get_image_count", &OMETIFFReaderWrapper::getImageCount)
    .def("close", &OMETIFFReaderWrapper::close);
}
