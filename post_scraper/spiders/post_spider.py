import scrapy
from discord_webhook import DiscordWebhook, DiscordEmbed
from googletrans import Translator


class PostSpiderSpider(scrapy.Spider):
    name = "post_spider"
    start_urls = []
    custom_settings = {'ROBOTSTXT_OBEY': False,
                       'RETRY_TIMES': 5,
                       'DOWNLOAD_DELAY': 1
                       }
    # List of webhook URLs
    webhook_urls = [
        '<insert your discord channel webhook url>',
        # Add more webhook URLs as needed
    ]
    search_url = 'https://gall.dcinside.com/mgallery/board/lists/?id=diablo2resurrected&s_type=search_name&s_keyword=.ED.85.8C.EB.9F.AC.EC.A1.B4.EB.85.B8.EC.98.88'

    def start_requests(self):
        yield scrapy.Request(url=self.search_url, callback=self.parse)

    def parse(self, response, **kwargs):
        posts = response.xpath("//table[@class='gall_list']/tbody/tr[contains(@class,'us-post')]")
        for post in posts[:1]:
            detail_url = post.xpath('./td[3]/a[1]/@href').get('')
            yield response.follow(url=detail_url, callback=self.parse_detail)

    def parse_detail(self, response):
        new_content = []
        content = response.xpath("//div[@class='write_div']/div/text()").getall()
        for txt in content:
            if '●──────────────' in txt:
                continue
            elif '↻' in txt or '⇆' in txt:
                continue
            else:
                # Apply markdown formatting
                if ':' in txt:
                    key, value = txt.split(':', 1)
                    txt = f'**{key.strip()}**: {value.strip()}'
                elif '<' in txt and '>' in txt:
                    txt = f'**{txt}**'

                translator = Translator()
                translation = translator.translate(txt)

                if translation.text.strip() != 'Mmmmmmm':  # Ignore 'Mmmmmmm' after translation
                    new_content.append(translation.text)

        # Create an embed object with red color
        embed = DiscordEmbed(
            title="Next Terror Zone Should Be:",
            description='\n'.join(new_content),
            color=16711680  # Red color
        )

        # Set the footer
        embed.set_footer(text='Please note this info relies on Terror Zone Slave. Info can be incorrect or repeated.')


        # For each webhook URL, initialize a webhook object, add the embed, and execute
        for url in self.webhook_urls:
            webhook = DiscordWebhook(url=url)
            webhook.add_embed(embed)
            response = webhook.execute()

        print('POST SEND...')
