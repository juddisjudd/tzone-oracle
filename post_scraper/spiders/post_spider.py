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
    webhook_url = '<insert your own discord channel webhook url>'
    search_url = 'https://gall.dcinside.com/mgallery/board/lists?id=diablo2resurrected&s_type=search_subject_memo&s_keyword=.EB.8B.A4.EC.9D.8C.20.ED.85.8C.EB.9F.AC.EC.A1.B4'

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

        # Initialize a webhook object
        webhook = DiscordWebhook(url=self.webhook_url)

        # Add the embed object to the webhook
        webhook.add_embed(embed)

        # Execute the webhook
        response = webhook.execute()

        print('POST SEND...')
