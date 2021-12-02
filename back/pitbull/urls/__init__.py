from .dataFetchingURLs import *
from .documentationURLs import *
from .stockManagingURLs import *
from .usersManagingURLs import *
from .authURLs import *

urlpatterns = data_fetching_urlpatterns + documentation_urlpatterns +\
              stock_managing_urlpatterns + users_managing_urlpatterns + \
              auth_urlpatterns