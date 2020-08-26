import unittest
import server

OK = 'OK\n'
FAIL = 'FAIL\n'
ERROR = 'ERROR\n'


class Test_ValidateMessage(unittest.TestCase):

    def setUp(self) -> None:
        self.indexer = server.PackageIndexer()

    def test_missing_mandatory_params(self):
        command, package, dependencies = self.indexer.validate_msg("INDEX|")
        self.assertEqual(ERROR, command)

    def test_missing_package_name(self):
        command, package, dependencies = self.indexer.validate_msg("INDEX||")
        self.assertEqual(ERROR, command)

    def test_invalid_package_name(self):
        command, package, dependencies = self.indexer.validate_msg("INDEX|ceylon,cloog|")
        self.assertEqual(ERROR, command)

    def test_invalid_command(self):
        command, package, dependencies = self.indexer.validate_msg("ERROR|ceylon|")
        self.assertEqual(ERROR, command)

    def test_none_dependencies(self):
        command, package, dependencies = self.indexer.validate_msg("ERROR|ceylon|")
        self.assertEqual(dependencies, None)

    def test_perfect_msg(self):
        command, package, dependencies = self.indexer.validate_msg("INDEX|cloog|gmp,isl,pkg-config")
        self.assertEqual(command, 'INDEX')
        self.assertEqual(package, 'cloog')
        self.assertEqual(dependencies, ['gmp', 'isl', 'pkg-config'])

class Test_Index(unittest.TestCase):
    def setUp(self) -> None:
        self.indexer = server.PackageIndexer()


    def test_index_with_not_indexed_dependencies(self):
        self.assertEqual(FAIL, self.indexer.index('foo',['bar']))

    def test_index_without_dependencies(self):
        self.assertEqual(OK,self.indexer.index('foo',None))
        self.assertEqual(self.indexer.INDEX['foo'], None)

    def test_index_with_indexed_dependencies(self):
        self.indexer.index('foo', None)
        self.assertEqual(OK, self.indexer.index('bar', ['foo']))

    def test_index_multiple_packages(self):
        packages = ['bar','foo','baz']
        for p in packages:
            self.assertEqual(OK,self.indexer.index(p,None))


class Test_Remove(unittest.TestCase):
    def setUp(self) -> None:
        self.indexer = server.PackageIndexer()

    def test_remove_not_indexed_package(self):
        self.assertEqual(OK, self.indexer.remove('foo'))

    def test_remove_package_not_a_dependency(self):
        self.indexer.index('foo',None)
        self.assertEqual(OK,self.indexer.remove('foo'))

    def test_remove_is_dependency(self):
        self.indexer.index('bar',None)
        self.indexer.index('foo',['bar'])
        self.assertEqual(FAIL, self.indexer.remove('bar'))

    def test_dependency_loop(self):
        self.indexer.index('foo', None)
        self.indexer.index('bar', ['foo'])
        self.indexer.index('baz', ['bar'])
        self.assertEqual(FAIL, self.indexer.remove('bar'))

    def test_remove_dependency_loop_with_correct_order(self):
        self.indexer.index('foo', None)
        self.indexer.index('bar', ['foo'])
        self.indexer.index('baz', ['bar'])
        self.assertEqual(OK, self.indexer.remove('baz'))
        self.assertEqual(OK, self.indexer.remove('bar'))
        self.assertEqual(OK, self.indexer.remove('foo'))

class Test_Query(unittest.TestCase):
    def setUp(self) -> None:
        self.indexer = server.PackageIndexer()

    def test_query_non_existing_package(self):
        self.assertEqual(FAIL, self.indexer.query('foo'))

    def test_query_existing_package(self):
        self.indexer.index('foo',None)
        self.indexer.index('bar',['foo'])
        self.assertEqual(OK, self.indexer.query('foo'))
        self.assertEqual(OK, self.indexer.query('bar'))

if __name__ == '__main__':
    unittest.main()
