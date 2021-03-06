"""
This file tests proper creation, saving and loading
of odML Documents with all supported odML parsers.
"""

import os
import shutil
import tempfile
import unittest

import odml


class TestDocumentIntegration(unittest.TestCase):

    def setUp(self):
        # Set up test environment
        self.tmp_dir = tempfile.mkdtemp(suffix=".odml")

        self.json_file = os.path.join(self.tmp_dir, "test.json")
        self.xml_file = os.path.join(self.tmp_dir, "test.xml")
        self.yaml_file = os.path.join(self.tmp_dir, "test.yaml")

        # Set up odML document stub
        doc = odml.Document()
        self.doc = doc

    def tearDown(self):
        if os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)

    def save_load(self):
        """
        Helper method to save and load the current state of the document
        with all supported parsers.
        :return: jdoc ... document loaded from JSON file
                 xdoc ... document loaded from XML file
                 ydoc ... document loaded from YAML file
        """
        odml.save(self.doc, self.json_file, "JSON")
        jdoc = odml.load(self.json_file, "JSON")

        odml.save(self.doc, self.xml_file)
        xdoc = odml.load(self.xml_file)

        odml.save(self.doc, self.yaml_file, "YAML")
        ydoc = odml.load(self.yaml_file, "YAML")

        return jdoc, xdoc, ydoc

    def test_id(self):
        """
        This test checks the correct writing and loading of
        autogenerated and assigned document id.
        """
        # Test correct save and load of generated id.
        jdoc, xdoc, ydoc = self.save_load()

        self.assertEqual(jdoc.id, self.doc.id)
        self.assertEqual(xdoc.id, self.doc.id)
        self.assertEqual(ydoc.id, self.doc.id)

        # Test correct save and load of assigned id.
        assigned_id = "79b613eb-a256-46bf-84f6-207df465b8f7"
        self.doc = odml.Document(oid=assigned_id)
        jdoc, xdoc, ydoc = self.save_load()

        self.assertEqual(jdoc.id, assigned_id)
        self.assertEqual(xdoc.id, assigned_id)
        self.assertEqual(ydoc.id, assigned_id)

    def test_simple_attributes(self):
        """
        This test checks correct writing and loading of 'simple'
        Document format attributes.
        """
        author = "HPL"
        version = "ver64"
        date = "1890-08-20"
        repository = "invalid"

        self.doc = odml.Document(author, date, version, repository)
        jdoc, xdoc, ydoc = self.save_load()

        # Test correct JSON save and load.
        self.assertEqual(jdoc.author, author)
        self.assertEqual(jdoc.version, version)
        self.assertEqual(str(jdoc.date), date)
        self.assertEqual(jdoc.repository, repository)

        # Test correct XML save and load.
        self.assertEqual(xdoc.author, author)
        self.assertEqual(xdoc.version, version)
        self.assertEqual(str(xdoc.date), date)
        self.assertEqual(xdoc.repository, repository)

        # Test correct YAML save and load.
        self.assertEqual(ydoc.author, author)
        self.assertEqual(ydoc.version, version)
        self.assertEqual(str(ydoc.date), date)
        self.assertEqual(ydoc.repository, repository)

    def test_children(self):
        """
        This test checks the correct saving and loading of Section children of a Document.
        """
        s_type = "type"
        # Lvl 1 child Sections
        sec_lvl_11 = odml.Section(name="sec_11", type=s_type, parent=self.doc)
        _ = odml.Section(name="sec_12", type=s_type, parent=self.doc)

        # Lvl 2 child Sections
        sec_lvl_21 = odml.Section(name="sec_21", type=s_type, parent=sec_lvl_11)
        _ = odml.Section(name="sec_22", type=s_type, parent=sec_lvl_11)
        _ = odml.Section(name="sec_23", type=s_type, parent=sec_lvl_11)

        # Lvl 2 child Properties
        _ = odml.Property(name="prop_21", parent=sec_lvl_11)
        _ = odml.Property(name="prop_22", parent=sec_lvl_11)
        _ = odml.Property(name="prop_23", parent=sec_lvl_11)

        # Lvl 3 child Sections
        _ = odml.Section(name="sec_31", type=s_type, parent=sec_lvl_21)
        _ = odml.Section(name="sec_32", type=s_type, parent=sec_lvl_21)
        _ = odml.Section(name="sec_33", type=s_type, parent=sec_lvl_21)
        _ = odml.Section(name="sec_34", type=s_type, parent=sec_lvl_21)

        # Lvl 3 child Properties
        _ = odml.Property(name="prop_31", parent=sec_lvl_21)
        _ = odml.Property(name="prop_32", parent=sec_lvl_21)
        _ = odml.Property(name="prop_33", parent=sec_lvl_21)
        _ = odml.Property(name="prop_34", parent=sec_lvl_21)

        jdoc, xdoc, ydoc = self.save_load()

        # Test correct JSON save and load.
        self.assertEqual(len(jdoc.sections), 2)

        jsec_lvl_1 = jdoc[sec_lvl_11.name]
        self.assertEqual(len(jsec_lvl_1.sections), 3)
        self.assertEqual(len(jsec_lvl_1.properties), 3)

        jsec_lvl_2 = jsec_lvl_1[sec_lvl_21.name]
        self.assertEqual(len(jsec_lvl_2.sections), 4)
        self.assertEqual(len(jsec_lvl_2.properties), 4)

        # Test correct XML save and load.
        self.assertEqual(len(xdoc.sections), 2)

        xsec_lvl_1 = xdoc[sec_lvl_11.name]
        self.assertEqual(len(xsec_lvl_1.sections), 3)
        self.assertEqual(len(xsec_lvl_1.properties), 3)

        xsec_lvl_2 = xsec_lvl_1[sec_lvl_21.name]
        self.assertEqual(len(xsec_lvl_2.sections), 4)
        self.assertEqual(len(xsec_lvl_2.properties), 4)

        # Test correct YAML save and load.
        self.assertEqual(len(ydoc.sections), 2)

        ysec_lvl_1 = ydoc[sec_lvl_11.name]
        self.assertEqual(len(ysec_lvl_1.sections), 3)
        self.assertEqual(len(ysec_lvl_1.properties), 3)

        ysec_lvl_2 = ysec_lvl_1[sec_lvl_21.name]
        self.assertEqual(len(ysec_lvl_2.sections), 4)
        self.assertEqual(len(ysec_lvl_2.properties), 4)
