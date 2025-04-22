from scraper_module.config import *

config = SpiderConfig(
    name="university_of_florida",
    start_url="https://catalog.ufl.edu/UGRD/courses/",
    use_playwright=False,
    pagination=Search_Links(
        search_space='xpath://ul[contains(@class, "nav leveltwo")]',
        link_selector="xpath:li/a/@href",
        target_page_selector='html'
    ),
     tasks=[
        Find(
            task_name="courses",
            # Corrected the attribute selector: use = instead of a comma
            search_space='xpath://div[@class="sc_sccoursebyacadorg"]',
            # Added a dot to make the repeating selector relative to the search_space element
            repeating_selector='xpath://div[@class="courseblock courseblocktoggle"]',
            fields={
               "title": 'xpath:.//p[contains(@class, "courseblocktitle noindent")]/strong//text()',
                "description": 'xpath:.//p[contains(@class, "courseblockdesc noindent")]/text()join'
            },
            num_required=1
        )
    ]
)