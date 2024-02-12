import scrapy
from scrapy_scrapingbee import ScrapingBeeSpider, ScrapingBeeRequest


class LinkedCompanySpider(ScrapingBeeSpider):
    name = "linkedin_company_profile"

    # add your own list of company urls here
    company_pages = [
        'https://www.linkedin.com/company/usebraintrust?trk=public_jobs_jserp-result_job-search-card-subtitle',
        'https://www.linkedin.com/company/centraprise?trk=public_jobs_jserp-result_job-search-card-subtitle',
        "https://www.linkedin.com/company/lowe's-home-improvement?trk=public_jobs_jserp-result_job-search-card"
        "-subtitle/",
        "https://www.linkedin.com/company/tjx?trk=public_jobs_jserp-result_job-search-card-subtitle/",
        "https://www.linkedin.com/company/albertsons?trk=public_jobs_jserp-result_job-search-card-subtitle/",
        "https://www.linkedin.com/company/csi-companies?trk=public_jobs_jserp-result_job-search-card-subtitle/",
        "https://www.linkedin.com/company/sni-companies?trk=public_jobs_jserp-result_job-search-card-subtitle/",
        "https://www.linkedin.com/company/trc-companies-inc?trk=public_jobs_jserp-result_job-search-card-subtitle/",
        "https://www.linkedin.com/company/mccarthy-building-companies-inc?trk=public_jobs_jserp-result_job-search"
        "-card-subtitle/",
        "https://www.linkedin.com/company/otsuka-pharmaceutical-companies?trk=public_jobs_jserp-result_job-search"
        "-card-subtitle/",
        "https://www.linkedin.com/company/pipercompanies?trk=public_jobs_jserp-result_job-search-card-subtitle/",
        "https://www.linkedin.com/company/related?trk=public_jobs_jserp-result_job-search-card-subtitle/",
        "https://www.linkedin.com/company/loblaw-companies-limited?trk=public_jobs_jserp-result_job-search-card"
        "-subtitle/",
        "https://www.linkedin.com/company/audubon-companies?trk=public_jobs_jserp-result_job-search-card-subtitle/",
        "https://www.linkedin.com/company/the-davis-companies?trk=public_jobs_jserp-result_job-search-card-subtitle/",
        "https://www.linkedin.com/company/the-tempositions-group-of-companies?trk=public_jobs_jserp-result_job-search"
        "-card-subtitle/",
        "https://www.linkedin.com/company/shelter-insurance-companies?trk=public_jobs_jserp-result_job-search-card"
        "-subtitle/",
        "https://www.linkedin.com/company/shopritegroup?trk=public_jobs_jserp-result_job-search-card-subtitle/",
        "https://www.linkedin.com/company/the-bainbridge-companies?trk=public_jobs_jserp-result_job-search-card"
        "-subtitle/",
        "https://www.linkedin.com/company/van-metre-companies?trk=public_jobs_jserp-result_job-search-card-subtitle/"
    ]

    def start_requests(self):

        company_index_tracker = 0

        first_url = self.company_pages[company_index_tracker]

        yield ScrapingBeeRequest(url=first_url,
                                 callback=self.parse_response,
                                 params={
                                     'render_js': False,
                                     'premium_proxy': False,
                                 },
                                 meta={'company_index_tracker': company_index_tracker})

    def parse_response(self, response):
        company_index_tracker = response.meta['company_index_tracker']
        print('***************')
        print('****** Scraping page ' + str(company_index_tracker + 1) + ' of ' + str(len(self.company_pages)))
        print('***************')

        company_item = {
            'name': response.css('.top-card-layout__entity-info h1::text').get(default='not-found').strip(),
            'summary': response.css('.top-card-layout__entity-info h4 span::text').get(default='not-found').strip()}

        try:
            # all company details
            company_details = response.css('.core-section-container__content .mb-2')

            # industry line
            company_industry_line = company_details[1].css('.text-md::text').getall()
            company_item['industry'] = company_industry_line[1].strip()

            # company size line
            company_size_line = company_details[2].css('.text-md::text').getall()
            company_item['size'] = company_size_line[1].strip()

            # company founded
            company_size_line = company_details[5].css('.text-md::text').getall()
            company_item['founded'] = company_size_line[1].strip()
        except IndexError:
            print("Error: Skipped Company - Some details missing")

        yield company_item

        company_index_tracker = company_index_tracker + 1

        if company_index_tracker <= (len(self.company_pages) - 1):
            next_url = self.company_pages[company_index_tracker]

            yield ScrapingBeeRequest(url=next_url,
                                     params={
                                         'render_js': False,
                                         'premium_proxy': False,
                                     },
                                     callback=self.parse_response,
                                     meta={'company_index_tracker': company_index_tracker})
