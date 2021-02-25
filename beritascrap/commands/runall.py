from scrapy.commands import BaseRunSpiderCommand
from scrapy.utils.project import get_project_settings


class Command(BaseRunSpiderCommand):
    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs all of the spiders'

    def run(self, args, opts):
        settings = get_project_settings()
        print(self.crawler_process.spiders.list())
        print(settings)

        print(opts.spargs)
        for spider_name in self.crawler_process.spiders.list():
            self.crawler_process.crawl(spider_name, **opts.spargs)
        self.crawler_process.start()
