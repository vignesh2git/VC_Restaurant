from django.core.management.base import BaseCommand

from menu.models import Dish, DeliveryZone


SAMPLE_DISHES = [
    {
        "name": "Margherita Pizza",
        "description": "Classic pizza with tomato sauce, mozzarella, and basil. Margherita pizza is a classic Italian pizza that originated in Naples. It features a simple yet delicious combination of hand-crushed peeled tomatoes, mozzarella cheese (either buffalo mozzarella or fior di latte), fresh basil leaves, and extra virgin olive oil.",
        "price": "245.00",        
        "image_url": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8cGl6emElMjBpbWFnZXxlbnwwfHwwfHx8MA%3D%3D",
    },
    {
        "name": "Cheeseburger",
        "description": "Juicy beef patty with cheddar, lettuce, tomato, and pickles.",
        "price": "150.00",
        "image_url": "https://images.unsplash.com/photo-1572802419224-296b0aeee0d9?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Q2hlZXNlYnVyZ2VyfGVufDB8fDB8fHww",
    },
    {
        "name": "Pasta Carbonara",
        "description": "Creamy sauce with pancetta, egg, and Parmesan.",
        "price": "200.00",
        "image_url": "https://images.unsplash.com/photo-1719250726371-b4076d48ce6c?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTJ8fFBhc3RhJTIwQ2FyYm9uYXJhfGVufDB8fDB8fHww",
    },
    {
        "name": "Caesar Salad",
        "description": "Romaine, croutons, Parmesan, and Caesar dressing.",
        "price": "80.00",
        "image_url": "https://images.unsplash.com/photo-1580013759032-c96505e24c1f?w=600&auto=format&fit=crop&q=60",
    },
    {
        "name": "Chicken Biryani",
        "description": "Aromatic basmati rice with spiced chicken and herbs.",
        "price": "250.00",
        "image_url": "https://images.unsplash.com/photo-1631515243349-e0cb75fb8d3a?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8Q2hpY2tlbiUyMEJpcnlhbml8ZW58MHx8MHx8fDA%3D",
    },
    {
        "name": "Veggie Wrap",
        "description": "Grilled veggies, hummus, and greens in a soft wrap.",
        "price": "120.00",
        "image_url": "https://images.unsplash.com/photo-1666819615040-eff5e52c778a?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8d3JhcHxlbnwwfHwwfHx8MA%3D%3D",
    },
    {
        "name": "Sushi Platter",
        "description": "Assorted nigiri and maki rolls with fresh fish.",
        "price": "300.00",
        "image_url": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8c3VzaGl8ZW58MHx8MHx8fDA%3D",
    },
    {
        "name": "Pad Thai",
        "description": "Stir-fried rice noodles with shrimp, peanuts, and tamarind.",
        "price": "110.00",
        "image_url": "https://images.unsplash.com/photo-1655091273851-7bdc2e578a88?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8UGFkJTIwVGhhaXxlbnwwfHwwfHx8MA%3D%3D",
    },
    {
        "name": "Tacos Al Pastor",
        "description": "Marinated pork, pineapple, cilantro, and onions on corn tortillas.",
        "price": "100.00",
        "image_url": "https://plus.unsplash.com/premium_photo-1681406995031-fe952f1e0858?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjV8fFRhY29zJTIwQWwlMjBQYXN0b3J8ZW58MHx8MHx8fDA%3D",
    },
    {
        "name": "Butter Chicken",
        "description": "Creamy tomato-based curry with tender chicken.",
        "price": "130.00",
        "image_url": "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8QnV0dGVyJTIwQ2hpY2tlbnxlbnwwfHwwfHx8MA%3D%3D",
    },
    {
        "name": "Falafel Bowl",
        "description": "Crispy falafel with quinoa, veggies, and tahini sauce.",
        "price": "150.00",
        "image_url": "https://images.unsplash.com/photo-1701688596783-231b3764ef67?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8RmFsYWZlbCUyMEJvd2x8ZW58MHx8MHx8fDA%3D",
    },
    {
        "name": "Chocolate Brownie",
        "description": "Rich fudge brownie with walnuts.",
        "price": "85.00",
        "image_url": "https://images.unsplash.com/photo-1612078960206-1709f1f0c969?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8Q2hvY29sYXRlJTIwQnJvd25pZXxlbnwwfHwwfHx8MA%3D%3D",
    },
    {
        "name": "Greek Salad",
        "description": "Tomatoes, cucumbers, olives, feta, oregano, olive oil.",
        "price": "110.00",
        "image_url": "https://images.unsplash.com/photo-1505253716362-afaea1d3d1af?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8R3JlZWslMjBTYWxhZHxlbnwwfHwwfHx8MA%3D%3D",
    },
    {
        "name": "Ramen Bowl",
        "description": "Soy broth with chashu pork, egg, scallions, and nori.",
        "price": "250.00",
        "image_url": "https://plus.unsplash.com/premium_photo-1694708455249-992010f9db32?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8UmFtZW4lMjBCb3dsfGVufDB8fDB8fHww",
    },
    {
        "name": "Grilled Salmon",
        "description": "Lemon-herb salmon with roasted vegetables.",
        "price": "300.00",
        "image_url": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8R3JpbGxlZCUyMFNhbG1vbnxlbnwwfHwwfHx8MA%3D%3D",
    },
    {
        "name": "BBQ Ribs",
        "description": "Slow-cooked pork ribs glazed in smoky BBQ sauce.",
        "price": "300.00",
        "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8QkJRJTIwUmlic3xlbnwwfHwwfHx8MA%3D%3D",
    },
    {
        "name": "Avocado Toast",
        "description": "Sourdough toast with smashed avocado and chili flakes.",
        "price": "150.00",
        "image_url": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?auto=format&fit=crop&w=800&q=60",
    },
    {
        "name": "Pancake Stack",
        "description": "Fluffy pancakes with berries and maple syrup.",
        "price": "100.00",
        "image_url": "https://images.unsplash.com/photo-1495214783159-3503fd1b572d?auto=format&fit=crop&w=800&q=60",
    },
    {
        "name": "French Fries",
        "description": "Crispy golden fries with sea salt.",
        "price": "70.00",
        "image_url": "https://images.unsplash.com/photo-1598679253544-2c97992403ea?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8RnJlbmNoJTIwRnJpZXN8ZW58MHx8MHx8fDA%3D",
    },
    {
        "name": "Chicken Wings",
        "description": "Spicy buffalo wings with blue cheese dip.",
        "price": "130.00",
        "image_url": "https://plus.unsplash.com/premium_photo-1669742928112-19364a33b530?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8Q2hpY2tlbiUyMFdpbmdzfGVufDB8fDB8fHww",
    },
    {
        "name": "Steak Frites",
        "description": "Grilled sirloin with herb butter and fries.",
        "price": "350.00",
        "image_url": "https://images.unsplash.com/photo-1600891964092-4316c288032e?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8U3RlYWslMjBGcml0ZXN8ZW58MHx8MHx8fDA%3D",
    },
    {
        "name": "Mediterranean Platter",
        "description": "Hummus, pita, olives, feta, tabbouleh.",
        "price": "180.00",
        "image_url": "https://plus.unsplash.com/premium_photo-1687870051860-287c4a6b02d6?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzN8fE1lZGl0ZXJyYW5lYW4lMjBQbGF0dGVyfGVufDB8fDB8fHww",
    },
    {
        "name": "Chicken Tikka Masala",
        "description": "Tender chicken in creamy spiced tomato sauce.",
        "price": "180.00",
        "image_url": "https://images.unsplash.com/photo-1728910107534-e04e261768ae?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8QnV0dGVyJTIwQ2hpY2tlbnxlbnwwfHwwfHx8MA%3D%3D",
    },
    {
        "name": "Veggie Pizza",
        "description": "Peppers, mushrooms, onions, olives, mozzarella.",
        "price": "110.00",
        "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8VmVnZ2llJTIwUGl6emF8ZW58MHx8MHx8fDA%3D",
    },
    {
        "name": "Caprese Sandwich",
        "description": "Mozzarella, tomato, basil, balsamic on ciabatta.",
        "price": "120.00",
        "image_url": "https://images.unsplash.com/photo-1509722747041-616f39b57569?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Q2FwcmVzZSUyMFNhbmR3aWNofGVufDB8fDB8fHww",
    },
    {
        "name": "Pho Soup",
        "description": "Vietnamese beef broth with rice noodles and herbs.",
        "price": "170.00",
        "image_url": "https://images.unsplash.com/photo-1631709497146-a239ef373cf1?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8UGhvJTIwU291cHxlbnwwfHwwfHx8MA%3D%3D",
    },
    {
        "name": "Chicken Caesar Wrap",
        "description": "Grilled chicken, romaine, Parmesan, Caesar dressing.",
        "price": "120.00",
        "image_url": "https://images.unsplash.com/photo-1529006557810-274b9b2fc783?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8Y2hpY2tlbiUyMHdyYXB8ZW58MHx8MHx8fDA%3D",
    },
    {
        "name": "Margarita",
        "description": "Refreshing lime cocktail with salted rim (non-alcoholic option).",
        "price": "70.00",
        "image_url": "https://images.unsplash.com/photo-1546171753-97d7676e4602?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjB8fE1hcmdhcml0YXxlbnwwfHwwfHx8MA%3D%3D",
    },
    {
        "name": "Iced Coffee",
        "description": "Cold brew over ice with milk option.",
        "price": "75.00",
        "image_url": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=800&q=60",
         "category": "beverages",
    },
    {
        "name": "Masala Chai",
        "description": "Indian spiced tea with milk and ginger.",
        "price": "85.00",
        "image_url": "https://images.unsplash.com/photo-1625033405953-f20401c7d848?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8TWFzYWxhJTIwQ2hhaXxlbnwwfHwwfHx8MA%3D%3D",
        "category": "beverages",
    },
    {
        "name": "Filter Coffee",
        "description": "Strong South Indian filter coffee.",
        "price": "90.00",
        "image_url": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=800&q=60",
        "category": "beverages",
    },
    {
        "name": "Espresso",
        "description": "Double shot espresso for a bold kick.",
        "price": "100.00",
        "image_url": "https://images.unsplash.com/photo-1485808191679-5f86510681a2?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fEVzcHJlc3NvfGVufDB8fDB8fHww",
        "category": "beverages",
    },
    {
        "name": "Vegetable Sandwich",
        "description": "Toasted sandwich with cucumber, tomato, and chutney.",
        "price": "70.00",
        "image_url": "https://images.unsplash.com/photo-1655195672061-90c23e3e8026?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzB8fFZlZ2V0YWJsZSUyMFNhbmR3aWNofGVufDB8fDB8fHww",
        "category": "snacks",
    },
    {
        "name": "Paneer Pakora",
        "description": "Batter-fried paneer fritters, served with mint chutney.",
        "price": "90.00",
        "image_url": "https://images.unsplash.com/photo-1548340748-6d2b7d7da280?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8ZnJpZWR8ZW58MHx8MHx8fDA%3D",
        "category": "snacks",
    },
    {
        "name": "Cheesecake",
        "description": "Creamy New York-style cheesecake with berry coulis.",
        "price": "100.00",
        "image_url": "https://plus.unsplash.com/premium_photo-1722686461601-b2a018a4213b?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8Q2hlZXNlY2FrZXxlbnwwfHwwfHx8MA%3D%3D",
    },
    {
        "name": "Tiramisu",
        "description": "Classic Italian coffee-flavored dessert.",
        "price": "95.00",
        "image_url": "https://plus.unsplash.com/premium_photo-1695028378225-97fbe39df62a?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8VGlyYW1pc3V8ZW58MHx8MHx8fDA%3D",
    },
    {
        "name": "Mac and Cheese",
        "description": "Creamy cheddar macaroni with breadcrumb topping.",
        "price": "130.00",
        "image_url": "https://plus.unsplash.com/premium_photo-1661677825991-caa232fea9da?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8bWFjYXJvbmklMjBhbmQlMjBjaGVlc2V8ZW58MHx8MHx8fDA%3D",
    },
    {
        "name": "Fish and Chips",
        "description": "Crispy beer-battered fish with tartar sauce.",
        "price": "12.25",
        "image_url": "https://plus.unsplash.com/premium_photo-1695758774479-faae1180b078?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OXx8RmlzaCUyMGFuZCUyMENoaXBzfGVufDB8fDB8fHww",
    },
    {
        "name": "Chicken burger",
        "description": "Crispy beer-battered fish with tartar sauce.",
        "price": "120.00",
        "image_url": "https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=800&q=60",
    },
    {
        "name": "Masala Dosa",
        "description": "Crispy rice crepe filled with spiced potato masala, served with sambar and chutney.",
        "price": "120.00",
        "image_url": "https://images.unsplash.com/photo-1668236543090-82eba5ee5976?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8TWFzYWxhJTIwRG9zYXxlbnwwfHwwfHx8MA%3D%3D",
        "category": "meals",
    },
    {
        "name": "Paneer Butter Masala",
        "description": "Cottage cheese cubes simmered in rich creamy tomato gravy.",
        "price": "240.00",
        "image_url": "https://images.unsplash.com/photo-1701579231378-3726490a407b?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8UGFuZWVyJTIwQnV0dGVyJTIwTWFzYWxhfGVufDB8fDB8fHww",
        "category": "meals",
    },
    {
        "name": "Chicken Biryani (Hyderabadi)",
        "description": "Layered basmati rice with succulent chicken, aromatic spices, fried onions.",
        "price": "260.00",
        "image_url": "https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8YmlyeWFuaXxlbnwwfHwwfHx8MA%3D%3D",
    },
    {
        "name": "Veg Thali",
        "description": "Assorted Indian curries, dal, rice, roti, salad, dessert.",
        "price": "220.00",
        "image_url": "https://images.unsplash.com/photo-1742281257687-092746ad6021?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8VmVnJTIwVGhhbGl8ZW58MHx8MHx8fDA%3D",
    },
    {
        "name": "Rogan Josh",
        "description": "Kashmiri-style lamb curry with aromatic spices.",
        "price": "320.00",
        "image_url": "https://images.unsplash.com/photo-1640542509430-f529fdfce835?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTV8fGxhbWIlMjBjdXJyeXxlbnwwfHwwfHx8MA%3D%3D",
    },
    {
        "name": "Butter Naan",
        "description": "Soft tandoor-baked flatbread brushed with butter.",
        "price": "45.00",
        "image_url": "https://images.unsplash.com/photo-1655979284091-eea0e93405ee?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8bmFhbnxlbnwwfHwwfHx8MA%3D%3D",
        "category": "meals",
    },
    {
        "name": "Tandoori Chicken",
        "description": "Yogurt and spice-marinated chicken roasted in tandoor.",
        "price": "280.00",
        "image_url": "https://plus.unsplash.com/premium_photo-1669245207961-0281fd9396eb?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8VGFuZG9vcmklMjBDaGlja2VufGVufDB8fDB8fHww",
    },
    {
        "name": "Chole Bhature",
        "description": "Spiced chickpea curry with fluffy fried bhature.",
        "price": "140.00",
        "image_url": "https://images.unsplash.com/photo-1717587052948-fb9825de50f8?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8aW5kaWFuJTIwc3RyZWV0JTIwZm9vZHxlbnwwfHwwfHx8MA%3D%3D",
    },
    {
        "name": "Vada Pav",
        "description": "Mumbai-style potato fritter slider with chutneys.",
        "price": "35.00",
        "image_url": "https://images.unsplash.com/photo-1750767397012-3413ba4fdbc7?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OXx8VmFkYSUyMFBhdnxlbnwwfHwwfHx8MA%3D%3D",
        "category": "snacks",
    },
    {
        "name": "Pani Puri",
        "description": "Crispy puris filled with tangy spiced water and potatoes.",
        "price": "60.00",
        "image_url": "https://images.unsplash.com/photo-1760263051331-0e4d3dafc9ff?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NTJ8fGluZGlhbiUyMHN0cmVldCUyMGZvb2R8ZW58MHx8MHx8fDA%3D",
        "category": "snacks",
    },
    {
        "name": "Pav Bhaji",
        "description": "Spiced mashed vegetable curry with buttered pav.",
        "price": "130.00",
        "image_url": "https://images.unsplash.com/photo-1619193099598-6856ec4e2a87?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTl8fGluZGlhbiUyMHN0cmVldCUyMGZvb2R8ZW58MHx8MHx8fDA%3D",
    },
    {
        "name": "Idli Sambar",
        "description": "Steamed rice cakes served with sambar and coconut chutney.",
        "price": "90.00",
        "image_url": "https://images.unsplash.com/photo-1632104667384-06f58cb7ad44?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8SWRsaSUyMFNhbWJhcnxlbnwwfHwwfHx8MA%3D%3D",
        "category": "meals",
    },
    {
        "name": "Gulab Jamun",
        "description": "Soft milk-solid dumplings soaked in rose-cardamom syrup.",
        "price": "80.00",
        "image_url": "https://images.unsplash.com/photo-1666190092159-3171cf0fbb12?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8R3VsYWIlMjBKYW11bnxlbnwwfHwwfHx8MA%3D%3D",
        "category": "desserts",
    },
    {
        "name": "Jalebi",
        "description": "Crisp pretzel-shaped sweets soaked in saffron syrup.",
        "price": "70.00",
        "image_url": "https://images.unsplash.com/photo-1760263216784-a4ca9a841ff5?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTN8fGphbGViaXxlbnwwfHwwfHx8MA%3D%3D",
        "category": "desserts",
    },
    {
        "name": "Rasmalai",
        "description": "Cottage cheese patties soaked in sweet cardamom milk.",
        "price": "110.00",
        "image_url": "https://images.unsplash.com/photo-1694402594431-23c594be1745?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8UmFzbWFsYWl8ZW58MHx8MHx8fDA%3D",
        "category": "desserts",
    },
    {
        "name": "Kulfi",
        "description": "Traditional Indian ice cream, pistachio flavored.",
        "price": "90.00",
        "image_url": "https://images.unsplash.com/photo-1683135801080-d276e9028a6a?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTY0fHxpY2UlMjBjcmVhbXxlbnwwfHwwfHx8MA%3D%3D",
        "category": "desserts",
    },
    {
        "name": "Lassi (Mango)",
        "description": "Refreshing mango yogurt drink.",
        "price": "80.00",
        "image_url": "https://images.unsplash.com/photo-1623065422902-30a2d299bbe4?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8bWFuZ28lMjBsYXNzaXxlbnwwfHwwfHx8MA%3D%3D",
        "category": "beverages",
    },
    {
        "name": "Fish Curry (Goan)",
        "description": "Tangy coconut-based curry with fish and spices.",
        "price": "300.00",
        "image_url": "https://images.unsplash.com/photo-1645066804237-08145dd196e9?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NTV8fEZpc2glMjBDdXJyeSUyMChHb2FuKXxlbnwwfHwwfHx8MA%3D%3D",
    },
    {
        "name": "Butter Chicken Roll",
        "description": "Kathi roll stuffed with butter chicken and onions.",
        "price": "160.00",
        "image_url": "https://images.unsplash.com/photo-1559095240-55a16b2dda6a?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8ZWdnJTIwcm9sbHxlbnwwfHwwfHx8MA%3D%3D",
    },
    {
        "name": "Samosa",
        "description": "Crispy pastry with spiced potato-pea filling.",
        "price": "30.00",
        "image_url": "https://plus.unsplash.com/premium_photo-1695297515417-5aeacd5dd313?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjF8fFNhbW9zYXxlbnwwfHwwfHx8MA%3D%3D",
        "category": "snacks",
    },
    {
        "name": "Veg Fried Rice",
        "description": "Stir-fried rice with mixed vegetables and soy sauce.",
        "price": "140.00",
        "image_url": "https://images.unsplash.com/photo-1664717698774-84f62382613b?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8VmVnJTIwRnJpZWQlMjBSaWNlfGVufDB8fDB8fHww",
        "category": "meals",
    },
    {
        "name": "Paneer Tikka Masala",
        "description": "Grilled paneer in creamy tomato-onion gravy.",
        "price": "260.00",
        "image_url": "https://images.unsplash.com/photo-1690401767645-595de0e0e5f8?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8UGFuZWVyJTIwVGlra2ElMjBNYXNhbGF8ZW58MHx8MHx8fDA%3D",
        "category": "meals",
    },
    {
        "name": "Grilled Chicken Meal",
        "description": "Herb grilled chicken served with rice and salad.",
        "price": "280.00",
        "image_url": "https://images.unsplash.com/photo-1577110632782-397c0dea76b4?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTc2fHxHcmlsbGVkJTIwQ2hpY2tlbiUyME1lYWx8ZW58MHx8MHx8fDA%3D",
        "category": "meals",
    },
    {
        "name": "Chocolate Cake Slice",
        "description": "Moist chocolate cake with ganache frosting.",
        "price": "95.00",
        "image_url": "https://images.unsplash.com/photo-1695605302698-21f49c671a41?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjN8fENob2NvbGF0ZSUyMENha2UlMjBTbGljZXxlbnwwfHwwfHx8MA%3D%3D",
        "category": "desserts",
    },
    {
        "name": "Black Forest Cake",
        "description": "Layers of chocolate sponge, cherries and cream.",
        "price": "120.00",
        "image_url": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=800&q=60",
        "category": "desserts",
    },
    {
        "name": "Cafe Mocha",
        "description": "Chocolate flavored latte with cocoa.",
        "price": "110.00",
        "image_url": "https://images.unsplash.com/photo-1632845407875-10b4d85e6bf8?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjR8fENhZmUlMjBNb2NoYXxlbnwwfHwwfHx8MA%3D%3D",
        "category": "beverages",
    },
    {
        "name": "Cold Coffee Frappe",
        "description": "Blended iced coffee with milk and cream.",
        "price": "120.00",
        "image_url": "https://images.unsplash.com/photo-1747218622335-77b9bb8f76bb?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NzF8fENvbGQlMjBDb2ZmZWUlMjBGcmFwcGV8ZW58MHx8MHx8fDA%3D",
        "category": "beverages",
    },
    {
        "name": "Herbal Tea",
        "description": "Caffeine-free infusion of herbs and flowers.",
        "price": "45.00",
        "image_url": "https://images.unsplash.com/photo-1648455321715-e8ed86188c0e?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fEhlcmJhbCUyMFRlYXxlbnwwfHwwfHx8MA%3D%3D",
        "category": "beverages",
    },
    {
        "name": "Loaded Nachos",
        "description": "Corn chips topped with cheese, beans and salsa.",
        "price": "160.00",
        "image_url": "https://images.unsplash.com/photo-1582169296194-e4d644c48063?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8TG9hZGVkJTIwTmFjaG9zfGVufDB8fDB8fHww",
        "category": "snacks",
    },
    {
        "name": "Glazed Donut",
        "description": "Soft ring donut with sugar glaze.",
        "price": "60.00",
        "image_url": "https://images.unsplash.com/photo-1643298892616-3737fa0c5451?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzR8fEdsYXplZCUyMERvbnV0fGVufDB8fDB8fHww",
        "category": "desserts",
    },
]


