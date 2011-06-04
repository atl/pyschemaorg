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
# PlaceOrContactPoint
# PersonOrOrganization
# PhotographOrImageObject


class Thing(Base):
    '''The most generic type of item.'''
    properties = {'description': Text,
                        'image': URL,
                         'name': Text,
                          'url': Text}
    _base_URL = 'http://schema.org/'

class Intangible(Thing):
    '''A utility class that serves as the umbrella for a number of 'intangible' things such as quantities,
    structured values, etc.'''
    pass

class Enumeration(Intangible):
    '''Lists or enumerations - for example, a list of cuisines or music genres, etc.'''
    pass

class Language(Intangible):
    '''Natural languages such as Spanish, Tamil, Hindi, English, etc. and programming languages 
    such as Scheme and Lisp.'''
    pass

class Offer(Intangible):
    '''An offer to sell an item - for example, an offer to sell a product, the DVD of a movie, 
    or tickets to an event.'''
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
    '''When a single product that has different offers (for example, the same pair of shoes 
    is offered by different merchants), then AggregateOffer can be used.'''
    properties = {'highPrice': NumberOrText,
                   'lowPrice': NumberOrText,
                 'offerCount': Integer}

class Quantity(Intangible):
    '''Quantities such as distance, time, mass, weight, etc. Particular instances of say Mass are 
    entities like '3 Kg' or '4 milligrams'.'''
    pass

class Distance(Quantity):
    '''Properties that take Distances as values are of the form '<Number> <Length unit of measure>'. 
    E.g., '7 ft' '''
    pass

class Duration(Quantity, Date):
    '''Quantity: Duration (use ISO 8601 duration format).'''
    pass

class Mass(Quantity):
    '''Properties that take Mass as values are of the form '<Number> <Mass unit of measure>'. E.g., '7 kg' '''
    pass

class Rating(Intangible):
    '''The rating of the video.'''
    properties = {'bestRating': NumberOrText,
                 'ratingValue': NumberOrText, # 2011-06-04: Spec has "Text", suspect a bug.
                 'worstRating': NumberOrText}

class AggregateRating(Rating):
    '''The average rating based on multiple ratings or reviews.'''
    properties = {'itemReviewed': 'Thing',
                   'ratingCount': Number,
                   'reviewCount': Number}

class StructuredValue(Intangible):
    '''Structured values are strings - for example, addresses - that have certain constraints on their 
    structure.'''
    pass

class ContactPoint(StructuredValue):
    '''A contact point - for example, a Customer Complaints department.'''
    properties = {'contactPoint': Text,
                         'email': Text,
                     'faxNumber': Text,
                     'telephone': Text}

class PostalAddress(ContactPoint):
    '''The mailing address.'''
    properties = {'addressCountry': 'Country',
                 'addressLocality': Text,
                   'addressRegion': Text,
             'postOfficeBoxNumber': Text,
                      'postalCode': Text,
                   'streetAddress': Text}

class GeoCoordinates(StructuredValue):
    '''The geographic coordinates of a place or event.'''
    properties = {'elevation': NumberOrText,
                   'latitude': NumberOrText,
                  'longitude': NumberOrText}

class NutritionalInformation(StructuredValue):
    '''Nutritional information about the recipe.'''
    properties = {'calories': 'Energy', # The number of calories
       'carbohydrateContent': 'Mass', # The number of grams of carbohydrates.
        'cholesterolContent': 'Mass', # The number of milligrams of cholesterol.
                'fatContent': 'Mass', # The number of grams of fat.
              'fiberContent': 'Mass', # The number of grams of fiber.
            'proteinContent': 'Mass', # The number of grams of protein.
       'saturatedFatContent': 'Mass', # The number of grams of saturated fat.
               'servingSize': Text, # The serving size, in terms of the number of volume or mass
             'sodiumContent': 'Mass', # The number of milligrams of sodium.
              'sugarContent': 'Mass', # The number of grams of sugar.
           'transFatContent': 'Mass', # The number of grams of trans fat.
     'unsaturatedFatContent': 'Mass'  # The number of grams of unsaturated fat.
    }

class Place(Thing):
    '''Entities that have a somewhat fixed, physical extension.'''
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
    '''A geographical region under the jurisdiction of a particular government.'''
    pass

class City(AdministrativeArea):
    '''A city or town.'''
    pass

class Country(AdministrativeArea):
    '''A country.'''
    pass
    
