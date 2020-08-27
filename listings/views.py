from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import price_choices, bedroom_choices, state_choices

from .models import Listing
# Create your views here.
def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True) #fetch all the listings according to descending date (-list_date), filter = filters out paramter given

    paginator = Paginator(listings, 3) #three listings in a page
    page = request.GET.get('page')
    page_listings = paginator.get_page(page)

    context = {
        'listings': page_listings
    }
    return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    context = {
        'listing': listing
    }
    return render(request, 'listings/listing.html', context)

def search(request):
    query_set = Listing.objects.order_by('-list_date')

    #keywords
    if 'keywords' in request.GET: # if keyword exist in the request data, ( .GET looks for the name attribute)
        keywords = request.GET['keywords'] #then put the keyword data in the keyword variable
        if keywords: #to check it is not a empty string
            query_set = query_set.filter(description__icontains=keywords) # __icontains is used to match if it contains text, not have to be exact

    #city 
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            query_set = query_set.filter(city__iexact=city) # __iexact is used to match if it contains that exact text, 'i' is for case insensitive

    #state
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            query_set = query_set.filter(state__iexact=state)

    #bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            query_set = query_set.filter(bedrooms__lte=bedrooms) #lte = less than or equal

    #price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            query_set = query_set.filter(price__lte=price)

    context = {
        'price_choices': price_choices,
        'bedroom_choices': bedroom_choices,
        'state_choices': state_choices,
        'listings': query_set,
        'values': request.GET # whatever we search for will be available to the search page 
    }

    return render(request, 'listings/search.html', context)