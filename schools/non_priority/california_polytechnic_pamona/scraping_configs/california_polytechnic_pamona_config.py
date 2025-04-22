from scraper_module.config import *

config = SpiderConfig(
    name="cpp",
    start_url="https://catalog.cpp.edu/content.php?catoid=68&navoid=5731",
    use_playwright=False,
    tasks=[
        DynamicFind(
            task_name="dynamic_courses",
            search_space='xpath://a[contains(@href, "preview_course_nopop.php")]',
            base_url="http://catalog.cpp.edu/ajax/preview_course.php",
            catoid=68,
            fields={
                "title": 'xpath://h3//text()join',
                "description": 'xpath://div[2]/text()join'
            },
            pagination_selector='xpath://a[contains(@aria-label, "Page")]/@href'
        )
    ]
)