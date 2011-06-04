from schemaorg.base import Base

Boolean = bool

class Date(object):
    pass

class Float(float):
    pass

class Integer(int):
    pass

class Text(unicode):
    pass

class URL(Text):
    pass

def NumberOrText(n):
    try:
        if '.' in unicode(n):
            return Integer(n)
        else:
            return Float(n)
    except ValueError:
        return Text(n)

def Number(n):
    try:
        if '.' in unicode(n):
            return Integer(n)
        else:
            return Float(n)
    except ValueError:
        return Float(n)

# Currency
# PlaceOrPostalAddress
# PersonOrOrganization
# PhotographOrImageObject


class Thing(Base):
    properties = {'description': Text,
                        'image': URL,
                         'name': Text,
                          'url': Text}
    _base_URL = 'http://schema.org/'

class Intangible(Thing):
    pass

class Enumeration(Intangible):
    pass

class Rating(Intangible):
    properties = {'bestRating': NumberOrText,
                 'ratingValue': NumberOrText, # 2011-06-04: Spec has "Text", suspect a bug.
                 'worstRating': NumberOrText}

class AggregateRating(Rating):
    properties = {'itemReviewed': 'Thing',
                   'ratingCount': Number,
                   'reviewCount': Number}

class StructuredValue(Intangible):
    pass

class Place(Thing):
    properties = {'address': 'PostalAddress',
          'aggregateRating': 'AgregateRating',
              'containedIn': 'Place',
                   'events': 'Event',
                'faxNumber': Text,
                      'geo': 'GeoCoordinates',
         'interactionCount': Text,
                     'maps': 'Map',
                   'photos': 'PhotographOrImageObject',
                  'reviews': 'Review',
                'telephone': Text}

class AdministrativeArea(Place):
    pass

class City(AdministrativeArea):
    pass

class Country(AdministrativeArea):
    pass
    
class State(AdministrativeArea):
    pass

class ContactPoint(StructuredValue):
    properties = {'contactPoint': Text,
                         'email': Text,
                     'faxNumber': Text,
                     'telephone': Text}

class PostalAddress(ContactPoint):
    properties = {'addressCountry': 'Country',
                 'addressLocality': Text,
                   'addressRegion': Text,
             'postOfficeBoxNumber': Text,
                      'postalCode': Text,
                   'streetAddress': Text}

class Organization(Thing):
    properties = {'address': 'PostalAddress',
          'aggregateRating': 'AggregateRating',
            'contactPoints': 'ContactPoint',
                    'email': Text,
                'employees': 'Person',
                   'events': 'Event',
                'faxNumber': Text,
                 'founders': 'Person',
             'foundingDate': Date,
         'interactionCount': Text, # docs refer to UserInteraction
                 'location': 'PlaceOrPostalAddress',
                  'members': 'PersonOrOrganization',
                  'reviews': 'Review',
                'telephone': Text}

class Product(Thing):
    properties = {'aggregateRating': 'AggregateRating', 
                            'brand': 'Organization',
                     'manufacturer': 'Organization',
                            'model': Text,
                           'offers': 'Offer',
                        'productID': Text,
                          'reviews': 'Review'}


class Offer(Intangible):
    properties = {'aggregateRating': 'AggregateRating',
                     'availability': 'ItemAvailability',
                    'itemCondition': 'OfferItemCondition',
                      'itemOffered': 'Product',
                            'price': NumberOrText,
                    'priceCurrency': Text,
                  'priceValidUntil': Date,
                          'reviews': 'Review',
                           'seller': 'Organization'}

class AggregateOffer(Offer):
    properties = {'highPrice': NumberOrText,
                   'lowPrice': NumberOrText,
                 'offerCount': Integer}

class GeoCoordinates(StructuredValue):
    properties = {'elevation': NumberOrText,
                   'latitude': NumberOrText,
                  'longitude': NumberOrText}

