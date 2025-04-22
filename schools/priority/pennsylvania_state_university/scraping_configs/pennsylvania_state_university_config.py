from scraper_module.config import *

config = SpiderConfig(
    name="pennstate",
    start_url="https://bulletins.psu.edu/university-course-descriptions/undergraduate/",
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
            search_space='xpath://div[@class="sc_sccoursedescs"]',
            # Added a dot to make the repeating selector relative to the search_space element
            repeating_selector='xpath://div[@class="courseblock"]',
            fields={
               "title": 'xpath:.//div[contains(@class, "course_codetitle")]/text()',
                "description": 'xpath:.//div[contains(@class, "courseblockdesc")]/p/text()join'
            },
            num_required=1
        )
    ]
)