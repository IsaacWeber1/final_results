from scraper_module.config import *

config = SpiderConfig(
    name="calstate",
    start_url="http://catalog.csulb.edu/content.php?catoid=10&navoid=1156",
    use_playwright=False,
    tasks=[
        DynamicFind(
            task_name="dynamic_courses",
            search_space='xpath://a[contains(@href, "preview_course_nopop.php")]',
            base_url="http://catalog.csulb.edu/ajax/preview_course.php",
            catoid=10,
            fields={
                "title": 'xpath://h3//text()join',
                "description": 'xpath://div[2]/text()join'
            },
            pagination_selector='xpath://a[contains(@aria-label, "Page")]/@href'
        )
    ]
)