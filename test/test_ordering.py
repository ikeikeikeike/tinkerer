'''
    Test Ordering
    ~~~~~~~~~~~~~

    Tests that Tinkerer adds posts and pages in the correct order

    :copyright: Copyright 2011 by Vlad Riscutia
'''
import datetime
import unittest
import utils
import tinkerer.cmdline


# test case
class TestOrdering(utils.BaseTinkererTest):
    def test_ordering(self):
        utils.test = self

        # create some pages and posts 
        tinkerer.cmdline.page("First Page")
        tinkerer.cmdline.page("Second Page")
        tinkerer.cmdline.post("Oldest Post", datetime.date(2010, 10, 1))
        tinkerer.cmdline.post("Newer Post", datetime.date(2010, 11, 2))
        tinkerer.cmdline.post("Newest Post", datetime.date(2010, 12, 3))

        utils.hook_extension("test_ordering")
        self.build()


# test ordering through extension
def build_finished(app, exception):
    # check post and pages have the correct relations
    relations = app.builder.env.collect_relations()

    utils.test.assertEquals(relations["index"], 
                            [None, None, "2010/12/03/newest_post"])
    utils.test.assertEquals(relations["2010/12/03/newest_post"], 
                               ["index", "index", "2010/11/02/newer_post"])
    utils.test.assertEquals(relations["2010/11/02/newer_post"], 
                               ["index", "2010/12/03/newest_post", "2010/10/01/oldest_post"])
    utils.test.assertEquals(relations["2010/10/01/oldest_post"], 
                               ["index", "2010/11/02/newer_post", "pages/first_page"])
    utils.test.assertEquals(relations["pages/first_page"],
                               ["index", "2010/10/01/oldest_post", "pages/second_page"])
    utils.test.assertEquals(relations["pages/second_page"],
                               ["index", "pages/first_page", None])


# extension setup    
def setup(app):
    app.connect("build-finished", build_finished)
