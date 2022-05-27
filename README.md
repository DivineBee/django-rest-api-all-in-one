## Task No2 for work integration process

## Prerequisites
* Create a new Django Rest Framework Project
* Configuration of PostgreSQL 
* Configuration of Elastic Search and Kibana
* Put each part of the system into a docker container inside Docker-compose file

## Tasks
* Authentication System using Firebase
* Create Product-Category models
* Create endpoints to display all products and categories
* Add CRUD endpoints for all products and categories
* Add ability to import categories and products from json files. (separate end-point)
* Sync existing database with ElasticSearch
* Search with autocomplete using ElasticSearch

## Explanation
A requirements file as well as an environment file was made to run the whole project through docker-compose, where all 
keys and dependencies are defined. With the command ``docker-compose up --build`` whole project should be build and run
with ease.  
There was needed to make two models: products and category. Because it is a one-to-many relationship (one category has 
many products) in the Product model the _category_ model was referenced as foreign key as follows:  
```python
class Product(models.Model):
    ...
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
```
Then for both models within _views.py_ were created api endpoints for listing the existing created instances using 
``ListCreateAPIView`` as such:
```python
class ProductList(generics.ListCreateAPIView):
    serializer_class = ProductSerializer  # reference to serializer class
    permission_classes = [permissions.IsAuthenticated]  # allow only authenticated users

    def get_queryset(self):  # without a defined query set it will not work
        return Product.objects.order_by('title')  # order products by their title
```
Because it wasn't needed anything additional for CRUD operations, it was used the ``RetrieveUpdateDestroyAPIView`` class
that will be inherited by the caller class, and performs all the CRUD operations by us.
```python
class ProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Product.objects.order_by('title')
```
For uploading from json instantly to database, it was required to:
* make an end-point in views for both models that inherit ``APIView``
* read the uploaded file
* check if it has contents and parse them
* extract the fields and assign to temporary dictionary
* assign dictionary to the save function upon the model.
_NOTE: Each model has its own file like: category.json and products.json_  

For synchronization of Postgres and ElasticSearch, as well as for implementing the search functionality it was needed to be created a document class that will be used in the
``ProductDocumentViewElasticSearch`` for both models that inherits ``BaseDocumentViewSet``. There are defined the filtering
fields, the searching fields and ordering. It is important to insert all the related configurations in settings file of the
project that will allow functioning of this autocomplete feature. Full logic can be seen in ``views.py``.  

Firebase authentication was done in an endpoint as well. With the use of firebase admin, in the ``auth.py`` was made a class
that extends ``rest_framework.BaseAuthentication`` it provides ``authenticate`` function, if successfull, it should 
return a user and if not, it should return None. This is done by extracting the authorization token from the request, it 
contains the Firebase user's id token.  If there’s no token, we return None, which means the user could not be authenticated.
if an idToken was provided, we need to verify it with Firebase. With ``firebase_admin package``, which has everything for
that. The verification could fail if token is expired etc. so we wrap it in a try/catch block. The function throws 
different types of exceptions according to an error, so you could except on different ones to get a better look into it,
those are in the ``exceptions.py``. In a previous step, we also extracted the uid corresponding to that idToken.
In my case, that uid is identifying the User object in our database, which holds the profile info. We do a quick query
and then return that user. If that fails (i.e. user doesn’t exist), we also return None which means auth was not successfull.

**Client**
Every client request to the backend must include the Firebase auth idToken. We obtain that token on the client and pack
it in the request headers. That’s everything special about the client. It could be an app or website for example.  
**Server**
For every request, we need to verify that idToken. If token is successfully verified, we then fetch the corresponding 
user profile from the database. If verification fails, we forbid the access to that resource.