class State(AdministrativeArea):
    '''A state or province.'''
    pass

class Organization(Thing):
    '''An organization such as a school, NGO, corporation, club, etc.'''
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

class Corporation(Organization):
    '''Organization: A business corporation.'''
    pass

class EducationalOrganization(Organization):
    '''An educational organization.'''
    properties = {'alumni': 'Person'}

class CollegeOrUniversity(EducationalOrganization):
    '''A college, university, or other third-level educational institution.'''
    pass

class ElementarySchool(EducationalOrganization):
    '''An elementary school.'''
    pass

class HighSchool(EducationalOrganization):
    '''A high school.'''
    pass

class MiddleSchool(EducationalOrganization):
    '''A middle school.'''
    pass

class Preschool(EducationalOrganization):
    '''A preschool.'''
    pass

class School(EducationalOrganization):
    '''A school.'''
    pass

class GovernmentOrganization(Organization):
    '''A governmental organization or agency.'''
    pass

class LocalBusiness(Organization, Place):
    '''A particular physical business or branch of an organization. Examples of
    LocalBusiness include a restaurant, a particular branch of a restaurant chain, a
    branch of a bank, a medical practice, a club, a bowling alley, etc.'''
    properties = {'branchOf': 'Organization', # The larger organization that this local business is a branch of, if any.
        'currenciesAccepted': Text, # The currency accepted (in ISO 4217 currency format).
              'openingHours': Duration, # The opening hours for a business. Opening hours can be specified as a weekly time range, starting with days, then times per day. Multiple days can be listed with commas ',' separating each day. Day or time ranges are specified using a hyphen '-'.
                                        # - Days are specified using the following two-letter combinations: Mo, Tu, We, Th, Fr, Sa, Su.
                                        # - Times are specified using 24:00 time. For example, 3pm is specified as 15:00.
                                        # Here is an example: <time itemprop="openingHours" datetime="Tu,Th 16:00-20:00">Tuesdays and Thursdays 4-8pm</time>
           'paymentAccepted': Text, # Cash, credit card, etc.
                'priceRange': Text # The price range of the business, for example $$$.
    }

class Product(Thing):
    '''A product is anything that is made available for sale - 
    for example, a pair of shoes, a concert ticket, or a car.''' 
    properties = {'aggregateRating': 'AggregateRating',
                            'brand': 'Organization', 
                     'manufacturer': 'Organization', 
                            'model': Text, 
                           'offers': 'Offer', 
                        'productID': Text, 
                          'reviews': 'Review'}

class Person(Thing):
    '''A person (alive, dead, undead, or fictional).'''
    properties = {'address': 'PostalAddress', # Physical address of the item.
              'affiliation': 'Organization', # An organization that this person is affiliated with. For example, a school/university, a club, or a team.
                 'alumniOf': 'EducationalOrganization', # An educational organizations that the person is an alumni of.
                   'awards': Text, # Awards won by this person or for this creative work.
                'birthDate': Date, # Date of birth.
                 'children': 'Person', # A child of the person.
               'colleagues': 'Person', # A colleague of the person.
            'contactPoints': 'ContactPoint', # A contact point for a person or organization.
                'deathDate': Date, # Date of death.
                    'email': Text, # Email address.
                'faxNumber': Text, # The fax number.
                  'follows': 'Person', # The most generic uni-directional social relation.
                   'gender': Text, # Gender of the person.
             'homeLocation': 'PlaceOrContactPoint', # A contact location for a person's residence.
         'interactionCount': Text, # A count of a specific user interactions with this item - fors example, 20 UserLikes, 5 UserComments, or 300 UserDownloads. The user interaction type should be one of the sub types of UserInteraction.
                 'jobTitle': Text, # The job title of the person (for example, Financial Manager).
                    'knows': 'Person', # The most generic bi-directional social/work relation.
                 'memberOf': 'Organization', # An organization to which the person belongs.
              'nationality': 'Country', # Nationality of the person.
                  'parents': 'Person', # A parents of the person.
              'performerIn': 'Event', # Event that this person is a performer or participant in.
                'relatedTo': 'Person', # The most generic familial relation.
                 'siblings': 'Person', # A sibling of the person.
                   'spouse': 'Person', # The person's spouse.
                'telephone': Text, # The telephone number.
             'workLocation': 'PlaceOrContactPoint', # A contact location for a person's place of work.
                 'worksFor': 'Organization' # Organizations that the person works for.
    }
