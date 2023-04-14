import requests
from bs4 import BeautifulSoup
from bs4.element import Tag, ResultSet
from .site import Site

class ZoneLetting(Site):
    PREPEND = 'https://zonegroup.co.uk'

    def __init__(self, link:str):
        super().__init__(link)

    def get_title(self, listing:Tag) -> str:
        try:
            bedrooms = listing.select('div[class="zText semiSmallText semiBoldWeight propertyMetaItem"]')[-1].contents[-1]
            location = listing.select('p', {'class': 'proAddress'})[0].contents[-1]
            return f'{bedrooms} flat at {location}'
        
        except:
            return self.MISSING

    def get_link(self, listing:Tag) -> str:
        try:
            raw_link = listing.a['href']
            return ZoneLetting.PREPEND + raw_link

        except:
            return self.MISSING

    def get_price(self, listing:Tag) -> str:
        try:
            price_str = listing.h3.string
            start_idx = price_str.find('£')
            return price_str[start_idx:]
        
        except:
            return self.MISSING

    def get_availability(self, listing:Tag) -> str:
            try:
                response = requests.get(self.link)
                soup = BeautifulSoup(response.text, 'html.parser')
                return soup.select('div[class="zText semiMediumText semiBoldWeight metaDataSectionItem"]')[0].span.string
            
            except:
                return self.MISSING

    def get_raw_listings(self) -> ResultSet:
        return self.soup.find_all('div', {'class': 'propertyItem'})
    