class Command(BaseCommand):
    help = "Seed the database with sample dishes"

    def handle(self, *args, **options):
        created_count = 0
        for data in SAMPLE_DISHES:
            dish, created = Dish.objects.get_or_create(
                name=data["name"],
                defaults={
                    "description": data["description"],
                    "price": data["price"],
                    "image_url": data["image_url"],
                    "is_active": True,
                    "is_best_seller": data.get("is_best_seller", False),
                    "is_new": data.get("is_new", False),
                    "category": data.get("category", Dish.Category.MEALS),
                },
            )
            if created:
                created_count += 1

        # Category normalization
        for kw in ["coffee", "chai", "latte", "cappuccino", "americano", "mocha", "tea", "lassi", "margarita", "frappe"]:
            Dish.objects.filter(name__icontains=kw).update(category=Dish.Category.BEVERAGES)

        for kw in ["fries", "wings", "sandwich", "wrap", "nacho", "pakora", "samosa", "spring roll", "garlic bread", "taco", "toast"]:
            Dish.objects.filter(name__icontains=kw).update(category=Dish.Category.SNACKS)

        for kw in ["cake", "brownie", "cheesecake", "tiramisu", "mousse", "kulfi", "jalebi", "rasmalai", "pancake", "dessert"]:
            Dish.objects.filter(name__icontains=kw).update(category=Dish.Category.DESSERTS)

        Dish.objects.filter(name__icontains="pizza").update(price="100.00", category=Dish.Category.MEALS)

        # delivery zones
        zones = [
            {"pincode_prefix": "560", "fee": "29", "eta_min": 30, "eta_max": 40},
            {"pincode_prefix": "5600", "fee": "19", "eta_min": 25, "eta_max": 35},
            {"pincode_prefix": "110", "fee": "39", "eta_min": 35, "eta_max": 45},
            {"pincode_prefix": "400", "fee": "35", "eta_min": 35, "eta_max": 50},
        ]
        for z in zones:
            DeliveryZone.objects.get_or_create(pincode_prefix=z["pincode_prefix"], defaults=z)

        self.stdout.write(self.style.SUCCESS(f"Seed complete. Dishes created: {created_count}, zones ensured."))
