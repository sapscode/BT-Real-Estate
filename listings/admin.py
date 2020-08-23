from django.contrib import admin

from .models import Listing
 
class ListingAdmin(admin.ModelAdmin): #to add extra functionality to the realtor admin area
    list_display = ('id', 'title', 'is_published', 'price', 'list_date', 'realtor',) #titles to display on the display 
    list_display_links = ('id', 'title',) #entries that can be clicked to take you to the that listings edit page
    list_filter = ('realtor',) #adding a filter based on the parameter
    list_editable = ('is_published',) #entry that you can edit from the admin page itself
    search_fields = ('title', 'description', 'address', 'city', 'state', 'zipcode', 'price',) #search on these parameters
    list_per_page = 25 #pagination

admin.site.register(Listing, ListingAdmin)
