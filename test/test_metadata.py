# #%L
# OME-FILES Python library for image IO.
# Copyright (c) 2017 University of Dundee
# %%
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# #L%

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

import ome_files.metadata as ofmd


@pytest.fixture(scope='class',
                params=["""\
<?xml version="1.0" encoding="UTF-8"?>
<OME xmlns="http://www.openmicroscopy.org/Schemas/OME/2016-06"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns:OME="http://www.openmicroscopy.org/Schemas/OME/2016-06"
  xsi:schemaLocation="http://www.openmicroscopy.org/Schemas/OME/2016-06
  http://www.openmicroscopy.org/Schemas/OME/2016-06/ome.xsd">
  <StructuredAnnotations>
    <MapAnnotation ID="Annotation:0" Annotator="A0" Namespace="N0">
      <Description>D0</Description>
      <AnnotationRef ID="Annotation:10"/>
      <AnnotationRef ID="Annotation:20"/>
      <Value>
        <M K="K00">V00.0</M>
        <M K="K00">V00.1</M>
        <M K="K01">V01.0</M>
      </Value>
    </MapAnnotation>
    <MapAnnotation ID="Annotation:1" Annotator="A1" Namespace="N1">
      <Description>D1</Description>
      <AnnotationRef ID="Annotation:11"/>
      <AnnotationRef ID="Annotation:21"/>
      <Value>
        <M K="K10">V10.0</M>
        <M K="K10">V10.1</M>
        <M K="K11">V11.0</M>
      </Value>
    </MapAnnotation>
    <XMLAnnotation ID="Annotation:2" Annotator="A2" Namespace="N2">
      <Description>D2</Description>
      <AnnotationRef ID="Annotation:12"/>
      <AnnotationRef ID="Annotation:22"/>
      <Value>
        <This Foo="Bar"/>
        <Can/>
        <Be>Anything</Be>
      </Value>
    </XMLAnnotation>
  </StructuredAnnotations>
</OME>
"""])
def metadata_testcases(request):
    request.cls.xml = request.param
    request.cls.meta = ofmd.OMEXMLMetadata(request.param)
    yield


@pytest.mark.usefixtures('metadata_testcases')
class TestOMEXMLMetadata(object):

    def __by_id(self, annotations):
        return dict((_.ID.split(":")[1], _) for _ in annotations)

    def __check_annotation(self, ann, id):
        assert ann.Annotator == "A%s" % id
        assert ann.Namespace == "N%s" % id
        assert ann.Description == "D%s" % id
        assert ann.AnnotationRef == [
            "Annotation:1%s" % id, "Annotation:2%s" % id
        ]

    def test_map_annotations(self):
        annotations = self.meta.get_map_annotations()
        assert len(annotations) == 2
        for id, ann in self.__by_id(annotations).items():
            self.__check_annotation(ann, id)
            assert ann.Value == {
                "K%s0" % id: ["V%s0.0" % id, "V%s0.1" % id],
                "K%s1" % id: ["V%s1.0" % id],
            }

    def test_xml_annotations(self):
        annotations = self.meta.get_xml_annotations()
        assert len(annotations) == 1
        for id, ann in self.__by_id(annotations).items():
            self.__check_annotation(ann, id)
        children = ofmd.get_children(ann.Value)
        assert len(set(_.nodeName for _ in children).symmetric_difference(
                         set(("This", "Can", "Be")))) == 0

    def test_unicode(self):
        nonascii = "\N{CYRILLIC CAPITAL LETTER O WITH DIAERESIS}"
        try:
            meta = ofmd.OMEXMLMetadata(self.xml.replace("D0", nonascii))
        except UnicodeEncodeError:
            self.fail("Cannot construct OMEXMLMetadata from xml string")
        by_id = self.__by_id(meta.get_map_annotations())
        assert by_id["0"].Description == nonascii
