To also add to what i could not include in the loom, due to the recording time being limited: The last issue being mentioned by the finance team is related to a rounding error. 
The database seems to be safe from any rounding issues. Postgres stores the total_amount fine and calculates teh sum fine. 
The issue is that the backend returns the amount as a float which can lead to small inconsistencies throughout the time.
The fix is to return the total_amount as Decimal. I did not include this fix due to the issue not being observed in the data.

More clarifying details:

1. get_properties was already available and I simply exposed it as an endpoint. The UI was using hardcoded filters but it also had a function available for requesting the properties.
2. During my initial investigation I found a couple of issues that do not affect this test much but could be problematic in production environments. Prime example is the resolve_context_id function which defautls to tenant_a
3. I identified cache issues which could lead to data being missed or incorrectly attributed or processed and added the tenant_id to the cache key.
   
Some general remarks:

1. The fixes I made are minimal and are suited to this test only. I wanted to reuse as much available code as possible but in production environments this might not be possible.
2. Some issues required searching for common fixes and i did the search using a mistral-4-small using a web search tool. All items returned were verified by me.
3. The whole process could be accelerated by the usage of coding agents but I refrained from using them just to be safe.
