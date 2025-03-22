from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

# 1. Note Model
# Represents a simple note with a title, content, creation date, and author.
class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")

    def __str__(self):
        return self.title


# 2. Profile Model
# Extends the User model to store additional information like bio and profile picture.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


# 3. Product Model
# Represents a product with a name, description, price, and stock quantity.
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# 4. Category Model
# Represents a category for products or blog posts.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# 5. BlogPost Model
# Represents a blog post with a title, content, author, and publication date.
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# 6. Comment Model
# Represents a comment on a blog post or product review.
class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username}"


# 7. Order Model
# Represents an order placed by a user for one or more products.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    products = models.ManyToManyField(Product, through="OrderItem")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="Pending")

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


# 8. OrderItem Model
# Represents an item in an order, linking a product to an order with a quantity.
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in Order #{self.order.id}"


# 9. Review Model
# Represents a review for a product with a rating and comment.
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"


# 10. Notification Model
# Represents a notification for a user, such as order updates or messages.
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"


# 11. Tag Model
# Represents a tag for categorizing blog posts or products.
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# 12. PostTag Model
# Represents a many-to-many relationship between BlogPost and Tag.
class PostTag(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="post_tags")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="post_tags")

    def __str__(self):
        return f"{self.post.title} - {self.tag.name}"


# 13. Address Model
# Represents a user's address for shipping or billing purposes.
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"


# 14. Wishlist Model
# Represents a user's wishlist of products.
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlists")
    products = models.ManyToManyField(Product, related_name="wishlists")

    def __str__(self):
        return f"{self.user.username}'s Wishlist"


# 15. Coupon Model
# Represents a discount coupon for orders.
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


# 16. Cart Model
# Represents a user's shopping cart.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    products = models.ManyToManyField(Product, through="CartItem")

    def __str__(self):
        return f"{self.user.username}'s Cart"


# 17. CartItem Model
# Represents an item in a user's shopping cart.
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in Cart #{self.cart.id}"


# 18. Subscription Model
# Represents a user's subscription to a service or newsletter.
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Subscription for {self.email}"


# 19. Image Model
# Represents an image for products or blog posts.
class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", null=True, blank=True)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="images", null=True, blank=True)
    image = models.ImageField(upload_to="images/")
    caption = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.product.name if self.product else self.post.title}"


# 20. FAQ Model
# Represents frequently asked questions and answers.
class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question


# 21. ContactMessage Model
# Represents a message sent by a user through a contact form.
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
