from scraper_module.config import *

config = SpiderConfig(
    name="savannah",
    start_url="http://catalog.savannahstate.edu/content.php?catoid=13&navoid=630",
    use_playwright=False,
    tasks=[
        DynamicFind(
            task_name="dynamic_courses",
            search_space='xpath://a[contains(@href, "preview_course_nopop.php")]',
            base_url="https://catalog.savannahstate.edu/ajax/preview_course.php",
            catoid=13,
            fields={
                "title": 'xpath://h3//text()join',
                "description": 'xpath://div[2]/text()[3]join'
            },
            pagination_selector='xpath://a[contains(@aria-label, "Page")]/@href'
        )
    ]
)