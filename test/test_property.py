import unittest

from odml import Property, Section, Document, DType
from odml.property import BaseProperty
from odml.section import BaseSection


class TestProperty(unittest.TestCase):

    def setUp(self):
        pass

    def test_simple_attributes(self):
        p_name = "propertyName"
        p_origin = "from over there"
        p_unit = "pears"
        p_uncertainty = "+-12"
        p_ref = "4 8 15 16 23"
        p_def = "an odml test property"
        p_dep = "yes"
        p_dep_val = "42"

        prop = Property(name=p_name, value_origin=p_origin, unit=p_unit,
                        uncertainty=p_uncertainty, reference=p_ref, definition=p_def,
                        dependency=p_dep, dependency_value=p_dep_val)

        self.assertEqual(prop.name, p_name)
        self.assertEqual(prop.value_origin, p_origin)
        self.assertEqual(prop.unit, p_unit)
        self.assertEqual(prop.uncertainty, p_uncertainty)
        self.assertEqual(prop.reference, p_ref)
        self.assertEqual(prop.definition, p_def)
        self.assertEqual(prop.dependency, p_dep)
        self.assertEqual(prop.dependency_value, p_dep_val)

        # Test setting attributes
        prop.name = "%s_edit" % p_name
        self.assertEqual(prop.name, "%s_edit" % p_name)
        prop.value_origin = "%s_edit" % p_origin
        self.assertEqual(prop.value_origin, "%s_edit" % p_origin)
        prop.unit = "%s_edit" % p_unit
        self.assertEqual(prop.unit, "%s_edit" % p_unit)
        prop.uncertainty = "%s_edit" % p_uncertainty
        self.assertEqual(prop.uncertainty, "%s_edit" % p_uncertainty)
        prop.reference = "%s_edit" % p_ref
        self.assertEqual(prop.reference, "%s_edit" % p_ref)
        prop.definition = "%s_edit" % p_def
        self.assertEqual(prop.definition, "%s_edit" % p_def)
        prop.dependency = "%s_edit" % p_dep
        self.assertEqual(prop.dependency, "%s_edit" % p_dep)
        prop.dependency_value = "%s_edit" % p_dep_val
        self.assertEqual(prop.dependency_value, "%s_edit" % p_dep_val)

        # Test setting attributes to None when '' is passed.
        prop.value_origin = ""
        self.assertIsNone(prop.value_origin)
        prop.unit = ""
        self.assertIsNone(prop.unit)
        prop.uncertainty = ""
        self.assertIsNone(prop.uncertainty)
        prop.reference = ""
        self.assertIsNone(prop.reference)
        prop.definition = ""
        self.assertIsNone(prop.definition)
        prop.dependency = ""
        self.assertIsNone(prop.dependency)
        prop.dependency_value = ""
        self.assertIsNone(prop.dependency_value)

    def test_value(self):
        p = Property("property", 100)
        self.assertEqual(p.value[0], 100)
        self.assertEqual(type(p.value), list)

        p.append(10)
        self.assertEqual(len(p), 2)
        self.assertRaises(ValueError, p.append, [1, 2, 3])

        p.extend([20, 30, '40'])
        self.assertEqual(len(p), 5)
        with self.assertRaises(ValueError):
            p.append('invalid')
        with self.assertRaises(ValueError):
            p.extend(('5', 6, 7))

        p2 = Property("property 2", 3)
        self.assertRaises(ValueError, p.append, p2)
        p.extend(p2)
        self.assertEqual(len(p), 6)

        p.value = None
        self.assertEqual(len(p), 0)

        p.value = [1, 2, 3]
        p.value = ""
        self.assertEqual(len(p), 0)

        p.value = [1, 2, 3]
        p.value = []
        self.assertEqual(len(p), 0)

        p.value = [1, 2, 3]
        p.value = ()
        self.assertEqual(len(p), 0)

        p3 = Property("test", value=2, unit="Hz")
        p4 = Property("test", value=5.5, unit="s")

        with self.assertRaises(ValueError):
            p3.append(p4)

        p.value.append(5)
        self.assertEqual(len(p.value), 0)
        self.assertRaises(ValueError, p.append, 5.5)

        p.append(5.5, strict=False)
        self.assertEqual(len(p), 1)

        self.assertRaises(ValueError, p.extend, [3.14, 6.28])
        p.extend([3.14, 6.28], strict=False)
        self.assertEqual(len(p), 3)

        p5 = Property("test", value="a string")
        p5.append("Freude")
        self.assertEqual(len(p5), 2)
        self.assertRaises(ValueError, p5.append, "[a, b, c]")
        p5.extend("[a, b, c]")
        self.assertEqual(len(p5), 5)

        p6 = Property("test", {"name": "Marie", "name": "Johanna"})
        self.assertEqual(len(p6), 1)

        # Test tuple dtype value.
        t = Property(name="Location", value='(39.12; 67.19)', dtype='2-tuple')
        tuple_value = t.value[0]  # As the formed tuple is a list of list
        self.assertEqual(tuple_value[0], '39.12')
        self.assertEqual(tuple_value[1], '67.19')

        # Test invalid tuple length
        with self.assertRaises(ValueError):
            _ = Property(name="Public-Key", value='(5689; 1254; 687)', dtype='2-tuple')

    def test_get_set_value(self):
        values = [1, 2, 3, 4, 5]
        p = Property("property", value=values)

        self.assertEqual(len(p), 5)
        for s, d in zip(values, p.value):
            self.assertEqual(s, d)

        count = 0
        for v in p:
            count += 1
        self.assertEqual(count, len(values))

        p[0] = 10
        self.assertEqual(p[0], 10)
        with self.assertRaises(ValueError):
            p[1] = 'stringval'

    def test_bool_conversion(self):
        # Success tests
        p = Property(name='received', value=[1, 0, 1, 0, 1])
        assert(p.dtype == 'int')
        p.dtype = DType.boolean
        assert(p.dtype == 'boolean')
        assert(p.value == [True, False, True, False, True])

        q = Property(name='sent', value=['False', True, 'TRUE', '0', 't', 'F', '1'])
        assert(q.dtype == 'string')
        q.dtype = DType.boolean
        assert(q.dtype == 'boolean')
        assert(q.value == [False, True, True, False, True, False, True])

        # Failure tests
        curr_val = [3, 0, 1, 0, 8]
        curr_type = 'int'
        p = Property(name='received', value=curr_val)
        assert(p.dtype == curr_type)
        with self.assertRaises(ValueError):
            p.dtype = DType.boolean
        assert(p.dtype == curr_type)
        assert(p.value == curr_val)

        curr_type = 'string'
        q = Property(name='sent', value=['False', True, 'TRUE', '0', 't', '12', 'Ft'])
        assert(q.dtype == curr_type)
        with self.assertRaises(ValueError):
            q.dtype = DType.boolean
        assert(q.dtype == curr_type)

    def test_str_to_int_convert(self):
        # Success Test
        p = Property(name='cats_onboard', value=['3', '0', '1', '0', '8'])
        assert(p.dtype == 'string')
        p.dtype = DType.int
        assert(p.dtype == 'int')
        assert(p.value == [3, 0, 1, 0, 8])

        # Failure Test
        p = Property(name='dogs_onboard', value=['7', '20', '1 Dog', 'Seven'])
        assert(p.dtype == 'string')

        with self.assertRaises(ValueError):
            p.dtype = DType.int

        assert(p.dtype == 'string')
        assert(p.value == ['7', '20', '1 Dog', 'Seven'])

    def test_parent(self):
        p = Property("property_section", parent=Section("S"))
        self.assertIsInstance(p.parent, BaseSection)
        self.assertEqual(len(p.parent._props), 1)

        """ Test if child is removed from _props of a parent after assigning
            a new parent to the child """
        prop_parent = p.parent
        p.parent = Section("S1")
        self.assertEqual(len(prop_parent._props), 0)
        self.assertIsInstance(p.parent, BaseSection)
        self.assertIsInstance(p.parent._props[0], BaseProperty)

        prop_parent = p.parent
        p.parent = None
        self.assertIsNone(p.parent)
        self.assertEqual(len(prop_parent._props), 0)

        with self.assertRaises(ValueError):
            Property("property_prop", parent=Property("P"))
        with self.assertRaises(ValueError):
            Property("property_doc", parent=Document())

    def test_dtype(self):
        prop = Property(name="prop")

        # Test assignment of all supported dtypes.
        for curr_type in DType:
            prop.dtype = curr_type
            self.assertEqual(prop.dtype, curr_type)

        # Test assignment of dtype alias.
        prop.dtype = "bool"
        self.assertEqual(prop.dtype, "bool")
        prop.dtype = "str"
        self.assertEqual(prop.dtype, "str")

        # Test assignment of tuple.
        prop.dtype = "2-tuple"
        self.assertEqual(prop.dtype, "2-tuple")

        # Test set None
        prop.dtype = None
        self.assertIsNone(prop.dtype)

        # Test assignment fails.
        with self.assertRaises(AttributeError):
            prop.dtype = 1
        with self.assertRaises(AttributeError):
            prop.dtype = "crash and burn"
        with self.assertRaises(AttributeError):
            prop.dtype = "x-tuple"

    def test_get_path(self):
        doc = Document()
        sec = Section(name="parent", parent=doc)

        # Check root path for a detached Property.
        prop = Property(name="prop")
        self.assertEqual("/", prop.get_path())

        # Check absolute path of Property in a Document.
        prop.parent = sec
        self.assertEqual("/%s:%s" % (sec.name, prop.name), prop.get_path())

    def test_id(self):
        p = Property(name="P")
        self.assertIsNotNone(p.id)

        p = Property("P", id="79b613eb-a256-46bf-84f6-207df465b8f7")
        self.assertEqual(p.id, "79b613eb-a256-46bf-84f6-207df465b8f7")

        p = Property("P", id="id")
        self.assertNotEqual(p.id, "id")

        # Make sure id cannot be reset programmatically.
        with self.assertRaises(AttributeError):
            p.id = "someId"

    def test_new_id(self):
        prop = Property(name="prop")
        old_id = prop.id

        # Test assign new generated id.
        prop.new_id()
        self.assertNotEqual(old_id, prop.id)

        # Test assign new custom id.
        old_id = prop.id
        prop.new_id("79b613eb-a256-46bf-84f6-207df465b8f7")
        self.assertNotEqual(old_id, prop.id)
        self.assertEqual("79b613eb-a256-46bf-84f6-207df465b8f7", prop.id)

        # Test invalid custom id exception.
        with self.assertRaises(ValueError):
            prop.new_id("crash and burn")

    def test_merge(self):
        p_dst = Property("p1", value=[1, 2, 3], unit="Hz", definition="Freude\t schoener\nGoetterfunken\n",
                         reference="portal.g-node.org", uncertainty=0.0)
        p_src = Property("p2", value=[2, 4, 6], unit="Hz", definition="FREUDE schoener GOETTERfunken")

        test_p = p_dst.clone()
        test_p.merge(p_src)
        self.assertEqual(len(test_p.value), 5)

        p_inv_unit = p_src.clone()
        p_inv_unit.unit = 's'

        p_inv_def = p_src.clone()
        p_inv_def.definition = "Freunde schoender Goetterfunken"

        p_inv_uncert = p_src.clone()
        p_inv_uncert.uncertainty = 10.0

        p_inv_ref = p_src.clone()
        p_inv_ref.reference = "test"

        test_p = p_dst.clone()
        self.assertRaises(ValueError, test_p.merge, p_inv_unit)
        self.assertRaises(ValueError, test_p.merge, p_inv_def)
        self.assertRaises(ValueError, test_p.merge, p_inv_uncert)
        self.assertRaises(ValueError, test_p.merge, p_inv_ref)

        test_p.reference = None
        test_p.merge(p_src)
        self.assertEqual(test_p.reference, p_src.reference)

        test_p.unit = ""
        test_p.merge(p_src)
        self.assertEqual(test_p.unit, p_src.unit)

        test_p.uncertainty = None
        test_p.merge(p_src)
        self.assertEqual(test_p.uncertainty, p_src.uncertainty)

        test_p.definition = ""
        test_p.merge(p_src)
        self.assertEqual(test_p.definition, p_src.definition)

        double_p = Property("adouble", value=3.14)
        int_p = Property("aint", value=3)
        self.assertRaises(ValueError, double_p.merge, int_p)

        int_p.merge(double_p, strict=False)
        self.assertEqual(len(int_p), 2)

    def test_clone(self):
        sec = Section(name="parent")

        # Check different id.
        prop = Property(name="original")
        clone_prop = prop.clone()
        self.assertNotEqual(prop.id, clone_prop.id)

        # Check parent removal in clone.
        prop.parent = sec
        clone_prop = prop.clone()
        self.assertIsNotNone(prop.parent)
        self.assertIsNone(clone_prop.parent)

    def test_get_merged_equivalent(self):
        sec = Section(name="parent")
        mersec = Section(name="merged_section")
        merprop_other = Property(name="other_prop", value="other")
        merprop = Property(name="prop", value=[1, 2, 3])

        # Check None on unset parent.
        prop = Property(name="prop")
        self.assertIsNone(prop.get_merged_equivalent())

        # Check None on parent without merged Section.
        prop.parent = sec
        self.assertIsNone(prop.get_merged_equivalent())

        # Check None on parent with merged Section but no attached Property.
        sec.merge(mersec)
        self.assertIsNone(prop.get_merged_equivalent())

        # Check None on parent with merged Section and unequal Property.
        merprop_other.parent = mersec
        self.assertIsNone(prop.get_merged_equivalent())

        # Check receiving merged equivalent Property.
        merprop.parent = mersec
        self.assertIsNotNone(prop.get_merged_equivalent())
        self.assertEqual(prop.get_merged_equivalent(), merprop)


if __name__ == "__main__":
    print("TestProperty")
    tp = TestProperty()
    tp.test_value()
    tp.test_merge()
